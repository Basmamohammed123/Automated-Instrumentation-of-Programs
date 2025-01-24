import unittest
import os
from generate_tracing_statements import run_semgrep, extract_first_last_line_numbers, apply_summaries_to_file

class TestSemgrepAndLLM(unittest.TestCase):
    def setUp(self):
        # Path to the existing rule file
        self.rule_file = "./rule.yaml"  # Replace with the actual path to your existing rule file
        
        # Create a temporary Python test file with sample code
        self.test_code_file = "test_code.py"
        with open(self.test_code_file, "w") as f:
            f.write("""
class MyClass:
    def my_function(self):
        x = 10
        for i in range(x):
            if i % 2 == 0:
                print(i)
""")

    def tearDown(self):
        # Clean up the temporary Python test file
        os.unlink(self.test_code_file)

    def test_semgrep_and_llm(self):
        # Run Semgrep with the provided rule file and test code
        findings = run_semgrep(self.rule_file, self.test_code_file)

        # Extract line number blocks from Semgrep output
        line_number_blocks = extract_first_last_line_numbers(findings)

        # Define mock summaries for the blocks (simulating LLM output)
        mock_summaries = [
            "This is a class definition",
            "This is a method definition",
            "This is a variable declaration",
            "This is a for loop",
            "This is an if statement"
        ]

        # Apply summaries as comments to the test code
        apply_summaries_to_file(self.test_code_file, line_number_blocks, mock_summaries)

        # Read the modified file and verify the inserted comments
        with open(self.test_code_file, "r") as f:
            modified_content = f.read()

        # Expected modified content
        expected_content = """# This is a class definition
class MyClass:
    # This is a method definition
    def my_function(self):
        # This is a variable declaration
        x = 10
        # This is a for loop
        for i in range(x):
            # This is an if statement
            if i % 2 == 0:
                print(i)
"""

        # Assert the modified content matches the expected content
        self.assertEqual(modified_content, expected_content)


if __name__ == "__main__":
    unittest.main()
