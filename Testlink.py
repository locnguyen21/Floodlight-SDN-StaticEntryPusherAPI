import requests
import json

#Example of request Floodlight device
#response = requests.get("http://10.2.221.172:8080/wm/topology/links/json")
#STATIC_FLOW_PUSHER_API = f'http://{CONTROLLER_IP}:8080/wm/staticentrypusher/json'

link_response = requests.get("http://192.168.58.155:8080/wm/topology/links/json")
if link_response.status_code == 200:
    links = link_response.json()
    for link in links:
        if(link['src-switch'] == '00:00:00:00:00:00:00:04'):
            print(link)
else:
    print(link_response.status_code)

# data = link_response.json()
# print(data)
# for switch in data['staticEntries']:
#     print(switch)
#     print(f"Switch ID: {switch['switch']}, Hostname: {switch['name']}")