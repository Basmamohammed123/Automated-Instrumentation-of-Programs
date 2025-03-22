import tkinter as tk
from tkinter import scrolledtext
import file_loader
import sys

file_path = file_loader.get_file_path()

def read_test_code():
    try:
        with open("test_code.py", "r") as file:
            return file.read()
    except FileNotFoundError:
        return "Error: test_code.py not found."

def on_closing():
    root.destroy()
    root.quit()

class RedirectText:

    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.configure(state="normal")
        self.text_widget.insert(tk.END, string)
        self.text_widget.configure(state="disabled")
        self.text_widget.see(tk.END)  # Auto-scroll to the bottom

    def flush(self):
        pass  # Needed for compatibility with sys.stdout

def handle_choice_action(choice):
    print(f"User selected: {choice}")

    if choice == "1. Generate Tracing Statements":
        import generate_tracing_statements
        generate_tracing_statements.main()

    elif choice == "2. Create Call Graph":
        import  generate_call_graph
        generate_call_graph.main()

    elif choice == "3. Runtime Coverage":
        import runtime_coverage
        runtime_coverage.main()

    elif choice == "4. Track Variables":
        import variable_tracer
        variable_tracer.main()

    file_loader.save_file()


root = tk.Tk()
root.title("Automated Instrumentation Options: ")
root.geometry("1000x700")
root.config(bg="#8996a1")

root.protocol("WM_DELETE_WINDOW", on_closing)

path_label = tk.Label(root, text=f"Path: {file_path if file_path else 'No file selected'}", font=("Arial", 10, "bold"))
path_label.pack(pady=(10,5))

text_area = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD)
text_area.insert(tk.INSERT, read_test_code())
text_area.configure(state="disabled")
text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

sys.stdout = RedirectText(text_area)

button_frame = tk.Frame(root, bg="#f4f4f9")
button_frame.pack(pady=15, fill=tk.X)

button_style = {
    'font': ("Arial", 10),
    'bg': "#2196F3",
    'fg': "white",
    'bd': 1,
    'relief': "raised",
    'width': 30,
    'height': 2
}

choices = ["1. Generate Tracing Statements", "2. Create Call Graph", "3. Runtime Coverage", "4. Track Variables"]
for choice in choices:
    btn = tk.Button(button_frame, text=choice, command=lambda c=choice: handle_choice_action(c), **button_style)
    btn.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)



root.mainloop()
