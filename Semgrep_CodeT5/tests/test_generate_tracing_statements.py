import unittest
import os
import subprocess
from tracing_statements.generate_tracing_statements import generate_summary, install_semgrep, get_semgrep_path, run_semgrep, extract_first_last_line_numbers

class TestGenerateTracingStatements(unittest.TestCase):
    
    def test_install_semgrep(self):
        """Test that Semgrep is installed correctly."""
        try:
            subprocess.run(["semgrep", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            install_semgrep()
    
        result = subprocess.run(["semgrep", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertRegex(result.stdout.strip(), r'^\d+\.\d+\.\d+$')

    def test_get_semgrep_path(self):
        """Test if Semgrep path is correctly resolved."""
        semgrep_path = get_semgrep_path()
        self.assertTrue(os.path.isfile(semgrep_path) or semgrep_path == "semgrep")
    
    def test_run_semgrep(self):
        """Test running Semgrep on a sample rule file and target file."""
        rule_file = "./tracing_statements/rule.yaml"  # Assume test rule exists
        target_file = "./test_code/sample2.py"  # Assume test code exists
        
        if not os.path.isfile(rule_file) or not os.path.isfile(target_file):
            self.skipTest("Missing test files for Semgrep execution")
        
        output = run_semgrep(rule_file, target_file)
        self.assertIsInstance(output, str)
    
    def test_extract_first_last_line_numbers(self):
        """Test extraction of line number blocks from Semgrep output."""
        sample_output = """
        Semgrep found an issue:
        3┆    print("Error detected")
        ┆----------------------------------------
        """
        result = extract_first_last_line_numbers(sample_output)
        self.assertEqual(result, [(3, 3)])
    
    def test_generate_summary(self):
        """Test LLM-generated summary function."""
        sample_code = "def test_func():\n    print('Hello')\n"
        summary = generate_summary(sample_code)
        self.assertIsInstance(summary, str)
        self.assertTrue(len(summary) > 0)

if __name__ == "__main__":
    unittest.main()
