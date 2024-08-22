"""
Generated from chat gpt
"""

import customtkinter as ctk
from tkinter import filedialog

class FileSelector(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("File Selector")
        self.geometry("400x200")

        # Create a frame for layout
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill='both', expand=True)

        # Button to open file dialog
        self.select_button = ctk.CTkButton(self.frame, text="Select File", command=self.open_file_dialog)
        self.select_button.pack(pady=10, padx=10)

        # Label to display the selected file path
        self.file_path_label = ctk.CTkLabel(self.frame, text="No file selected")
        self.file_path_label.pack(pady=10, padx=10)

    def open_file_dialog(self):
        # Open a file selection dialog and get the selected file path
        file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py")]
        )
        # Update the label with the selected file path
        if file_path:
            self.file_path_label.configure(text=f"Selected file: {file_path}")
        else:
            self.file_path_label.configure(text="No file selected")

if __name__ == "__main__":
    app = FileSelector()
    app.mainloop()
