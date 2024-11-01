import http.client as httplib
import json
import requests
import json
import sys
class StaticEntryPusher(object):
 
    def __init__(self, server):
        self.server = server
 
    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])
 
    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200
 
    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200
 
    def rest_call(self, data, action):
        path = '/wm/staticentrypusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        print(ret)
        conn.close()
        return ret

#nhap danh sach cac duong di, cac hop can di qua
#OK
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
    #print(danhsachswitch)
    len_path = 2 + len(danhsachswitch)
    for path in range(len_path):
        if (path == 0):
            path_dict.append({"type": "hostsrc", "host1":iphost1})
        elif (path == len_path-1):
            path_dict.append({"type": "hostdst","host2":iphost2})
        else:
            switch_num = danhsachswitch[path-1]
            print(f"sw{path}: {switch_num}")
            path_dict.append({"type":"switch", f"sw{path}":switch_num})
#path_dict la array chua dict la thanh phan trong array
    print(path_dict)
    return path_dict

#1. Lay danh sach connect cua cac device to switch trong lan dau tien - ok
def check_device_connect_first_time():
    response2 = requests.get("http://192.168.58.155:8080/wm/device/")
    list_con_devices = response2.json()
    return list_con_devices

#2. Lay danh sach link switch to switch trong lan dau tien -> ok
def check_switch_connect_first_time():
    link_response = requests.get("http://192.168.58.155:8080/wm/topology/links/json")
    list_con_switch = link_response.json()
    return list_con_switch

#3 Kiem tra ket noi port cua host va switch -> ok
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
                        #print(f"Host has ipv4: {ip1} is connect to Switch DPID: {switch_dpid} via port: {port}")
                    else:
                        continue
            else:
                continue
        else:
            continue
    return port

#4 Kiem tra cong ket noi cua switch 1 to switch 2, tra ve output cua switch 2
def check_link_switch_to_swich(switch1, switch2):
    link_response = requests.get("http://192.168.58.155:8080/wm/topology/links/json")
    list_con_switch = link_response.json()
    #print(list_con_switch)
    dst_port = None 
    for link in list_con_switch:
        if(link['src-switch'] == switch1 and link['dst-switch'] == switch2):
            #print(link)
            dst_port = link['src-port']
            break
        elif(link['src-switch'] == switch2 and link['dst-switch'] == switch1):
            #print(link)
            dst_port = link['dst-port']
            break
        else:
            continue
    return dst_port


