import customtkinter as ctk
import os



app = ctk.CTk()
app.geometry(800,700)
inputfeild = ctk.CTkEntry(app, placeholder_text="please insert the video link or name")
input.pack()
def linkchekr():
    val = inputfeild.get()
    if "https://" is val:
        os.system("")        

app.mainloop()