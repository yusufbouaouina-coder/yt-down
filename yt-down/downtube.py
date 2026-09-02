import customtkinter as ctk
import os
import playwright
os.system('python -m pip install --user pipx')
os.system("python -m pipx ensurepath")
os.system("pipx install customtkinter playwright")

app = ctk.CTk()
app.geometry('800x700')
inputfeild = ctk.CTkEntry(app, placeholder_text="please insert the video link or name", width=600)
inputfeild.pack()
def linkchekr():
    val = inputfeild.get()
    if "https://" in val:
        os.system(f"yt-dlp -t 'mp4' -P '%USERPROFILE%\\Downloads\\' '{val}' ")        

app.mainloop()