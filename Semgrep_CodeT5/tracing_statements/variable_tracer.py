import sys
import traceback
import types

class VariableTracer:
    def __init__(self):
        self.initial_state = {}
        self.final_state = {}
        self.ignored_vars = {"self", "script_file", "filename", "tracer", "f", "code", "compiled_code"}

    def trace_calls(self, frame, event, arg):
        if event == "call":
            return self.trace_lines
        return None

    def trace_lines(self, frame, event, arg):
        if event != "line":
            return

        # Track only variables from the user script (not from the tracer itself)
        if "variable_tracer.py" in frame.f_code.co_filename:
            return

        local_vars = frame.f_globals.copy()  # Track global variables
        local_vars.update(frame.f_locals)  # Include local variables

        for var, value in local_vars.items():
            # Ignore built-in variables, function definitions, modules, and ignored vars
            if (var.startswith("__") or 
                isinstance(value, (types.BuiltinFunctionType, types.ModuleType, type, types.FunctionType)) or
                var in self.ignored_vars):
                continue  # Skip function definitions, modules, and ignored variables

            if var not in self.initial_state:
                self.initial_state[var] = repr(value)
            self.final_state[var] = repr(value)

        return self.trace_lines

    def start_tracing(self):
        sys.settrace(self.trace_calls)

    def stop_tracing(self):
        sys.settrace(None)

    def print_trace_results(self):
        print("\n📌  \033[1mVariable States\033[0m  📌")
        print("=" * 50)

        if not self.initial_state:
            print("No variables were traced. Ensure your script has variable assignments.")

        for var in self.initial_state:
            initial = self.initial_state[var]
            final = self.final_state.get(var, initial)

            status_emoji = "🟢"
            print(f"{status_emoji} Variable `{var}`: Initial = {initial}, Final = {final}")

        print("=" * 50)

def execute_script(filename):
    tracer = VariableTracer()
    try:
        with open(filename, "r") as f:
            code = f.read()

        compiled_code = compile(code, filename, "exec")

        tracer.start_tracing()  # Start tracing before execution
        exec(compiled_code, globals())  # FIX: Run in the global scope to track variables
        tracer.stop_tracing()

    except FileNotFoundError:
        print(f"\n❌ Error: The file '{filename}' was not found.")
    except Exception as e:
        print("\n❌ Error encountered while executing script:")
        print(traceback.format_exc())

    finally:
        tracer.print_trace_results()

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python variable_tracer.py <script_file.py>")
#         sys.exit(1)
#
#     script_file = sys.argv[1]
#     execute_script(script_file)

def main(script_file="test_code.py"):
    execute_script(script_file)

if __name__ == "__main__":
    script_file = sys.argv[1] if len(sys.argv) == 2 else "test_code.py"
    main(script_file)