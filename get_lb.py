#!/usr/bin/env python3

from urllib import response
import requests
import json
from auth import auth

uname = "nsroot"
passwd = "adminpass"
base_path = "http://192.168.203.101/nitro/v1/config"

token = auth(base_path, uname, passwd)

session = requests.Session()
headers = {
    'Content-Type': 'application/json',
    'Cookie': f'NITRO_AUTH_TOKEN={token}'
    }  
session.headers.update(headers)
    
    
def main():
    get_all_lbs()
    

def get_all_lbs():
    
    url = f"{base_path}/lbvserver"
    response = session.get(url)
    if response.ok:
        data = json.loads(response.text)
        lb_vservers = data["lbvserver"]
        
        for lb in lb_vservers:
            name = lb["name"]
            print(f"\nLB Vserver {name}: ")
            get_lb_binding(name)
            
            
def get_lb_binding(lb):
    
    url = f"{base_path}/lbvserver_servicegroup_binding/{lb}"
    response = session.get(url)
    
    if response.ok:
        data = json.loads(response.text)
        svc_grps = data["lbvserver_servicegroup_binding"]
        
        for svc_grp in svc_grps:
            name = svc_grp["servicegroupname"]
            print(f"\nService Group {name}:")
            get_svc_grp_binding(name)
            
            
def get_svc_grp_binding(svc_grp):
    #
    url = f"{base_path}/servicegroup_binding/{svc_grp}"
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
                
                print(name, ip, port, state)
    
if __name__ == '__main__': 
    main()