import os
import subprocess
import re
import ast

def run_coverage(target_file):
    """Run coverage analysis on the target file."""
    print("Running coverage.py to track executed lines...")

    try:
        # Run the target file with coverage
        subprocess.run(
            ["coverage", "run", "--include", target_file, target_file],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running target file: {e}")
        return

    # Always generate and save the report (even if empty)
    with open("runtime_coverage.txt", "w") as f:
        result = subprocess.run(
            ["coverage", "report", "-m", "--include", target_file],
            stdout=subprocess.PIPE,
            text=True,
            check=False
        )
        f.write(result.stdout)
    
    # Print the report to terminal
    print(result.stdout)
    print("Coverage report generated in 'runtime_coverage.txt'.")



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

def format_coverage_log(target_file):
    """
    Read the coverage output and generate formatted report with function names.
    """
    try:
        with open("runtime_coverage.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("❌ Error: Coverage data not found. Run analysis first.")
        return

    formatted_report = []
    formatted_report.append("🛠️  Python Code Coverage Report\n")
    formatted_report.append("=" * 50 + "\n")

    target_basename = os.path.basename(target_file)
    missing_lines = set()
    function_ranges = get_function_ranges(target_file)
    coverage_summary = ""

    # Parse coverage data
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith(target_basename):
            parts = line.split()
            coverage_summary = line  # Capture the summary line
            if len(parts) < 5:
                continue

            missing_ranges = "".join(parts[4:]).replace(" ", "")
            if missing_ranges:
                missing_lines.update(parse_missing_lines(missing_ranges))

    # Add the original coverage summary line
    if coverage_summary:
        formatted_report.append(f"{coverage_summary}\n\n")

    # Group missed lines by function
    function_missed = {}
    for line_num in sorted(missing_lines):
        for func_name, (start, end) in function_ranges.items():
            if start <= line_num <= end:
                if func_name not in function_missed:
                    function_missed[func_name] = []
                function_missed[func_name].append(line_num)
                break
        else:
            if 'Global' not in function_missed:
                function_missed['Global'] = []
            function_missed['Global'].append(line_num)

    # Build formatted report
    if function_missed:
        formatted_report.append("\n🚨 **Lines NOT Executed by Function(s):**\n")
        for func, lines in function_missed.items():
            formatted_report.append(f"\n=== Function: {func} ===\n")
            code_lines = extract_missing_lines(target_file, lines)
            formatted_report.extend([f"{line}\n" for line in code_lines])
    else:
        formatted_report.append("\n✅ All lines were executed!\n")

    with open("formatted_coverage_log.txt", "w") as f:
        f.writelines(formatted_report)
    
    print("Formatted report saved to 'formatted_coverage_log.txt'")

def main():
    target_file = "test_code.py"  # Update this with your actual script file

    # Step 1: Run Coverage Analysis
    run_coverage(target_file)

    # Step 2: Format Coverage Report
    format_coverage_log(target_file)

if __name__ == "__main__":
    main()