import tkinter as tk
from tkinter import filedialog
import shutil
import os


def get_file_path():
    print("Second check")    # REMOVE
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Select a file")


    if file_path:

        script_dir = os.path.dirname(os.path.abspath(__file__))

        test_code_path = os.path.join(script_dir, 'test_code.py')

        try:
            with open(file_path, 'r') as source_file:
                file_contents = source_file.read()

            with open(test_code_path, 'w') as test_code_file:
                test_code_file.write(file_contents)

            print(f"Contents from {file_path} have been copied to {test_code_path}")
            return file_path
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No file selected.")
        return None
