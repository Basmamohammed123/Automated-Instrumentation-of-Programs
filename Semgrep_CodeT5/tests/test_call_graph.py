#Basma Mohammed, 101187310
import unittest
import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tracing_statements.generate_call_graph import create_trace_calls, display_call_graph, call_graph

class TestCallGraphTracing(unittest.TestCase):
    
    def setUp(self):
        """Setup before each test."""
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.test_script = os.path.abspath(os.path.join(base_path, "../test_code/test_code_call_graph.py"))

        if not os.path.exists(self.test_script):
            raise FileNotFoundError(f"Script not found at {self.test_script}")

    def test_trace_function_calls(self):
        """Check if function calls are traced correctly."""
        global call_graph  # Ensure we're modifying the correct global call_graph
        call_graph.clear()  # Reset before each test

        trace_function = create_trace_calls(self.test_script)  # Create trace function

        # Start tracing globally
        sys.settrace(trace_function)

        try:
            with open(self.test_script, encoding='utf-8') as f:
                code = compile(f.read(), self.test_script, 'exec')
                exec(code, {"__builtins__": __builtins__, "__name__": "__main__"})  # Ensure correct execution context
        finally:
            sys.settrace(None)  # Always disable tracing after execution

        # Debugging output
        print("Captured Call Graph:", dict(call_graph))

        # Expected function call relationships based on test_code_call_graph.py
        expected_graph = {
            "Program Start": ["<module>"],
            "f1": ["f2", "f3"],
            "f2": ["f3"],
            "f3": ["f4"]
        }

        cleaned_call_graph = {k: v for k, v in call_graph.items() if k != "<module>"}

        cleaned_call_graph = {k: sorted(set(v)) for k, v in cleaned_call_graph.items()}

        self.assertEqual(cleaned_call_graph, expected_graph)

    def test_display_call_graph(self):
        """Check if the call graph prints correctly without errors."""
        global call_graph
        call_graph.clear()
        call_graph.update({
            "Program Start": ["f1"],
            "f1": ["f2", "f3"],
            "f2": ["f3"],
            "f3": ["f4"]
        })

        try:
            display_call_graph(call_graph)
        except Exception as e:
            self.fail(f"display_call_graph failed with error: {e}")

if __name__ == "__main__":
    unittest.main()
