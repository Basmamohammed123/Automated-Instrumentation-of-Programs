import os
import subprocess
import sys
import re

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
    Extracts the first and last line numbers from each block of findings in the Semgrep output.

    Parameters:
    semgrep_output (str): The raw output from Semgrep.

    Returns:
    list of tuples: Each tuple contains the first and last line numbers of a block.
    """
    blocks = []
    first_line_number = None
    last_line_number = None
    in_block = False  # Flag to track when we're inside a block

    for line in semgrep_output.splitlines():
        # Detect the start of a block based on "Semgrep found"
        if "Semgrep found" in line:
            # If we're already capturing a block, finalize it before starting a new one
            first_line_number = None  # Reset for the new block
            last_line_number = None
            in_block = True  # Start capturing lines in the new block
        elif "┆----------------------------------------" in line or "❯❱" in line or "❱" in line:
            # Separator line signals the end of the current block
            if first_line_number is not None and last_line_number is not None:
                blocks.append((first_line_number, last_line_number))
            in_block = False  # Stop capturing until the next "Semgrep found" line
        elif in_block and re.match(r"^(\d+)┆", line.strip()):
            # Capture line numbers that start with a digit followed by "┆"
            match = re.match(r"^(\d+)┆", line.strip())
            if match:
                line_number = int(match.group(1))
                if first_line_number is None:
                    # This is the first line number in the block
                    first_line_number = line_number
                # Continuously update the last line number until the end of the block
                last_line_number = line_number

    # Add the last block if there was no trailing separator
    if first_line_number is not None and last_line_number is not None:
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

def insert_statements(file_path, blocks, statement):
    """
    Insert a comment statement before the first line of each block in the specified file.

    Parameters:
    file_path (str): Path to the file to modify.
    blocks (list of lists): Each inner list contains line numbers of a block.
    statement (str): The comment statement to insert before each block.
    """
    if not blocks:
        print("No blocks to process.")
        return

    # Read the original file
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Insert the comment statement before the first line of each block
    offset = 0
    for block in blocks:
        if block:  # Ensure the block is not empty
            first_line_number = int(block[0])
            index = first_line_number - 1 + offset
            lines.insert(index, str("# " + statement + "\n"))
            offset += 1  # Adjust for the newly added line

    # Write the modified file back
    with open(file_path, "w") as f:
        f.writelines(lines)

    print(f"Inserted statements in {file_path}.")

def main():
    # Define paths
    rule_file = os.path.expanduser("./rule.yaml")
    target_file = os.path.expanduser("./test_code.py")
    statement = "Block Found!"  # The statement to insert

    # Run Semgrep and get findings
    findings = run_semgrep(rule_file, target_file)
    print("Semgrep Findings:\n", findings)

    line_number_blocks = extract_first_last_line_numbers(findings)
    #for i, (first, last) in enumerate(line_number_blocks, 1):
     #   print(f"Block {i}: First line number = {first}, Last line number = {last}")
    #insert_statements(target_file, line_number_blocks, statement)
    
    blocks_content = get_blocks_from_file(target_file, line_number_blocks)
    for i, content in enumerate(blocks_content, 1):
        print(f"Block {i} Content:\n{content}\n")

if __name__ == "__main__":
    main()