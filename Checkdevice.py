import requests
import json

#Example of request Floodlight device
#response = requests.get("http://10.2.221.172:8080/wm/topology/links/json")

response2 = requests.get("http://192.168.58.155:8080/wm/device/")
devices = response2.json()
print(devices)
#print(devices)
#print(type(devices))
#print(len(devices))
#get value để tách dict cho devices thành các dict độc lập
valuedevices = devices["devices"]
for device in valuedevices:
    mac_list = device.get('mac', [None])
    mac = mac_list[0] if mac_list else None
    ipv4_list = device.get('ipv4', [None])
    ipv4 = ipv4_list[0] if ipv4_list else None
    attachment_point = device.get('attachmentPoint', [])
    if attachment_point:
        switch_dpid = attachment_point[0].get('switch')
        port = attachment_point[0].get('port')
        print(f"Device MAC: {mac}, IPv4: {ipv4}")
        print(f"Connected to Switch DPID: {switch_dpid}, Port: {port}")

