import tkinter as tk
from tkinter import ttk
import os

class UI:
    def __init__(self, controller):
        self.root = None
        self.text_box = None
        self.status_label = None
        self.control = None
        self.control = controller

    def open_results_window(self):
        file_path = os.path.expanduser("./test_code.py")


        results_window = tk.Toplevel(self.root)
        results_window.title("Parsing Results")
        results_window.geometry("600x450")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    result_text = file.read()
            except Exception as e:
               print("Error", f"Failed to load file: {str(e)}")

        result_text_widget = tk.Text(results_window, wrap=tk.WORD, height=20, width=80, font=("Courier New", 12), bg="#ffffff", fg="#007acc")
        result_text_widget.insert(tk.END, result_text)
        result_text_widget.pack(padx=10, pady=10)

        close_button = ttk.Button(results_window, text="Close", command=results_window.destroy)
        close_button.pack(pady=10)

    def main(self):
        self.root = tk.Tk()
        self.root.title("Code Summarization Program")
        self.root.geometry("700x500")  # Larger size for better layout
        self.root.configure(bg="#003366")
        # Styling
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TButton", font=("Arial", 12), padding=6, background="#00509e", foreground="white")
        style.configure("TLabel", font=("Arial", 12), padding=4, background="#003366", foreground="white")
        style.configure("TFrame", background="#003366")

        # Top frame
        top_frame = ttk.Frame(self.root, padding="10 10 10 10")
        top_frame.pack(fill=tk.X)
        ttk.Label(top_frame, text="Code Summarization Program", font=("Arial", 16, "bold")).pack(pady=5)

        # Middle frame
        middle_frame = tk.Frame(self.root, bg= "#003366", padx=10, pady=10)
        middle_frame.pack(fill=tk.BOTH, expand=True)

        self.text_box = tk.Text(middle_frame, wrap=tk.WORD, height=15, width=60, font=("Courier New", 12), bg="#F4F4F4")
        self.text_box.pack(pady=10, padx=10)

        # Bottom frame (buttons)
        bottom_frame = ttk.Frame(self.root, padding="10 10 10 10")
        bottom_frame.pack(fill=tk.X)

        upload_button = ttk.Button(bottom_frame, text="Upload", command=self.control.upload_file)
        upload_button.pack(side=tk.LEFT, padx=10)

        parse_button = ttk.Button(bottom_frame, text="Summarize", command=self.control.parse_content)
        parse_button.pack(side=tk.LEFT, padx=10)

        save_button = ttk.Button(bottom_frame, text="Save", command=self.control.save_file)
        save_button.pack(side=tk.LEFT, padx=10)

        exit_button = ttk.Button(bottom_frame, text="Exit", command=self.root.destroy)
        exit_button.pack(side=tk.LEFT, padx=10)


        # Status bar
        self.status_label = ttk.Label(self.root, text="Ready", anchor=tk.W, background="#002244", foreground="white", relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X, pady=5)

        self.root.mainloop()



    """
    
def multiply(a, lst):
    while a > 0:
        for i in lst:
            i + a
    return lst


def divide(a, b):
    return a / b
    
    
    
    """