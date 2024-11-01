import requests
import json
def get_switches_info(controller_ip):
    url = f"http://{controller_ip}:8080/wm/core/controller/switches/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for switch in data:
            print(switch)
            switch_id = switch['switchDPID']
            #hostname = switch.get('inetAddress', {}).get('address', 'N/A')
            #print(f"Switch ID: {switch_id}, Hostname: {hostname}")
            print(f"Switch ID: {switch_id}")
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")

# controller_ip = "192.168.58.155"
# get_switches_info(controller_ip)

def push_flow(controller_ip, switch_id, flow_name, match, actions):
    url = f"http://{controller_ip}:8080/wm/staticentrypusher/json"
    flow_entry = {
        "switch": switch_id,
        "name": flow_name,
        "cookie": "0",
        "priority": "32768",
        "active": "true",
        "actions": actions,
        "match": match
    }

    response = requests.post(url, data=json.dumps(flow_entry), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        return "Flow entry successfully pushed!"
    else:
        return f"Error: {response.status_code} {response.text}"
    
controller_ip = "192.168.58.155"
switch_id = "00:00:00:00:00:00:00:01"
flow_name = "flow-mod-h1-to-h6"
match = {
    "eth_type": "0x0800",  # IPv4
    "ipv4_dst": "10.0.0.6",
    "ip_proto": "6",       # TCP
    "tcp_dst": "80",
    "in_port": "1"
}
actions = "output=6"

print(push_flow(controller_ip, switch_id, flow_name, match, actions))

