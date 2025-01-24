import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import generate_tracing_statements
import UI

class Controller:
    def __init__(self):
         self.ui = None

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.ui.text_box.delete(1.0, tk.END)
                    self.ui.text_box.insert(tk.END, content)
                self.update_status("File loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                self.update_status("File loading failed.")
        else:
            self.update_status("No file selected.")

    def parse_content(self):
        content = self.ui.text_box.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No content to parse.")
            self.update_status("Parsing failed. No content.")
            return

        self.update_status("Parsing started...")
        self.save("./test_code.py")
        generate_tracing_statements.main()
        self.ui.open_results_window()

    def finish_parsing(self):
        self.update_status("Parsing completed successfully.")
        messagebox.showinfo("Success", "Content parsed successfully!")

    def update_status(self, message):
        self.ui.status_label.config(text=message)

    def save_file(self):
        print(f"Root exists: {self.ui.root.winfo_exists()}")

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        print(f"Selected path: {file_path}")


    def save(self, file_path):
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.ui.text_box.get(1.0, tk.END).strip())
                self.update_status("File saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
                self.update_status("File saving failed.")


    def main(self):
        self.ui = UI.UI(self)
        self.ui.main()


if __name__ == "__main__":
    control = Controller()
    control.main()
