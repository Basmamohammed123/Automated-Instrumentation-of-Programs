import os
import sys

def copy_to_test_code(source_file):
    if not source_file.endswith('.py'):
        print("Error: Only Python files can be copied.")
        return

    target_file = os.path.join(os.path.dirname(__file__), 'test_code.py')

    try:
        with open(source_file, 'r') as src, open(target_file, 'w') as dest:
            dest.write(src.read())
        print(f"Contents copied to: {target_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python copy_contents.py <source_file>")
    else:
        copy_to_test_code(sys.argv[1])
