"""
GUI for software

Timothy Chew
22/8/24
"""

import customtkinter
import os

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

#setting up app window
app = customtkinter.CTk()
app.geometry("500x300")

frame = customtkinter.CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill='both', expand=True)

label = customtkinter.CTkLabel(master=frame, text="DONK")
label.pack(pady=12, padx=10)

#button to select model
def select_model():
    path = customtkinter.filedialog.askdirectory(
        initialdir = os.getcwd(), #working directory path
        title="Select impedance model folder"
        )
    
    #change to relative path
    path = os.path.relpath(path, start=os.getcwd())

    if path:
        model_path_label.configure(text=path)
    else:
        model_path_label.configure(text="No file selected")

select_model_frame = customtkinter.CTkFrame(frame)
select_model_frame.pack(pady=10, padx=10, fill='x')

select_model_button = customtkinter.CTkButton(select_model_frame, text="Select impedance model folder", command=select_model)
select_model_button.pack(side="left", padx=10)

model_path_label = customtkinter.CTkLabel(select_model_frame, text="No file selected")
model_path_label.pack(side="left", padx=10, expand=True)

#button to select bias data file
def select_data():
    path = customtkinter.filedialog.askopenfilename(
        initialdir = os.getcwd(), #working directory path
        title="Select bias impedance data",
        filetypes=[("Text Files", "*.txt")]
        )
    
    #change to relative path
    path = os.path.relpath(path, start=os.getcwd())

    if path:
        biasdata_path_label.configure(text=path)
    else:
        biasdata_path_label.configure(text="No file selected")

select_bias_frame = customtkinter.CTkFrame(frame)
select_bias_frame.pack(pady=10, padx=10, fill='x')

select_biasdata_button = customtkinter.CTkButton(select_bias_frame, text="Select bias impedance data", command=select_data)
select_biasdata_button.pack(side="left", padx=10)

biasdata_path_label = customtkinter.CTkLabel(select_bias_frame, text="No file selected")
biasdata_path_label.pack(side="left", padx=10, expand=True)

#button to select bias data file
def select_data_nobias():
    path = customtkinter.filedialog.askopenfilename(
        initialdir = os.getcwd(), #working directory path
        title="Select no bias impedance file"
        )
    
    #change to relative path
    path = os.path.relpath(path, start=os.getcwd())

    if path:
        nobiasdata_path_label.configure(text=path)
    else:
        nobiasdata_path_label.configure(text="No file selected")

select_nobias_frame = customtkinter.CTkFrame(frame)
select_nobias_frame.pack(pady=10, padx=10, fill='x')

select_nobiasdata_button = customtkinter.CTkButton(select_nobias_frame, text="Select 0V bias data folder", command=select_data_nobias)
select_nobiasdata_button.pack(side="left", padx=10)

nobiasdata_path_label = customtkinter.CTkLabel(select_nobias_frame, text="No file selected")
nobiasdata_path_label.pack(side="left", padx=10, expand=True)

#button to run the code
# run_button = customtkinter.CTkButton(frame, text="Run", command=run)
# run_button.pack(pady=10, padx=10)

app.mainloop()
