import requests
def ytcheck():


    url = "https://youtube.com"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False