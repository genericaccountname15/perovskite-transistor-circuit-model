"""
Updated GUI for software using classes

Timothy Chew
22/8/24
"""

import customtkinter as ctk
import os

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

class App(ctk.CTk):
    """
    GUI
    Args:
        req_data(list of str): list of datafiles/models required
    """
    def __init__(self):
        super().__init__()

        #creating layout frame
        self.title("Banana")
        self.geometry("800x400")
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=60, fill='both', expand=True)

        self.titlelabel = ctk.CTkLabel(master=self.frame, text="DONK")
        self.titlelabel.pack(pady=12, padx=10)

        #generate buttons
        model = file_selector(self.frame, "Select impedance model", self.select_folder)
        nyquist_bias = file_selector(self.frame, "Select impedance data file", self.select_file)
        nyquist_nobias = file_selector(self.frame, "Select 0V bias impedance data file", self.select_file)
        IV_nobias = file_selector(self.frame, "Select IV data file", self.select_file)
        OCP = file_selector(self.frame, "Select OCP data file", self.select_file)

    def select_folder(self, title, path_label, file_selector):
        """
        Opens dialogue to select folder and writes filename to path_store
        Args:
            title: name of file diaglogue box
            path_label(ctk label object)
            file_selector(object): file selector object
        """
        path = ctk.filedialog.askdirectory(
            initialdir=os.getcwd(),
            title = title
        )

        #change to relative path
        path = os.path.relpath(path, start=os.getcwd())

        #change label text
        if path:
            path_label.configure(text=path)
        else:
            path_label.configure(text="No file selected")
        
        file_selector.set_filename(path)
    
    def select_file(self, title, file_label, file_selector):
        path = ctk.filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title=title,
            filetypes=[("Text Files", "*.txt")]
        )

        #change to relative path
        path = os.path.relpath(path, start=os.getcwd())

        #change label text
        if path:
            file_label.configure(text=path)
        else:
            file_label.configure(text="No file selected")
        
        file_selector.set_filename(path)

class file_selector(App):
    """
    Generates a button and label for file selection
    Args:
        file_selector(function)
    """
    def __init__(self, frame, dialogue_text, file_selector):
        self.file_selector = file_selector

        #value storage
        self._filename = None

        #frame
        self.button_label_frame = ctk.CTkFrame(frame)
        self.button_label_frame.pack(pady=10, padx=10, fill="x")

        #label
        self.label = ctk.CTkLabel(self.button_label_frame, text="No file selected")
        self.label.pack(side="right", padx=10, expand=True)

        #button
        self.button = ctk.CTkButton(self.button_label_frame, text=dialogue_text, 
                                                 command=lambda: self.file_selector(dialogue_text, self.label, self))
        self.button.pack(side="right", padx=10)

    def filename(self):
        return self._filename
    
    def set_filename(self, val):
        self._filename = val

if __name__ == "__main__":
    app = App()
    app.mainloop()