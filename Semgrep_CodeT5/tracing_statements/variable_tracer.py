import sys
import traceback
import types

class VariableTracer:
    def __init__(self, output_path=None):
        self.initial_state = {}
        self.final_state = {}
        self.ignored_vars = {"self", "script_file", "filename", "tracer", "f", "code", "compiled_code"}
        self.output_lines = []
        self.output_path = output_path

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

    def output_results(self):
        self.collect_trace_results()

        output_text = "\n".join(self.output_lines)
        print(output_text)

        # Save to file
        if self.output_path:
            try:
                with open(self.output_path, "w") as out_file:
                    out_file.write(output_text)
                print(f"\n✅ Trace results saved to: {self.output_path}")
            except Exception as e:
                print(f"\n❌ Error saving trace results: {e}")


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
        tracer.output_results()


def main():
    script_file = sys.argv[1] if len(sys.argv) > 1 else "test_code.py"
    execute_script(script_file)

if __name__ == "__main__":
    main()
