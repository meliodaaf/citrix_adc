#!/usr/bin/env python3

import requests
import json
from auth import auth


uname = "nsroot"
passwd = "adminpass"
base_path = "http://192.168.203.101/nitro/v1"


token = auth(f"{base_path}/config", uname, passwd)

session = requests.Session()
headers = {
    'Content-Type': 'application/json',
    'Cookie': f'NITRO_AUTH_TOKEN={token}'
    }  
session.headers.update(headers)
    
    
def main():
    get_all_lbs()
    

def get_all_lbs():
    # Retrieve all lb vservers and run each to the get_lb_binding() function.
    url = f"{base_path}/config/lbvserver"
    response = session.get(url)
    
    if response.ok:
        data = json.loads(response.text)
        lb_vservers = data["lbvserver"]
        
        for lb_vserver in lb_vservers:
            name = lb_vserver["name"]
            print(f"\n[*] Retrieving lb vserver bindings for {name}: ")
            get_serviceGroups(name)
            get_service(name)
            
            
def get_serviceGroups(lb):
    # Retrieve serviceGroups bound to an lb vserver.
    url = f"{base_path}/config/lbvserver_servicegroup_binding/{lb}"
    response = session.get(url)
    
    if response.ok:
        data = json.loads(response.text)
        try:
            svc_grps = data["lbvserver_servicegroup_binding"]
            
            for svc_grp in svc_grps:
                name = svc_grp["servicegroupname"]
                print(f"\nService Group {name}: ")
                get_serviceGroupBindings(name)
        except KeyError:
            svc_grps = None
            

def get_service(lb):
    # Retrieve serviceGroups bound to an lb vserver.
    url = f"{base_path}/config/lbvserver_service_binding/{lb}"
    response = session.get(url)
    
    if response.ok:
        data = json.loads(response.text)
        try:
            services = data["lbvserver_service_binding"]
            
            for service in services:
                name = service["servicename"]
                ip = service["ipv46"]
                port = service["port"]
                cur_state = service["curstate"]
                print(f"\nService: {name}")
                print(f"IP Address: {ip}")
                print(f"Port: {port}")
                print(f"Current State: {cur_state}")
                stats("service", name)
                
        except KeyError:
            service = None
            
            
def get_serviceGroupBindings(svc_grp):
    # Retrieve the servers bound to a serviceGroup
    url = f"{base_path}/config/servicegroup_binding/{svc_grp}"
    response = session.get(url)
    if response.ok:
        data = json.loads(response.text)
        svrs = data["servicegroup_binding"]
        
        for svr in svrs:
            members = svr["servicegroup_servicegroupmember_binding"]
            for member in members:
                name = member["servicegroupname"]
                ip = member["ip"]
                port = member["port"]
                state = member["svrstate"]
                print(f"\nIP Address: {ip}")
                print(f"Port: {port}")
                print(f"State: {state}")
                stats("servicegroupmember", name, ip, port)
            


def stats(resource, object, ip=None, port=None):

    if resource == "servicegroupmember":
        url = f"{base_path}/stat/{resource}/{object}?args=ip:{ip},port:{port}"
    elif resource == "service":
        url = f"{base_path}/stat/{resource}/{object}"
        
    response = requests.get(url, headers=headers)
    if response.ok:
        data = json.loads(response.text)
        members = data[resource]
        for member in members:
            t_req = member["totalrequests"]
            t_resp = member["totalresponses"]
            req_rate = member["requestsrate"]
            resp_rate = member["responsesrate"]
            current_svr_conn = member["cursrvrconnections"]
            
            print(f"Total Requests: {t_req}")
            print(f"Total Response: {t_resp}")
            print(f"Requests rate: {req_rate}")
            print(f"Response rate: {resp_rate}")
            print(f"Current server connections: {current_svr_conn}")
        
        
if __name__ == '__main__': 
    main()