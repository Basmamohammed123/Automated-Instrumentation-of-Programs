import sys
import traceback
import types

class VariableTracer:
    def __init__(self):
        self.initial_state = {}
        self.final_state = {}
        self.ignored_vars = {"self", "script_file", "filename", "tracer", "f", "code", "compiled_code"}
        self.output_lines = []

    def trace_calls(self, frame, event, arg):
        if event == "call":
            return self.trace_lines
        return None

    def trace_lines(self, frame, event, arg):
        if event != "line":
            return

        if "variable_tracer.py" in frame.f_code.co_filename:
            return

        local_vars = frame.f_globals.copy()
        local_vars.update(frame.f_locals)

        for var, value in local_vars.items():
            if (var.startswith("__") or 
                isinstance(value, (types.BuiltinFunctionType, types.ModuleType, type, types.FunctionType)) or
                var in self.ignored_vars):
                continue

            if var not in self.initial_state:
                self.initial_state[var] = repr(value)
            self.final_state[var] = repr(value)

        return self.trace_lines

    def start_tracing(self):
        sys.settrace(self.trace_calls)

    def stop_tracing(self):
        sys.settrace(None)

    def collect_trace_results(self):
        self.output_lines.append("📌  Variable States  📌")
        self.output_lines.append("=" * 50)

        if not self.initial_state:
            self.output_lines.append("No variables were traced. Ensure your script has variable assignments.")

        for var in self.initial_state:
            initial = self.initial_state[var]
            final = self.final_state.get(var, initial)
            self.output_lines.append(f"🟢 Variable `{var}`: Initial = {initial}, Final = {final}")

        self.output_lines.append("=" * 50)

    def save_trace_results(self, path=None):
        self.collect_trace_results()
        if path:
            with open(path, "w") as out_file:
                out_file.write("\n".join(self.output_lines))
        else:
            print("\n".join(self.output_lines))


def execute_script(filename, output_path=None):
    tracer = VariableTracer()
    try:
        with open(filename, "r") as f:
            code = f.read()

        compiled_code = compile(code, filename, "exec")
        tracer.start_tracing()
        exec(compiled_code, globals())
        tracer.stop_tracing()

    except FileNotFoundError:
        print(f"\n❌ Error: The file '{filename}' was not found.")
    except Exception as e:
        print("\n❌ Error encountered while executing script:")
        print(traceback.format_exc())
    finally:
        tracer.save_trace_results(output_path)


def main():
    if len(sys.argv) < 2:
        print("Usage: python variable_tracer.py <script_file.py> [output_file.txt]")
        sys.exit(1)

    script_file = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    execute_script(script_file, output_path)

if __name__ == "__main__":
    main()
