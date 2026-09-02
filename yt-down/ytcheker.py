import requests

url = "https://youtube.com"
try:
    response = requests.get(url, timeout=3)
    if response.status_code == 200:
        print("Website is up!")
    else:
        print(f"Website returned status code: {response.status_code}")
except requests.ConnectionError:
    print("Website is down or unreachable.")