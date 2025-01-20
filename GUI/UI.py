import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                text_box.delete(1.0, tk.END)
                text_box.insert(tk.END, content)
            update_status("File loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
            update_status("File loading failed.")
    else:
        update_status("No file selected.")

def parse_content():
    content = text_box.get(1.0, tk.END).strip()
    if not content:
        messagebox.showwarning("Warning", "No content to parse.")
        update_status("Parsing failed. No content.")
        return

    update_status("Parsing started...")
    progress_bar.start(10)  # Simulate progress
    root.after(1000, finish_parsing)  # Simulate delay (1 second)

def finish_parsing():
    progress_bar.stop()
    update_status("Parsing completed successfully.")
    messagebox.showinfo("Success", "Content parsed successfully!")

def update_status(message):
    status_label.config(text=message)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                file.write(text_box.get(1.0, tk.END).strip())
            update_status("File saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
            update_status("File saving failed.")

def main():
    global root, text_box, status_label, progress_bar

    root = tk.Tk()
    root.title("Enhanced Code Input")
    root.geometry("700x500")  # Larger size for better layout

    # Styling
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=6)
    style.configure("TLabel", font=("Arial", 12), padding=4)
    style.configure("TFrame", background="#f0f0f0")

    # Top frame
    top_frame = ttk.Frame(root, padding="10 10 10 10")
    top_frame.pack(fill=tk.X)
    ttk.Label(top_frame, text="Enhanced Code Input GUI", font=("Arial", 16, "bold")).pack(pady=5)

    # Middle frame
    middle_frame = ttk.Frame(root, padding="10 10 10 10")
    middle_frame.pack(fill=tk.BOTH, expand=True)

    text_box = tk.Text(middle_frame, wrap=tk.WORD, height=15, width=60, font=("Courier New", 12), bg="#f9f9f9")
    text_box.pack(pady=10, padx=10)

    # Bottom frame (buttons)
    bottom_frame = ttk.Frame(root, padding="10 10 10 10")
    bottom_frame.pack(fill=tk.X)

    upload_button = ttk.Button(bottom_frame, text="Upload", command=upload_file)
    upload_button.pack(side=tk.LEFT, padx=10)

    parse_button = ttk.Button(bottom_frame, text="Parse", command=parse_content)
    parse_button.pack(side=tk.LEFT, padx=10)

    save_button = ttk.Button(bottom_frame, text="Save", command=save_file)
    save_button.pack(side=tk.LEFT, padx=10)

    exit_button = ttk.Button(bottom_frame, text="Exit", command=root.destroy)
    exit_button.pack(side=tk.LEFT, padx=10)

    # Progress bar
    progress_bar = ttk.Progressbar(root, mode="indeterminate")
    progress_bar.pack(fill=tk.X, padx=20, pady=10)

    # Status bar
    status_label = ttk.Label(root, text="Ready", anchor=tk.W, background="#e0e0e0", relief=tk.SUNKEN)
    status_label.pack(fill=tk.X, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()