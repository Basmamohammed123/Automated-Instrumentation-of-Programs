import logging
import os
import subprocess
import re
import ast
# Need coverage.py

def run_coverage(target_file, save_dir):
    """Run coverage analysis and save report to specified directory"""
    print("Running coverage.py to track executed lines...")
    coverage_path = os.path.join(save_dir, "runtime_coverage.txt")

    try:
        subprocess.run(
            ["coverage", "run", "--include", target_file, target_file],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running coverage: {e}")
        return

    # Generate and save report
    with open(coverage_path, "w") as f:
        result = subprocess.run(
            ["coverage", "report", "-m", "--include", target_file],
            stdout=subprocess.PIPE,
            text=True,
            check=False
        )
        f.write(result.stdout)
    
    print(f"Coverage report generated in '{coverage_path}'")



def extract_missing_lines(file_path, missing_line_numbers):
    """
    Extract only the actual lines of code that were not executed.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

    missing_lines_content = []
    
    # Filter only the missing lines
    for line_number in missing_line_numbers:
        if 0 < line_number <= len(lines):  # Ensure line number is within valid range
            code_line = lines[line_number - 1].strip()  # Remove extra spaces
            if code_line:  # Ensure it's not an empty line
                missing_lines_content.append(f"Line {line_number}: {code_line}")

    return missing_lines_content



def parse_missing_lines(missing_lines_raw):
    """
    Parses the missing lines field from coverage report and converts it into a list of line numbers.
    """
    missing_lines = []
    parts = missing_lines_raw.split(",")
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = map(int, part.split("-"))
            missing_lines.extend(range(start, end + 1))
        else:
            missing_lines.append(int(part))

    return missing_lines


def get_function_ranges(file_path: str) -> dict:
    """Parse a Python file to get line ranges for each function."""
    function_ranges = {}
    with open(file_path, "r") as f:
        tree = ast.parse(f.read(), filename=file_path)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start_line = node.lineno
            end_line = node.end_lineno
            function_ranges[node.name] = (start_line, end_line)
    
    return function_ranges

def format_coverage_log(target_file, coverage_path, formatted_path):
    """
    Read the coverage output and generate formatted report with function names.
    """
    try:
        with open(coverage_path, "r") as f:
            lines = f.readlines()
            if not lines:
                logging.error("❌ No coverage data found.")
                return
    except FileNotFoundError:
        logging.error(f"❌ Coverage report not found: {coverage_path}")
        return

    formatted_report = ["🛠️ Python Code Coverage Report\n", "=" * 50 + "\n"]

    target_basename = os.path.basename(target_file)
    missing_lines = set()
    function_ranges = get_function_ranges(target_file)
    coverage_summary = ""

    # Parse the raw coverage data
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith(target_basename):
            parts = line.split()
            coverage_summary = line
            if len(parts) < 5:
                continue

            missing_ranges = "".join(parts[4:]).replace(" ", "")
            if missing_ranges:
                missing_lines.update(parse_missing_lines(missing_ranges))

    if coverage_summary:
        formatted_report.append(f"{coverage_summary}\n\n")

    # Organize missing lines by function
    function_missed = {}
    for line_num in sorted(missing_lines):
        for func_name, (start, end) in function_ranges.items():
            if start <= line_num <= end:
                function_missed.setdefault(func_name, []).append(line_num)
                break
        else:
            function_missed.setdefault("Global", []).append(line_num)

    # Build detailed report
    if function_missed:
        formatted_report.append("\n🚨 **Lines NOT Executed by Function(s):**\n")
        for func, lines in function_missed.items():
            formatted_report.append(f"\n=== Function: {func} ===\n")
            code_lines = extract_missing_lines(target_file, lines)
            formatted_report.extend([f"{line}\n" for line in code_lines])
    else:
        formatted_report.append("\n✅ All lines were executed!\n")

    # Save the final report
    with open(formatted_path, "w") as f:
        f.writelines(formatted_report)

    print("📄 Formatted coverage report saved to:", formatted_path)




def get_save_directory():
    """Prompt user for directory to save coverage reports"""
    while True:
        save_dir = input("Enter directory path to save reports (press Enter for current dir): ").strip()
        if not save_dir:
            return os.getcwd()
        
        if os.path.isdir(save_dir):
            return save_dir
        print(f"Directory '{save_dir}' doesn't exist. Creating it...")
        try:
            os.makedirs(save_dir, exist_ok=True)
            return save_dir
        except Exception as e:
            print(f"Error creating directory: {e}")

def main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: python coverage_analyzer.py <target_file.py> <output_path>")
        sys.exit(1)

    target_file = sys.argv[1]
    output_path = sys.argv[2]
    formatted_path = output_path.replace(".txt", "_formatted.txt")

    run_coverage(target_file, output_path)
    format_coverage_log(target_file, output_path, formatted_path)

if __name__ == "__main__":
    main()

