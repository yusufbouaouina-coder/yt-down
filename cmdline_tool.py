import yt_dlp

import os
os.system("taskkill /F /IM chrome.exe /T")
directory = os.path.dirname(os.path.abspath(__file__))
def ytcheck():
    class youtubeconnection(Exception):
        pass
    import requests
    import os
    url = "https://example.com"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            print("Website is up!")
        else:
            print(f"Website returned status code: {response.status_code}")
            raise youtubeconnection(f"youtube has responded with error code {response.status_code} ")
    except requests.ConnectionError:
        return False




a = ytcheck()

print("this tool only supports select browsers please enter wich of the following you use: \n brave, chrome, chromium, edge, firefox, opera, safari, vivaldi, whale")
browser = (input("plese enter the browser name from the above list:"))

if a == False:
   ydl_ops = {'proxy': 'socks5h://127.0.0.1:9050', 'cookiesfrombrowser': (browser,)}
   os.system(f'powershell -command & "{directory + "\\" + "tor\\tor\\tor.exe"}"')
else:
     ydl_ops = {'cookiesfrombrowser': (browser,),}   
      


def download(link):
    with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            ydl.download([link])
download("https://youtu.be/gEL2Zxzzf38?si=-BU5t5yuSJbpPRWB")