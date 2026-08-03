import customtkinter as ctk
import os



app = ctk.CTk()
app.geometry(800,700)
inputfeild = ctk.CTkEntry(app, placeholder_text="Enter your command here")
print
app.mainloop()
os.system("")