#!/usr/bin/env python3


import requests
import json
import sys
import argparse
import getpass
from auth import auth

parser = argparse.ArgumentParser(description="A tool that will generate all lb vservers and check its backend servers' status.")
parser.add_argument("-t", "--target", required=True, help="Target LB Vserver", metavar="")
parser.add_argument("-u", "--username", required=True, help="Username for logging in.", metavar="")
parser.add_argument("-v", "--vserver", help="Check specific LB Vserver", metavar="")
args = parser.parse_args()

host = args.target
uname = args.username
passwd = getpass.getpass("Password: ")
vserver = args.vserver

session = requests.Session()
base_path = "https://{}/nitro/v1".format(host)
session.verify=False

def main():
    # Main function to execute script
    print("\n[*] Connecting to {}".format(base_path))
    try:
        token = auth("{}/config".format(base_path), uname, passwd)
        headers = {
            "Content-Type": "application/json",
            "Cookie": "NITRO_AUTH_TOKEN={}".format(token)
            }
        session.headers.update(headers)
        check_ha_node()
        get_route()
        if vserver:
            get_lb(vserver)
        else:
            get_all_lbs()
    except KeyboardInterrupt:
        print("[X] Quitting...")
        sys.exit()


def get_route():
    url = "{}/config/route".format(base_path)
    response = session.get(url)
    if response.ok:
        print("\n[*] Route Information: ")
        data = json.loads(response.text)
        route = data["route"]
        for net in route:
            network = net["network"]
            netmask = net["netmask"]
            gw = net["gateway"]
            type = net["routetype"]
            print("\nNetwork: {}".format(network))
            print("Netmask: {}".format(netmask))
            print("Gateway: {}".format(gw))
            print("Route Type: {}".format(type))

def check_ha_node():
    url = "{}/config/hanode".format(base_path)
    response = session.get(url)
    if response.ok:
        print("\n[*] HA Nodes Information: ")
        data = json.loads(response.text)
        hanode = data["hanode"]
        for ha in hanode:
            ip = ha["ipaddress"]
            state = ha["state"]
            status = ha["hastatus"]
            print("\nIP Address: {}".format(ip))
            print("State: {}".format(state))
            print("Status: {}".format(status))


def get_lb(vserver):
    url = "{}/config/lbvserver/{}".format(base_path, vserver)
    response = session.get(url)
    if response.ok:
        data = json.loads(response.text)
        lb_vservers = data["lbvserver"]
        for lb_vserver in lb_vservers:
            name = lb_vserver["name"]
            state = lb_vserver["curstate"]
            ip = lb_vserver["ipv46"]
            port = lb_vserver["port"]
            lbmethod = lb_vserver["lbmethod"]
            blbmethod = lb_vserver["backuplbmethod"]
            persistence = lb_vserver["persistencetype"]
            print("\n[*] LB Vserver {}:".format(name))
            print("IP Address: {}".format(ip))
            print("Port: {}".format(port))
            print("State {}".format(state))
            print("Configured Method: {}, BackupMethod: {}".format(lbmethod, blbmethod))
            print("Persistence Type: {}".format(persistence))
            stats("lbvserver", name)
            get_serviceGroups(name)
            get_service(name)


def get_all_lbs():
    # Retrieve all lb vservers and run each to the get_lb_binding() function.
    url = "{}/config/lbvserver".format(base_path)
    response = session.get(url)

    if response.ok:
        data = json.loads(response.text)
        lb_vservers = data["lbvserver"]
        for lb_vserver in lb_vservers:
            name = lb_vserver["name"]
            state = lb_vserver["curstate"]
            ip = lb_vserver["ipv46"]
            port = lb_vserver["port"]
            lbmethod = lb_vserver["lbmethod"]
            blbmethod = lb_vserver["backuplbmethod"]
            persistence = lb_vserver["persistencetype"]
            print("\n[*] LB Vserver {}:".format(name))
            print("IP Address: {}".format(ip))
            print("Port: {}".format(port))
            print("State {}".format(state))
            print("Configured Method: {}, BackupMethod: {}".format(lbmethod, blbmethod))
            print("Persistence Type: {}".format(persistence))
            stats("lbvserver", name)
            get_serviceGroups(name)
            get_service(name)


def get_serviceGroups(lb):
    # Retrieve serviceGroups bound to an lb vserver.
    url = "{}/config/lbvserver_servicegroup_binding/{}".format(base_path, lb)
    response = session.get(url)

    if response.ok:
        data = json.loads(response.text)
        try:
            svc_grps = data["lbvserver_servicegroup_binding"]

            for svc_grp in svc_grps:
                name = svc_grp["servicegroupname"]
                print("\nService Group {}: ".format(name))
                get_serviceGroupBindings(name)
        except KeyError:
            svc_grps = None


def get_service(lb):
    # Retrieve serviceGroups bound to an lb vserver.
    url = "{}/config/lbvserver_service_binding/{}".format(base_path, lb)
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
                print("\nService: {}".format(name))
                print("IP Address: {}".format(ip))
                print("Port: {}".format(port))
                print("Current State: {}".format(cur_state))
                stats("service", name)

        except KeyError:
            service = None


def get_serviceGroupBindings(svc_grp):
    # Retrieve the servers bound to a serviceGroup
    url = "{}/config/servicegroup_binding/{}".format(base_path, svc_grp)
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
                servername = member["servername"]
                print("\nServer Name: {}".format(servername))
                print("IP Address: {}".format(ip))
                print("Port: {}".format(port))
                print("State: {}".format(state))
                stats("servicegroupmember", name, servername, port)



def stats(resource, object, ip=None, port=None):

    if resource == "servicegroupmember":
        url = "{}/stat/{}/{}?args=servername:{},port:{}".format(base_path, resource, object, ip, port)
    elif resource == "service":
        url = "{}/stat/{}/{}".format(base_path, resource, object)
    elif resource == "lbvserver":
        url = "{}/stat/{}/{}".format(base_path, resource, object)


    response = session.get(url)
    if response.ok:
        data = json.loads(response.text)
        members = data[resource]
        for member in members:
            t_req = member["totalrequests"]
            t_resp = member["totalresponses"]
            current_svr_conn = member["cursrvrconnections"]
            print("Total Requests: {}".format(t_req))
            print("Total Response: {}".format(t_resp))
            print("Current server connections: {}".format(current_svr_conn))


if __name__ == '__main__':
    main()