def staticroute(path_dict, priority):
    flows = []
    len_route = len(path_dict)
    #switchnearhost1 = switchlist[0]
    #switchnearhost2 = switchlist[-1]
    #port_in_host1_to_switch = check_link_host_to_switch(iphost1,switchnearhost1)
    #port_in_host2_to_switch = check_link_host_to_switch(iphost2,switchnearhost2)
    for path in range(len_route):
        outputport_switch_to_switch_nearhost = None
        if path_dict[path]["type"] == "hostsrc":
            inputport_switch_from_host1 = check_link_host_to_switch(path_dict[path]["host1"],path_dict[path+1][f"sw{path+1}"])
            #print(inputport_switch_from_host1)
            continue
        elif path_dict[path]["type"] == "switch" and path_dict[path-1]["type"] == "hostsrc" and path_dict[path+1]["type"] == "switch":
            outputport_switch_to_switch_nearhost = check_link_switch_to_swich(path_dict[path][f"sw{path}"],path_dict[path+1][f"sw{path+1}"])
            #print(outputport_switch_to_switch_nearhost)
            actions = f"output={outputport_switch_to_switch_nearhost}"
            flow = {
                'switch':path_dict[path][f"sw{path}"],
                "name":f"flow-from-host1-to-sw{path}",
                "cookie":"0",
                "priority": priority,
                "in_port": inputport_switch_from_host1, #ket noi toi tra ve host sw1
                "active":"true",
                "actions":actions
                }
            flows.append(flow)
            #print(flows)
            continue
        elif path_dict[path]["type"] == "switch" and path_dict[path-1]["type"] == "switch" and path_dict[path+1]["type"] == "switch":
            outputport_switchin_to_switchout = check_link_switch_to_swich(path_dict[path][f"sw{path}"],path_dict[path-1][f"sw{path-1}"])
            outputport_switchout_to_switchnear = check_link_switch_to_swich(path_dict[path][f"sw{path}"],path_dict[path+1][f"sw{path+1}"])
            actions = f"output={outputport_switchout_to_switchnear}"
            flow = {
                'switch':path_dict[path][f"sw{path}"],
                "name":f"flow-from-h1-sw{path-1}-to-sw{path}",
                "cookie":"0",
                "priority": priority,
                "in_port": outputport_switchin_to_switchout, #ket noi toi tra ve host sw1
                "active":"true",
                "actions":actions
                 }
            flows.append(flow)
            #print(flows)
            continue
        elif path_dict[path]["type"] == "switch" and path_dict[path+1]["type"] == "hostdst" and path_dict[path-1]["type"] == "switch":
            outputport_switch_from_host2 = check_link_host_to_switch(path_dict[path+1]["host2"],path_dict[path][f"sw{path}"])
            #print(outputport_switch_from_host2)
            inputport_switch_to_switchnear_host = check_link_switch_to_swich(path_dict[path][f"sw{path}"],path_dict[path-1][f"sw{path-1}"])
            actions = f"output={outputport_switch_from_host2}"
            flow = {
                'switch':path_dict[path][f"sw{path}"],
                "name":f"flow-from-h1-to-h2-from-sw{path-1}-to-sw{path}",
                "cookie":"0",
                "priority": priority,
                "in_port": inputport_switch_to_switchnear_host, #ket noi toi tra ve host sw1
                "active":"true",
                "actions":actions
                 }
            flows.append(flow)
            continue
        elif path_dict[path]["type"] == "switch" and path_dict[path+1]["type"] == "hostdst" and path_dict[path-1]["type"] == "hostsrc":
            inputport_switch_from_host1 = check_link_host_to_switch(path_dict[path]["host1"],path_dict[path][f"sw{path}"])
            outputport_switch_to_host2 = check_link_host_to_switch(path_dict[path]["host2"],path_dict[path][f"sw{path}"])
            actions = f"output={outputport_switch_to_host2}"
            flow = {
                'switch':path_dict[path][f"sw{path}"],
                "name":f"flow-from-h1-to-h2-from-sw{path}",
                "cookie":"0",
                "priority": priority,
                "in_port": inputport_switch_from_host1, #ket noi toi tra ve host sw1
                "active":"true",
                "actions":actions
                 }
            flows.append(flow)
            break
        else:
            continue
    #Thuc hien route switch to switch
    #Thuc hien route switch ve va voi switch cu
    return flows

def reverse_static_route(flows, priority):
    flows_reverse = []
    for path in range(len(flows)):
        actions = f"output={flows[path]['in_port']}"
        in_port = (flows[path]['actions']).split('=')[1]
        name = 'reverse-' + flows[path]['name']
        flow = {
            'switch':flows[path]['switch'],
            "name": name,
            "cookie":"0",
            "priority": priority,
            "in_port": in_port,
            "active":"true",
            "actions":actions
        }
        flows_reverse.append(flow)
    return flows_reverse
#check_link_switch_to_swich()
#def route_dinhtuyen():

# portvao = check_link_host_to_switch("10.0.0.1","00:00:00:00:00:00:00:05")
# print(portvao)


# danhsachpatch = ["10.0.0.1","00:00:00:00:00:00:00:05", "00:00:00:00:00:00:00:02", "00:00:00:00:00:00:00:07", "10.0.0.3"]
priority = input("Nhap priority: ")
path_dict = listpath_input()
flows = staticroute(path_dict,priority)
print(flows)
flows_reverse = reverse_static_route(flows,priority)
print(flows_reverse)
#flowsfull = reverse_static_route(flows, priority)
pusher = StaticEntryPusher('192.168.58.155')
for i in range(len(flows)):
    pusher.set(flows[i])
    pusher.set(flows_reverse[i])

# url = "http://192.168.58.155:8080/wm/staticentrypusher/list/00:00:00:00:00:00:00:05/json"
# response = requests.get(url)
# if response.status_code == 200:
#     data = response.json()
#     print(data)