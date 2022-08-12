#!/usr/bin/env python3


import requests
import json


class adc:

    def __init__(self, nsip, user, passwd):
        self.nsip = "http://{}".format(nsip)
        self.session = requests.Session()
        self.headers = {"Content-type": "application/json"}
        self.payload = {"login": {"username": user, "password": passwd}}
        self.auth(self.nsip)
        


    def auth(self, nsip):
        url = "{}/nitro/v1/config/login".format(nsip)

        response = self.session.post(url, headers=self.headers, json=self.payload)
        if not response.ok:
            print("[X] An error has occured!")
        token = json.loads(response.text)["sessionid"]

        self.headers["Cookie"] = "NITRO_AUTH_TOKEN={}".format(token)
        self.session.headers.update(self.headers)


    def get_route(self):
        url = "{}/nitro/v1/config/route".format(self.nsip)
        response = self.session.get(url)
        if response.ok:
            routes = json.loads(response.text)["route"]
            print("{0:15s}{1:15s}{2:17s}{3:10s}".format("Network", "Netmask", "Gateway", "Route Type"))
            for route in routes:
                network = route["network"]
                netmask = route["netmask"]
                gw = route["gateway"]
                type = route["routetype"]
                print("{0:15s}{1:15s}{2:17s}{3:10s}".format(network, netmask, gw, type))
        
                
    def get_all_lb(self):
        url = "{}/nitro/v1/config/lbvserver".format(self.nsip)
        response = self.session.get(url)
        if response.ok:
            lb_vservers = json.loads(response.text)["lbvserver"]
            print("{0:45s}{1:10s}{2:20s}{3:10s}{4:20s}{5:10}".format(
                "LB Vserver", "Current State", "IP Address", "Port", "LB Method", "Persistence"
            ))
            for lb_vserver in lb_vservers:
                name = lb_vserver["name"]
                state = lb_vserver["curstate"]
                ip = lb_vserver["ipv46"]
                port = lb_vserver["port"]
                lbmethod = lb_vserver["lbmethod"]
                persistence = lb_vserver["persistencetype"]
                print("{0:45s}{1:10s}{2:20s}{3:10s}{4:20s}{5:10s}".format(
                name, state, ip, str(port), lbmethod, persistence
            ))


lb = adc("192.168.203.100", "nsroot", "iamgroot")
lb.get_route()




