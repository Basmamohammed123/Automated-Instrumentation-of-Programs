import tkinter as tk
from tkinter import filedialog

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, content)

def parse_content():
    # Placeholder function for now
    content = text_box.get(1.0, tk.END).strip()
    if content:
        print("Parsing content:")
        print(content)
    else:
        print("No content to parse.")

def main():
    global text_box  # used in upload_file()

    root = tk.Tk()
    root.title("Code Input")

    tk.Label(root, text="Enter code as text or upload a file:").pack(pady=10)

    text_box = tk.Text(root, wrap=tk.WORD, height=15, width=50)
    text_box.pack(pady=10)

    upload_button = tk.Button(root, text="Upload from Local PC", command=upload_file)
    upload_button.pack(pady=5)

    parse_button = tk.Button(root, text="Parse", command=parse_content)
    parse_button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()