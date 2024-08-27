"""
Updated GUI for software using classes

Timothy Chew
22/8/24
"""

import customtkinter as ctk
import os
import pandas as pd

from software_main import imp_fitting

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

class App(ctk.CTk):
    """
    GUI
    """
    def __init__(self):
        super().__init__()

        #creating layout frame
        self.title("File Selection")
        self.geometry("800x500")
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=60, fill='both', expand=True)

        self.titlelabel = ctk.CTkLabel(master=self.frame, text="File selection")
        self.titlelabel.pack(pady=12, padx=10)

        #read cache
        fname_list = pd.read_csv("fcache.csv", delimiter=",").values[:,1]

        #generate file selector buttons
        self.model = file_selector(self.frame, "Select impedance model", self.select_folder, fname_list[0])
        self.nyquist_bias = file_selector(self.frame, "Select impedance data file", self.select_file, fname_list[1])
        self.nyquist_nobias = file_selector(self.frame, "Select 0V bias impedance data file", self.select_file, fname_list[2])
        self.IV = file_selector(self.frame, "Select IV data file", self.select_file, fname_list[3])
        self.OCP = file_selector(self.frame, "Select OCP data file", self.select_file, fname_list[4])

        #main bit of UI
        self.mainframe = ctk.CTkFrame(self.frame)
        self.mainframe.pack(pady=10, padx=10, fill="x")

        #button to run software
        self.run = ctk.CTkButton(self.mainframe, text="Run Software", command=self.run_software)
        self.run.pack(padx=10)

        #button to check if under bias
        self.bias = False
        self.biasbutton = ctk.CTkCheckBox(self.mainframe, text="Under Bias", command=self.update_bias)
        self.biasbutton.pack(side="right", padx=10)

        #button to see if we want to run checker
        self.runchecker = False
        self.runcheckerbutton = ctk.CTkCheckBox(self.mainframe, text="Run Checker", command=self.update_runchecker)
        self.runcheckerbutton.pack(side="left", padx=10)

        #button to clear cache
        self.clearcachebutton = ctk.CTkButton(self.frame, text="Clear Cache", command=self.clear_cache)
        self.clearcachebutton.pack(side="left", padx=10, pady=10)

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

        #change label text
        if path:            
            #change to relative path
            path = os.path.relpath(path, start=os.getcwd())
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

        #change label text
        if path:
            #change to relative path
            path = os.path.relpath(path, start=os.getcwd())
            file_label.configure(text=path)
        else:
            file_label.configure(text="No file selected")
        
        file_selector.set_filename(path)

    def run_software(self):
        #checks
        if self.model.filename() == "No File Selected":
            print("No Model selected!")
        elif self.nyquist_bias.filename() == "No File Selected":
            print("No datafile selected!")
        else:
            imp_fitting(self.model.filename(), self.nyquist_bias.filename(), self.nyquist_nobias.filename(), self.IV.filename(), self.OCP.filename(),
                    bias=self.bias, run_checker=self.runchecker)
        
        df = pd.read_csv("fcache.csv", delimiter=",")

        list_to_update = [self.model.filename(), self.nyquist_bias.filename(), self.nyquist_nobias.filename(), self.IV.filename(), self.OCP.filename()]

        df['filename'] = list_to_update

        df.to_csv("fcache.csv", index=False)

    def update_bias(self):
        if self.bias:
            self.bias = False
        else:
            self.bias = True
    
    def update_runchecker(self):
        if self.runchecker:
            self.runchecker = False
        else:
            self.runchecker = True

    def clear_cache(self):
        df = pd.read_csv("fcache.csv", delimiter=",")
        null_list = ["No File Selected", "No File Selected", "No File Selected", "No File Selected", "No File Selected"]
        
        df['filename'] = null_list
        df.to_csv("fcache.csv", index=False)

class file_selector(App):
    """
    Generates a button and label for file selection
    Args:
        file_selector(function)
    """
    def __init__(self, frame, dialogue_text, file_selector, fname):
        self.file_selector = file_selector

        #value storage
        self._filename = fname

        #frame
        self.button_label_frame = ctk.CTkFrame(frame)
        self.button_label_frame.pack(pady=10, padx=10, fill="x")

        #label
        self.label = ctk.CTkLabel(self.button_label_frame, text=fname)
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