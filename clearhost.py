import requests
import json

#Example of request Floodlight device
#response = requests.get("http://10.2.221.172:8080/wm/topology/links/json")

clear_response = requests.get("http://10.2.221.172:8080/wm/device/clear/all/json")
print(clear_response.status_code)