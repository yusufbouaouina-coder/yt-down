import customtkinter as ctk
import yt_dlp_ejs as yde
from ytcheker import ytcheck
import yt_dlp
import os
import signal
import sys
import wgconfig

directory = os.path.dirname(os.path.abspath(__file__))
confgenpath = os.path.join(directory, "tools", "proton-conf", "proton-confgen.exe")
wgconfpath = os.path.join(directory, "tools", "proton-conf", "protonvpn.conf")
wpconfpath = os.path.join(directory, "tools", "wireproxy", "wireproxy.conf")
wppath = os.path.join(directory, "tools", "wireproxy", "wireproxy.exe")

def pubkey():
    config_path = wgconfpath

    # Load the configuration file
    wc = wgconfig.WGConfig(config_path)
    wc.read_file()

    # Retrieve interface data which contains the PrivateKey
    interface_data = wc.get_interface()
    private_key = interface_data.get("PrivateKey")
    public_key = wc.get_peers()

# ---- state ----
browser = 'chrome'   # sensible default so cookiesfrombrowser is never empty/invalid
vpn_manip = None      # will hold the wireproxy process handle once VPN is started
output_folder = os.path.expandvars("%USERPROFILE%\\Downloads")  # actually expand the env var






def resource_path(relative_path):
    """Get path to bundled files, works normally and inside PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)





def get_ydl_opts():
    """Build ydl_opts fresh each time, so it always reflects the current browser choice."""
    return {
        "cookiesfrombrowser": ("chrome",),
        'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'ffmpeg_location': resource_path('ffmpeg/bin'),
        'js_runtimes': {
            'deno': {
                'path': resource_path('deno/deno.exe')
            }
        }}





app = ctk.CTk()
app.geometry("900x900")


def browserset(name):
    global browser
    browser = name


def signinwind():
    win = ctk.CTkToplevel(app)
    win.geometry('600x200')

    label = ctk.CTkLabel(
        win,
        text='please ensure you have a protonvpn account if not head to \n www.protonvpn.com and make yourself one'
    )
    label.pack(pady=10)

    username_entry = ctk.CTkEntry(win, placeholder_text="email")
    username_entry.pack(pady=10)

    passw_entry = ctk.CTkEntry(win, placeholder_text="password", show="*")
    passw_entry.pack(pady=10)


#    submit = ctk.CTkButton(
#        win, width=125, height=20, text='start vpn',
#        command=lambda: vpn_stat(username_entry.get(), passw_entry.get())
#    )
#    submit.pack(pady=10)


def browsersel():
    global browsersele
    browsersele = ctk.CTkToplevel(app)
    browsersele.geometry('300x600')

    chrome = ctk.CTkButton(browsersele, text='select chrome', command=lambda: browserset('chrome'))
    chrome.pack(pady=10)
    brave = ctk.CTkButton(browsersele, text='select brave', command=lambda: browserset('brave'))
    brave.pack(pady=10)
    edge = ctk.CTkButton(browsersele, text='select edge', command=lambda: browserset('msedge'))
    edge.pack(pady=10)
    firefox = ctk.CTkButton(browsersele, text='select firefox', command=lambda: browserset('firefox'))
    firefox.pack(pady=10)
    opera = ctk.CTkButton(browsersele, text='select opera', command=lambda: browserset('opera'))
    opera.pack(pady=10)

def quitme():
    #os.system('taskkill /im wireproxy.exe /F')
    os.kill(os.getpid(), signal.SIGILL)
def download():
    with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
        os.system(f'taskkill /im {browser}.exe /F')
        ydl.download([inputf.get()])
        os.system(r"start %USERPROFILE%\AppData\Local\Google\Chrome\Application\chrome.exe")


def ydltest():
    with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
        vindinf = ydl.extract_info('http://youtube.com/watch?v=KctNIihCrhQ&vl=en', download=False)
        print(vindinf['title'])


signinbutt = ctk.CTkButton(
    app, width=60, height=10, command=signinwind,
    text='unable to connect to youtube \n please press here to sign  into protonvpn'
)
#if yt_reach is False:
    #signinbutt.pack()

inputf = ctk.CTkEntry(app, width=400, placeholder_text='link to youtube video')

browserbutt = ctk.CTkButton(app, width=60, height=40, text='set/change main browser', command=browsersel)
browserbutt.pack()

downloadbutt = ctk.CTkButton(app, width=60, height=40, text='download', command=download)

quitbutt = ctk.CTkButton(app, text='quit',command=quitme)

inputf.pack(pady=30)
downloadbutt.pack(pady=10)
quitbutt.pack(pady = 10)
app.mainloop()