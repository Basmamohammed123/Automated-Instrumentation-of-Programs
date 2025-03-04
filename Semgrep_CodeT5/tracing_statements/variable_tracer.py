import sys
import os

def trace_calls(frame, event, arg):
    """Hook function for function calls."""
    if event == "call":
        return trace_lines  # Enable line-by-line tracing
    return None

def trace_lines(frame, event, arg):
    """Hook function for line execution to track variable assignments."""
    if event == "line":
        local_vars = frame.f_locals
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno

        # Initialize variable states if not already done
        if filename not in variable_states:
            variable_states[filename] = {}

        for var_name, value in local_vars.items():
            if var_name not in variable_states[filename]:
                # Capture initial state
                variable_states[filename][var_name] = {'initial': value, 'final': value}
            else:
                # Update final state
                variable_states[filename][var_name]['final'] = value

    return trace_lines

def run_script(script_path):
    """Executes a Python script with tracing enabled."""
    if not os.path.exists(script_path):
        print(f"Error: File '{script_path}' not found.")
        return

    global variable_states
    variable_states = {}

    # Read the script
    with open(script_path, "r") as file:
        script_code = file.read()

    # Set tracing function
    sys.settrace(trace_calls)
    try:
        exec(script_code, {"__name__": "__main__"})  # Execute script safely
    finally:
        sys.settrace(None)  # Stop tracing after execution

    # Display initial and final states
    print("\nVariable States:")
    for filename, vars in variable_states.items():
        print(f"\nFile: {filename}")
        for var_name, states in vars.items():
            print(f"Variable '{var_name}': Initial = {states['initial']}, Final = {states['final']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python variable_tracer.py <script.py>")
    else:
        run_script(sys.argv[1])
