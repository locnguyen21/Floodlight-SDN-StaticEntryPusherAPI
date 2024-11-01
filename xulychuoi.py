import sys
import requests
import json
def listpath_input():
    iphost1 = input("Nhap host nguon: ")
    iphost2 = input("Nhap host dich: ")
    print(f"Nhap danh sach cac switch se nhan cac packet tu {iphost1} sang {iphost2} (nhan 'exit' de dung lai):")
    danhsachswitch = []
    path_dict = []
    for line in sys.stdin:
        if line.strip() == 'exit':
            break
        switch = danhsachswitch.append(line.strip())
        print(f"Host nhap vao: {line.strip()}")
    print(danhsachswitch)
    len_path = 2 + len(danhsachswitch)
    #print(len_path)
    for path in range(len_path):
        if (path == 0):
            path_dict.append({"type": "hostsrc", "host1":iphost1})
        elif (path == len_path-1):
            path_dict.append({"type": "hostdst","host2":iphost2})
        else:
            switch_num = danhsachswitch[path-1]
            print(f"sw{path}: {switch_num}")
            path_dict.append({"type":"switch", f"sw{path-1}":switch_num})
#path_dict la array chua dict la thanh phan trong array
    print(path_dict)
    return path_dict
#path_dict = listpath_input()

def check_link_switch_to_swich(switch1, switch2):
    link_response = requests.get("http://192.168.58.155:8080/wm/topology/links/json")
    list_con_switch = link_response.json()
    #print(list_con_switch)
    dst_port = None 
    for link in list_con_switch:
        if(link['src-switch'] == switch1 and link['dst-switch'] == switch2):
            print(link)
            dst_port = link['src-port']
            break
        elif(link['src-switch'] == switch2 and link['dst-switch'] == switch1):
            print(link)
            dst_port = link['dst-port']
            break
        else:
            continue
    return dst_port
# dst_port = check_link_switch_to_swich("00:00:00:00:00:00:00:02", "00:00:00:00:00:00:00:05")
# print("DEST PORT")
# print(dst_port)
# dst_port = check_link_switch_to_swich("00:00:00:00:00:00:00:02", "00:00:00:00:00:00:00:07")
# print("DEST PORT")
# print(dst_port)
# listswitch = ["00:00:00:00:00:00:00:05", "00:00:00:00:00:00:00:02", "00:00:00:00:00:00:00:07"]
# switch1 = listswitch[0]
# switch2 = listswitch[1]

# def check_link_switch_to_swich(switchsrc, switchdest):
#     out_port = 0
#     link_response = requests.get("http://192.168.58.155:8080/wm/topology/links/json")
#     if link_response.status_code == 200:
#         links = link_response.json()
#         for link in links:
#             if(link['src-switch'] == switchsrc and link['dst-switch'] == switchdest):
#                 print(link)
#                 out_port = link['src-port']
#             if(link['src-switch'] == switchdest and link['dst-switch'] == switchsrc):
#                 print(link)
#                 out_port = link['dst-port']
#     else:
#         print(link_response.status_code)
#     return out_port
# out_port = check_link_switch_to_swich(switch1, switch2)
# print(out_port)

# def check_device_connect_first_time():
#     response2 = requests.get("http://192.168.58.155:8080/wm/device/")
#     list_con_devices = response2.json()
#     print(list_con_devices)
#     return list_con_devices

# check_device_connect_first_time()

def check_link_host_to_switch(ip1,switch_dpid):
    link_response = requests.get("http://192.168.58.155:8080/wm/device/")
    list_con_devices = link_response.json()
    #print(list_con_devices)
#get value để tách dict cho devices thành các dict độc lập
    valuedevices = list_con_devices["devices"]
    for device in valuedevices:
        ipv4_list = device.get('ipv4', [None])
        ipv4 = ipv4_list[0] if ipv4_list else None
        if ipv4 == ip1:
            attachment_point = device.get('attachmentPoint', [])
            if attachment_point:
                for i in range(len(attachment_point)):
                    switch_ppid_match = attachment_point[i].get('switch')
                    if switch_ppid_match == switch_dpid:
                        port = attachment_point[i].get('port')
                        print(f"Host has ipv4: {ip1} is connect to Switch DPID: {switch_dpid} via port: {port}")
                    else:
                        continue
            else:
                continue
        else:
            continue
    return port
port = check_link_host_to_switch("10.0.0.3", "00:00:00:00:00:00:00:07")
print(port)
# a = [{'switch': '00:00:00:00:00:00:00:05', 'name': 'flow-from-host1-to-sw1', 'cookie': '0', 'priority': 1234, 'in_port': '5', 'active': 'true', 'actions': 'output=2'}, {'switch': '00:00:00:00:00:00:00:02', 'name': 'flow-from-h1-sw1-to-sw2', 'cookie': '0', 'priority': 1234, 'in_port': 1, 'active': 'true', 'actions': 'output=3'}, {'switch': '00:00:00:00:00:00:00:07', 'name': 'flow-from-h1-to-h2-from-sw2-to-sw3', 'cookie': '0', 'priority': 1234, 'in_port': 2, 'active': 'true', 'actions': 'output=5'}]
# print(a)
# print((a[0]['switch']))
# a = 'flow-from-h1-to-h2-from-sw2-to-sw3'
# b = 'reverse-' + a
# print(b)