import os
import subprocess
import sys
import re

def install_semgrep():
    print("Semgrep is not installed. Installing Semgrep...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "semgrep"])
    print("Semgrep installed successfully.")

def get_semgrep_path():
    scripts_dir = os.path.join(os.path.dirname(sys.executable), "Scripts")
    semgrep_path = os.path.join(scripts_dir, "semgrep.exe")
    return semgrep_path if os.path.isfile(semgrep_path) else "semgrep"

def run_semgrep(rule_file, target_file):
    semgrep_path = get_semgrep_path()

    try:
        subprocess.run([semgrep_path, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        install_semgrep()
        semgrep_path = get_semgrep_path()
    except subprocess.CalledProcessError:
        print("Warning: Semgrep version check failed. Attempting to run Semgrep anyway.")

    if not os.path.isfile(rule_file):
        print(f"Error: Rule file '{rule_file}' not found.")
        return ""
    if not os.path.isfile(target_file):
        print(f"Error: Target file '{target_file}' not found.")
        return ""

    print(f"Running Semgrep on {target_file}")
    result = subprocess.run(
        [semgrep_path, "--config", rule_file, target_file],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return result.stdout

def insert_runtime_tracing(file_path, line_number_blocks):
    """
    Insert print statements for runtime tracing at the start of each identified block,
    ensuring correct indentation and avoiding indentation errors.
    """
    if not line_number_blocks:
        print("No blocks to process.")
        return

    # Clear previous contents of runtime_log.txt before execution
    open("runtime_log.txt", "w").close()

    with open(file_path, "r") as f:
        lines = f.readlines()

    offset = 0
    for block in line_number_blocks:
        if block:
            first_line_number, last_line_number = block
            index = first_line_number - 1 + offset
            if index < len(lines):
                # Determine the indentation level of the current line
                current_line = lines[index]
                indentation = re.match(r"^(\s*)", current_line).group(1)

                # Construct runtime tracing statements with correct indentation
                trace_statement = (
                    f'{indentation}print(f"Executing block: lines {first_line_number}-{last_line_number}")\n'
                    f'{indentation}with open("runtime_log.txt", "a") as log_file:\n'
                    f'{indentation}    log_file.write(f"Block executed: lines {first_line_number}-{last_line_number}\\n")\n'
                )

                # Insert the trace statements at the correct position
                lines.insert(index, trace_statement)
                offset += 3  # Three lines were added for each block

    with open(file_path, "w") as f:
        f.writelines(lines)

    print(f"Inserted runtime tracing statements with logging in {file_path}.")



def extract_first_last_line_numbers(semgrep_output):
    blocks = []
    first_line_number = None
    last_line_number = None
    in_block = False

    for line in semgrep_output.splitlines():
        if "Semgrep found" in line:
            first_line_number = None
            last_line_number = None
            in_block = True
        elif "┆----------------------------------------" in line:
            if first_line_number is not None and last_line_number is not None:
                blocks.append((first_line_number, last_line_number))
            in_block = False
        elif in_block and re.match(r"^(\d+)┆", line.strip()):
            match = re.match(r"^(\d+)┆", line.strip())
            if match:
                line_number = int(match.group(1))
                if first_line_number is None:
                    first_line_number = line_number
                last_line_number = line_number

    # Ensure that the function's last line is included properly
    if first_line_number is not None and last_line_number is not None:
        blocks.append((first_line_number, last_line_number))

    return blocks


def generate_coverage_log_with_line_ranges(semgrep_output, target_file):
    """
    Generate a detailed code coverage log with line ranges based on Semgrep output.
    """
    summary = {}
    detailed_report = []
    current_pattern_type = None
    current_pattern_desc = None
    current_start_line = None
    current_end_line = None

    for line in semgrep_output.splitlines():
        if "Semgrep found" in line and ":" in line:
            if current_pattern_desc and current_start_line and current_end_line:
                key = f"{current_pattern_type} ({current_pattern_desc})"
                summary[key] = summary.get(key, 0) + 1
                detailed_report.append(f"{key} at lines {current_start_line}-{current_end_line}")

            current_pattern_type = line.split(":")[0].replace("Semgrep found", "").strip()
            current_pattern_desc = line.split(":", 1)[1].strip()
            current_start_line = current_end_line = None

        elif re.match(r"^\s*(\d+)┆", line):
            current_line_number = int(re.match(r"^\s*(\d+)┆", line).group(1))
            if current_start_line is None:
                current_start_line = current_line_number
            current_end_line = current_line_number

    if current_pattern_desc and current_start_line and current_end_line:
        key = f"{current_pattern_type} ({current_pattern_desc})"
        summary[key] = summary.get(key, 0) + 1
        detailed_report.append(f"{key} at lines {current_start_line}-{current_end_line}")

    with open("coverage_log.txt", "w") as log_file:
        log_file.write("Code Coverage Report\n")
        log_file.write("===================\n\n")
        log_file.write(f"File: {target_file}\n\n")
        log_file.write("Summary of Patterns Detected:\n")
        log_file.write("----------------------------\n")
        for pattern, count in summary.items():
            log_file.write(f"{pattern}: {count} occurrences\n")

        log_file.write("\nDetailed Report:\n")
        log_file.write("----------------\n")
        for entry in detailed_report:
            log_file.write(f"{entry}\n")

    print("Code coverage log with line ranges generated in coverage_log.txt")

def compare_coverage_logs(static_log="coverage_log.txt", runtime_log="runtime_log.txt"):
    """
    Compare static coverage log with runtime coverage log and calculate executed percentage.
    """
    static_blocks = set()
    runtime_blocks = set()

    with open(static_log, "r") as f:
        for line in f:
            match = re.search(r"at lines (\d+)-(\d+)", line)
            if match:
                static_blocks.add((int(match.group(1)), int(match.group(2))))

    with open(runtime_log, "r") as f:
        for line in f:
            match = re.search(r"Block executed: lines (\d+)-(\d+)", line)
            if match:
                runtime_blocks.add((int(match.group(1)), int(match.group(2))))

    executed_blocks = static_blocks.intersection(runtime_blocks)
    coverage_percentage = (len(executed_blocks) / len(static_blocks)) * 100 if static_blocks else 0

    print("\nCoverage Report")
    print("===================")
    print(f"Total Static Blocks: {len(static_blocks)}")
    print(f"Executed Blocks: {len(executed_blocks)}")
    print(f"Coverage Percentage: {coverage_percentage:.2f}%")

    
def remove_runtime_tracing(file_path):
    """
    Remove all runtime tracing statements from the specified file.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

    cleaned_lines = []
    skip_line = False

    for line in lines:
        if 'print(f"Executing block:' in line or 'with open("runtime_log.txt"' in line:
            skip_line = True
        elif skip_line and 'log_file.write' in line:
            skip_line = False
        else:
            cleaned_lines.append(line)

    with open(file_path, "w") as f:
        f.writelines(cleaned_lines)

    print(f"Removed runtime tracing statements from {file_path}.")

def main():
    rule_file = os.path.expanduser("./rule.yaml")
    target_file = os.path.expanduser("./test_code.py")

    # Step 1: Static Coverage Analysis
    findings = run_semgrep(rule_file, target_file)
    print("Static Coverage Findings:\n", findings)
    generate_coverage_log_with_line_ranges(findings, target_file)

    # Step 2: Insert Runtime Tracing
    line_number_blocks = extract_first_last_line_numbers(findings)
    insert_runtime_tracing(target_file, line_number_blocks)
    
    # Step 3: Run Instrumented Code to Generate Runtime Log
    print("Running the instrumented code...")
    try:
        subprocess.run([sys.executable, target_file], check=True, stderr=subprocess.STDOUT)
        print("Runtime log generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running the instrumented code: {e}")
        return
    
    # Step 4: Compare Coverage Logs
    compare_coverage_logs("coverage_log.txt", "runtime_log.txt")

    # Step 5: Cleanup
    remove_runtime_tracing(target_file)
    print(f"Restored {target_file} to its original state.")
    
    # Verify line number blocks
    for i, (first, last) in enumerate(line_number_blocks, 1):
        print(f"Block {i}: First line = {first}, Last line = {last}")

if __name__ == "__main__":
    main()