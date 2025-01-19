import re
from transformers import AutoModel, AutoTokenizer
import os
import subprocess
import sys

# # Specify the checkpoint and device
checkpoint = "Salesforce/codet5p-220m-bimodal"
device = "cpu"  # Change to "cuda" if GPU is available

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)
model = AutoModel.from_pretrained(checkpoint, trust_remote_code=True).to(device)

def install_semgrep():
    """
    Install Semgrep using pip if it is not already installed.
    """
    print("Semgrep is not installed. Installing Semgrep...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "semgrep"])
    print("Semgrep installed successfully.")

def get_semgrep_path():
    """
    Get the path to the Semgrep executable.
    """
    scripts_dir = os.path.join(os.path.dirname(sys.executable), "Scripts")
    semgrep_path = os.path.join(scripts_dir, "semgrep.exe")
    return semgrep_path if os.path.isfile(semgrep_path) else "semgrep"

def run_semgrep(rule_file, target_file):
    """
    Run Semgrep with the specified rule file on the given Python file and return the raw output.
    """
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

def extract_first_last_line_numbers(semgrep_output):
    """
    Extracts first and last line numbers from the Semgrep output, including support for nested blocks.

    Parameters:
    semgrep_output (str): The raw output from Semgrep.

    Returns:
    list of tuples: Each tuple contains the first and last line numbers of a block.
    """
    blocks = []
    current_stack = []  # Stack to manage nested blocks
    in_block = False

    for line in semgrep_output.splitlines():
        if "Semgrep found" in line:
            # Close the current block if we're starting a new one
            if current_stack:
                first_line_number, last_line_number = current_stack.pop()
                if first_line_number and last_line_number:
                    blocks.append((first_line_number, last_line_number))
            current_stack.clear()
            in_block = True

        elif "┆----------------------------------------" in line:
            # Finalize the current block
            if current_stack:
                first_line_number, last_line_number = current_stack.pop()
                if first_line_number and last_line_number:
                    blocks.append((first_line_number, last_line_number))
            in_block = False

        elif in_block and re.match(r"^(\d+)┆", line.strip()):
            # Match line numbers and manage nested contexts
            match = re.match(r"^(\d+)┆", line.strip())
            if match:
                line_number = int(match.group(1))

                if not current_stack:
                    # Start a new block
                    current_stack.append((line_number, line_number))
                else:
                    # Update the last line number of the current block
                    first_line_number, last_line_number = current_stack[-1]
                    current_stack[-1] = (first_line_number, line_number)

    # Ensure any remaining block in the stack is added
    if current_stack:
        first_line_number, last_line_number = current_stack.pop()
        if first_line_number and last_line_number:
            blocks.append((first_line_number, last_line_number))

    return blocks

def get_blocks_from_file(file_path, line_number_blocks):
    """
    Get the content of each block based on line number ranges and store each block as a string in a list.

    Parameters:
    file_path (str): Path to the file to read from.
    line_number_blocks (list of tuples): Each tuple contains the first and last line numbers of a block.

    Returns:
    list: Each element in the list is a string representing the content of a block.
    """
    # Read the file into a list of lines
    with open(file_path, "r") as f:
        lines = f.readlines()

    # List to store the content of each block
    blocks_content = []

    # Iterate through each line number range and capture the corresponding block content
    for first, last in line_number_blocks:
        block_content = "".join(lines[first - 1:last])  # Extract and join lines in the range
        blocks_content.append(block_content)  # Store the block as a single string in the list

    return blocks_content

# Function to add summary after the function header
def add_comment_before_block(block_code, summary):
    """
    Inserts the summary as a `# summary` comment before the block.

    Parameters:
    - block_code (str): The code block as a string.
    - summary (str): The summary to insert as a comment.

    Returns:
    - str: The updated block with the `# summary` comment inserted before it.
    """
    lines = block_code.splitlines(keepends=True)  # Preserve original line endings
    if not lines:  # Handle empty blocks gracefully
        return ""

    # Determine the indentation of the first line in the block
    indent = " " * (len(lines[0]) - len(lines[0].lstrip()))
    comment = f"{indent}# {summary}\n"  # Align comment with block's indentation
    return comment + "".join(lines)  # Prepend comment to the block

def apply_summaries_to_file(file_path, line_number_blocks, summaries):
    """
    Inserts LLM-generated summaries as comments before the detected blocks in the file.

    Parameters:
    file_path (str): Path to the file to modify.
    line_number_blocks (list of tuples): Line ranges of detected blocks.
    summaries (list): Generated summaries to insert as tracing comments.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Create a mapping of line numbers to summaries to insert as comments
    insertions = {first: f"# {summary}\n" for (first, _), summary in zip(line_number_blocks, summaries)}

    # Build the modified file content
    updated_lines = []
    for i, line in enumerate(lines, start=1):
        if i in insertions:  # Check if there's a comment for this line
            updated_lines.append(insertions[i])  # Add the tracing comment
        updated_lines.append(line)  # Add the original line

    # Write the updated content back to the file in one operation
    with open(file_path, "w") as f:
        f.writelines(updated_lines)

def main():
    print("Testing!")
    # Define paths
    rule_file = os.path.expanduser("./rule.yaml")
    target_file = os.path.expanduser("./test_code.py")

    # Run Semgrep and get findings
    findings = run_semgrep(rule_file, target_file)
    print("Semgrep Findings:\n", findings)

    line_number_blocks = extract_first_last_line_numbers(findings)
    blocks_content = get_blocks_from_file(target_file, line_number_blocks)
    for i, content in enumerate(blocks_content, 1):
        print(f"Block {i} Content:\n{content}\n")

    
    summaries = []
    for func in blocks_content:
        # Tokenize the function code
        input_ids = tokenizer(func, return_tensors="pt").input_ids.to(device)
    
        # Generate summary
        generated_ids = model.generate(input_ids, max_length=200)
        summary = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    
        summaries.append(summary)

    apply_summaries_to_file(target_file, line_number_blocks, summaries)
    

if __name__ == "__main__":
    main()