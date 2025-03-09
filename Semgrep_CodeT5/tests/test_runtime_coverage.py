import unittest
from unittest.mock import patch, mock_open, call, MagicMock
import tempfile
import os
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../tracing_statements')))

from runtime_coverage import (
    parse_missing_lines,
    extract_missing_lines,
    run_coverage,
    format_coverage_log
)

class TestCoverageAnalysis(unittest.TestCase):
    def setUp(self):
        self.test_file = """def simple_func():
    print("test")
"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file_path = os.path.join(self.temp_dir.name, "test_code.py")
        with open(self.test_file_path, 'w') as f:
            f.write(self.test_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parse_missing_lines(self):
        self.assertEqual(parse_missing_lines("1-3"), [1, 2, 3])
        self.assertEqual(parse_missing_lines("5"), [5])

    def test_extract_missing_lines(self):
        with patch('builtins.open', mock_open(read_data="Line 1\nLine 2")):
            result = extract_missing_lines("dummy.txt", [1])
            self.assertEqual(result, ["Line 1: Line 1"])

    @patch('subprocess.run')
    def test_run_coverage_success(self, mock_run):
        mock_run.return_value = MagicMock(stdout="Coverage report")
        run_coverage(self.test_file_path)
        mock_run.assert_any_call(
            ["coverage", "run", "--include", self.test_file_path, self.test_file_path],
            check=True, capture_output=True, text=True
        )

    @patch('subprocess.run')
    def test_run_coverage_failure(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, "cmd", output=b"Error")
        with self.assertLogs(level='ERROR') as cm:
            run_coverage(self.test_file_path)
            self.assertTrue(any("Error running coverage" in msg for msg in cm.output))

            
    @patch('runtime_coverage.get_function_ranges')
    def test_format_coverage_log(self, mock_func_ranges):
        mock_func_ranges.return_value = {'simple_func': (1, 2)}
        with patch('builtins.open', mock_open(read_data="test_code.py 2 0 100%")):
            format_coverage_log(self.test_file_path)
            with open("formatted_coverage_log.txt") as f:
                content = f.read()
                self.assertIn("100%", content)

    def test_empty_coverage_log(self):
        with patch('builtins.open', mock_open(read_data="")):
            with self.assertLogs(level='ERROR') as cm:
                format_coverage_log(self.test_file_path)
                self.assertTrue(any("No coverage data found" in msg for msg in cm.output))

if __name__ == '__main__':
    unittest.main()