import json
import requests


url = "http://192.168.58.155:8080/wm/staticentrypusher/list/00:00:00:00:00:00:00:09/json"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print(data)