import json
import subprocess
import os
import sys
from collections import defaultdict

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
    """Runs Semgrep with the given rule file on a Python file and stores output in a JSON file."""
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
        return None
    if not os.path.isfile(target_file):
        print(f"Error: Target file '{target_file}' not found.")
        return None

    json_output_file = "semgrep_output.json"

    print(f"Running Semgrep with rule file '{rule_file}' on '{target_file}'")
    result = subprocess.run(
        [semgrep_path, "--config", rule_file, "--json", target_file],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # Save Semgrep output to a file
    with open(json_output_file, "w") as json_file:
        json_file.write(result.stdout)

    return json_output_file

def extract_call_graph(json_file):
    """Extracts function calls from Semgrep's JSON output file."""
    call_graph = defaultdict(list)

    with open(json_file, "r") as file:
        json_data = json.load(file)

    for match in json_data.get("results", []):
        if "extra" in match and "metavars" in match["extra"]:
            function_call = match["extra"]["metavars"].get("$FUNC", {}).get("abstract_content", "")
            args = match["extra"]["metavars"].get("$ARGS", {}).get("abstract_content", "")

            formatted_call = f"{function_call}({args})" if args else f"{function_call}()"

            filename = match["path"]
            if function_call:
                call_graph[filename].append(formatted_call)

    return call_graph

def display_call_graph(graph):
    """Displays the extracted call graph in text format."""
    print("\nSemgrep-Generated Call Graph:")
    for filename, calls in graph.items():
        print(f"\nFile: {filename}")
        for call in calls:
            print(f"  -> {call}")

# Rule file and target Python file (update paths if needed)
RULE_FILE = "call_graph_rule.yaml"  # Ensure this file exists in the same directory
TARGET_FILE = "test_code_call_graph.py"  # Replace with the actual Python file path

# Run Semgrep and process results
json_output_file = run_semgrep(RULE_FILE, TARGET_FILE)

if json_output_file:
    call_graph = extract_call_graph(json_output_file)
    display_call_graph(call_graph)
