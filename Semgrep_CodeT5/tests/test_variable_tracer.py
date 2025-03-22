import unittest
import types
import sys
from io import StringIO
import textwrap
import os

# Add the root directory (Semgrep_CodeT5) to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tracing_statements.variable_tracer import VariableTracer

class TestSampleScript(unittest.TestCase):
    def setUp(self):
        self.tracer = VariableTracer()
        self.original_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        sys.stdout = self.original_stdout

    def test_sample_script_variable_states(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test_code', 'sample.py'))
        
        # Run the script with tracing
        try:
            with open(script_path, 'r') as f:
                code = f.read()
            compiled = compile(code, script_path, 'exec')
            self.tracer.start_tracing()
            exec_globals = {}
            exec(compiled, exec_globals)
            self.tracer.stop_tracing()
        finally:
            self.tracer.print_trace_results()

        # Expected values
        expected_initial = {
            'x': '10',
            'y': '20',
            'z': '30',
            'a': "'Hello'",
            'b': '[1, 2, 3]',
            'd': '10',
            'c': '20',
            'w': '30'
        }
        expected_final = {
            'x': '50',
            'y': '100',
            'z': '30',
            'a': "'World'",
            'b': '[1, 2, 3]',
            'd': '10',
            'c': '20',
            'w': '30'
        }

        # Assert variable states
        for var, init_val in expected_initial.items():
            self.assertIn(var, self.tracer.initial_state, f"Missing variable: {var}")
            self.assertEqual(self.tracer.initial_state[var], init_val, f"Incorrect initial value for {var}")
        for var, final_val in expected_final.items():
            self.assertIn(var, self.tracer.final_state, f"Missing variable: {var}")
            self.assertEqual(self.tracer.final_state[var], final_val, f"Incorrect final value for {var}")

    def test_no_variables_script(self):
        # This code contains only ignored/built-in variables
        code = """
def unused_function():
    pass

__version__ = "1.0"

print("Hello World")
"""

        compiled = compile(code, "<no_vars_script>", "exec")
        self.tracer.start_tracing()
        exec_globals = {}
        exec(compiled, exec_globals)
        self.tracer.stop_tracing()

        self.tracer.print_trace_results()
        output = sys.stdout.getvalue()

        # Assert that no user-defined variables were traced
        self.assertEqual(len(self.tracer.initial_state), 0)
        self.assertIn("No variables were traced", output)


if __name__ == "__main__":
    unittest.main()
