import customtkinter
from CTkLogsConsole import CTkConsole

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry('690x320')
root.resizable(False, False)
root.title('CTkLogsConsole - Example')

console = CTkConsole(root)
console.grid(row=0, column=0, pady=10, padx=10)

control_frame = customtkinter.CTkFrame(root, width=160, height=300)
control_frame.grid(row=0, column=1, pady=10)
control_frame.grid_propagate(False)

def add_error_event():
    console.log(type='ERROR', text='Sample ERROR.')

def add_info_event():
    console.log(type='INFO', text='Sample INFO.')

def add_warning_event():
    console.log(type='WARNING', text='Sample WARNING.')

def add_debug_event():
    console.log(type='DEBUG', text='Sample DEBUG.')

def change_appearance_mode(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)
    console.update_counters() # To fix bugs

def clear():
    console.clear()
    console.log('INFO', 'Cleared logs.')

def clear_file_saved_logs():
    console.clear_file_saved_logs()
    console.log('INFO', 'Cleared logs saved in file.')

add_error_button = customtkinter.CTkButton(control_frame, text='Add error', command=add_error_event)
add_error_button.grid(row=0, column=0, padx=10, pady=(15, 0))

add_info_button = customtkinter.CTkButton(control_frame, text='Add info', command=add_info_event)
add_info_button.grid(row=1, column=0, padx=10, pady=(10, 0))

add_warning_button = customtkinter.CTkButton(control_frame, text='Add warning', command=add_warning_event)
add_warning_button.grid(row=2, column=0, padx=10, pady=(10, 0))

add_warning_button = customtkinter.CTkButton(control_frame, text='Add debug', command=add_debug_event)
add_warning_button.grid(row=3, column=0, padx=10, pady=(10, 0))

clear_button = customtkinter.CTkButton(control_frame, text='Clear', command=clear)
clear_button.grid(row=4, column=0, padx=10, pady=(10, 0))

clear_file_button = customtkinter.CTkButton(control_frame, text='Clear logs saved\nin file', command=clear_file_saved_logs)
clear_file_button.grid(row=5, column=0, padx=10, pady=(10, 0))

appearance_mode_optionemenu = customtkinter.CTkOptionMenu(control_frame, values=["Dark", "Light"], command=change_appearance_mode)
appearance_mode_optionemenu.grid(row=6, column=0, padx=10, pady=(10, 10))

root.mainloop()