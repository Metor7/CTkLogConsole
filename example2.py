import customtkinter
from CTkLogsConsole import CTkConsole

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()

console_frame = customtkinter.CTkFrame(root, width=520, height=320)
console_frame.pack(padx=10, pady=10)

console = CTkConsole(console_frame)
console.pack()

console.log(type='INFO', text='My info')

root.mainloop()