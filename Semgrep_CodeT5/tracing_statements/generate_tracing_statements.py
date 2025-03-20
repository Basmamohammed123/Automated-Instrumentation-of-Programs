import re
from transformers import AutoModel, AutoTokenizer
import os
import subprocess
import sys

checkpoint = "Salesforce/codet5p-220m-bimodal"
device = "cpu"

tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)
model = AutoModel.from_pretrained(checkpoint, trust_remote_code=True).to(device)

def install_semgrep():
    """Install Semgrep using pip if it is not already installed."""
    print("Semgrep is not installed. Installing Semgrep...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "semgrep"])
    print("Semgrep installed successfully.")

def get_semgrep_path():
    """Get the path to the Semgrep executable."""
    scripts_dir = os.path.join(os.path.dirname(sys.executable), "Scripts")
    semgrep_path = os.path.join(scripts_dir, "semgrep.exe")
    return semgrep_path if os.path.isfile(semgrep_path) else "semgrep"

def run_semgrep(rule_file, target_file):
    """Run Semgrep with the specified rule file on the given Python file and return the raw output."""
    semgrep_path = get_semgrep_path()

    try:
        subprocess.run([semgrep_path, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        install_semgrep()
        semgrep_path = get_semgrep_path()
    except subprocess.CalledProcessError:
        print("Warning: Semgrep version check failed. Attempting to run Semgrep anyway.")

    if not os.path.isfile(rule_file) or not os.path.isfile(target_file):
        print(f"Error: Missing files: rule_file='{rule_file}', target_file='{target_file}'")
        return ""

    print(f"Running Semgrep on {target_file}")
    result = subprocess.run(
        [semgrep_path, "--config", rule_file, target_file],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    return result.stdout

def extract_first_last_line_numbers(semgrep_output):
    """Extracts first and last line numbers from the Semgrep output, including support for nested blocks."""
    blocks = []
    current_stack = []
    in_block = False

    for line in semgrep_output.splitlines():
        if "Semgrep found" in line:
            if current_stack:
                first_line_number, last_line_number = current_stack.pop()
                if first_line_number and last_line_number:
                    blocks.append((first_line_number, last_line_number))
            current_stack.clear()
            in_block = True

        elif "┆----------------------------------------" in line:
            if current_stack:
                first_line_number, last_line_number = current_stack.pop()
                if first_line_number and last_line_number:
                    blocks.append((first_line_number, last_line_number))
            in_block = False

        elif in_block and re.match(r"^(\d+)┆", line.strip()):
            match = re.match(r"^(\d+)┆", line.strip())
            if match:
                line_number = int(match.group(1))

                if not current_stack:
                    current_stack.append((line_number, line_number))
                else:
                    first_line_number, last_line_number = current_stack[-1]
                    current_stack[-1] = (first_line_number, line_number)

    if current_stack:
        first_line_number, last_line_number = current_stack.pop()
        if first_line_number and last_line_number:
            blocks.append((first_line_number, last_line_number))

    return blocks

def get_blocks_from_file(file_path, line_number_blocks):
    """Get the content of each block based on line number ranges and store each block as a string in a list."""
    with open(file_path, "r") as f:
        lines = f.readlines()

    return ["".join(lines[first - 1:last]) for first, last in line_number_blocks]

def generate_summary(block_code):
    """Generates a basic LLM-generated summary of the given function."""
    input_ids = tokenizer(block_code, return_tensors="pt").input_ids.to(device)
    generated_ids = model.generate(input_ids, max_length=300)
    summary = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    return summary

def apply_summaries_and_tracing_to_file(file_path, line_number_blocks, summaries):
    """Inserts LLM-generated summaries as docstrings inside functions and adds enhanced TRACE logs at the beginning of each function."""
    
    log_file = "trace_log.txt"  # Define the log file

    with open(file_path, "r") as f:
        lines = f.readlines()

    insertions = {}
    for (first, _), summary in zip(line_number_blocks, summaries):
        indent = " " * (len(lines[first - 1]) - len(lines[first - 1].lstrip()))  # Match function indentation
        insertions[first] = f'{indent}"""\n{indent}{summary.strip()}\n{indent}"""\n'

    updated_lines = []
    for i, line in enumerate(lines, start=1):
        stripped_line = line.strip()

        if i in insertions:
            updated_lines.append(insertions[i])  # Insert docstring with correct indentation

        updated_lines.append(line)

        # Inject enhanced entry trace logs **inside** the function with correct indentation
        if line.strip().startswith("def "):
            function_name_match = re.match(r"def (\w+)\((.*?)\)", line.strip())
            if function_name_match:
                function_name = function_name_match.group(1)
                params = function_name_match.group(2).strip()
                
                indent = " " * (len(line) - len(line.lstrip()) + 4)

                if params:
                    param_list = [p.split('=')[0].strip() for p in params.split(', ') if p.split('=')[0].strip() != 'self']
                    if param_list:
                        param_values = ', '.join([f'{p}={{ {p} }}' for p in param_list])
                        trace_code = f'{indent}print(f"TRACE: Entering {function_name} function with parameters: {param_values}")\n'
                    else:
                        trace_code = f'{indent}print(f"TRACE: Entering {function_name} function with no parameters")\n'
                else:
                    trace_code = f'{indent}print(f"TRACE: Entering {function_name} function with no parameters")\n'
                
                updated_lines.append(trace_code)

    with open(file_path, "w") as f:
        f.writelines(updated_lines)

def main():
    print("Testing automated instrumentation...")
    rule_file = "rule.yaml"
    target_file = "test_code.py"

    findings = run_semgrep(rule_file, target_file)
    print("Semgrep Findings:\n", findings)

    line_number_blocks = extract_first_last_line_numbers(findings)
    blocks_content = get_blocks_from_file(target_file, line_number_blocks)

    summaries = [generate_summary(block) for block in blocks_content]

    apply_summaries_and_tracing_to_file(target_file, line_number_blocks, summaries)

if __name__ == "__main__":
    main()
