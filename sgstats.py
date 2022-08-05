#!/usr/bin/env python3


import requests
import json
import sys
import argparse
import getpass
from auth import auth

parser = argparse.ArgumentParser(description="A tool that will generate all service groups and check its backend servers' status.")
parser.add_argument("-t", "--target", required=True, help="Target Citrix ADC", metavar="")
parser.add_argument("-u", "--username", required=True, help="Username for logging in.", metavar="")
parser.add_argument("-sg", "--servicegroup", help="Check specific Service Group", metavar="")
args = parser.parse_args()

host = args.target
uname = args.username
passwd = getpass.getpass("Password: ")
sg = args.servicegroup

session = requests.Session()
base_path = "https://{}/nitro/v1".format(host)
session.verify=False

def main():
    print("\n[*] Connecting to {}".format(base_path))
    try:
        token = auth("{}/config".format(base_path), uname, passwd)
        headers = {
            "Content-Type": "application/json",
            "Cookie": "NITRO_AUTH_TOKEN={}".format(token)
            }
        session.headers.update(headers)
        if sg:
            service_group(sg)
        else:
            service_groups()
    except KeyboardInterrupt:
        print("[X] Quitting...")
        sys.exit()



def service_groups():
    url = "{}/config/servicegroup".format(base_path)
    response = session.get(url)
    if response.ok:
        data = json.loads(response.text)["servicegroup"]
        count = 1
        for servicegroup in data:
            name = servicegroup["servicegroupname"]
            service_type = servicegroup["servicetype"]
            state = servicegroup["servicegroupeffectivestate"]
            print("\n{})\tService Group: {} - {}".format(count, name, service_type))
            print(" \tEffective State: {}".format(state))
            service_group_binding(name)
            count += 1


def service_group(group):
    url = "{}/config/servicegroup/{}".format(base_path, group)
    response = session.get(url)
    if response.ok:
        data = json.loads(response.text)["servicegroup"]
        count = 1
        for servicegroup in data:
            name = servicegroup["servicegroupname"]
            service_type = servicegroup["servicetype"]
            state = servicegroup["servicegroupeffectivestate"]
            print("\n{})\tService Group: {} - {}".format(count, name, service_type))
            print(" \tEffective State: {}".format(state))
            service_group_binding(name)
            count += 1



def service_group_binding(service_group):
    # Retrieve the servers bound to a serviceGroup
    url = "{}/config/servicegroup_binding/{}".format(base_path, service_group)
    response = session.get(url)
    if response.ok:
        data = json.loads(response.text)["servicegroup_binding"]
        for server in data:
            try:
                members = server["servicegroup_servicegroupmember_binding"]
                count = 1
                for member in members:
                    name = member["servicegroupname"]
                    ip = member["ip"]
                    port = member["port"]
                    state = member["svrstate"]
                    servername = member["servername"]
                    print("\n\t{})\t{}:{} State: {} Server Name: {}".format(count, ip, port, state, servername))
                    stats(name, servername, port)
                    count +=1 
            except KeyError:
                members = None




def stats(object, ip=None, port=None):
    url = "{}/stat/servicegroupmember/{}?args=servername:{},port:{}".format(base_path, object, ip, port)
    response = session.get(url)
    if response.ok:
        data = json.loads(response.text)["servicegroupmember"]
        for member in data:
            t_req = member["totalrequests"]
            t_resp = member["totalresponses"]
            current_svr_conn = member["cursrvrconnections"]
            print("\t\tTotal Requests: {}".format(t_req))
            print("\t\tTotal Response: {}".format(t_resp))
            print("\t\tCurrent server connections: {}".format(current_svr_conn))



if __name__ == '__main__': 
    main()