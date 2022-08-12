#!/usr/bin/env python3

#
# Copyright (c) 2022 Clarence Subia <clarence.subia@oracle.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

# This script prints resource stats from Citrix ADC.
# Resouce including lb vserver, service, service group


import requests
import json


class adc:

    def __init__(self, nsip, user, passwd):
        self.nsip = nsip
        self.session = requests.Session()
        self.auth(self.nsip, user, passwd)


    def auth(self, nsip, user, passwd):
        url = "https://{}/nitro/v1/config/login".format(nsip)

        payload = json.dumps({
            "login": {
                "username": user,
                "password": passwd
            }
        })

        headers = {
            "Content-type": "application/json"
        }

        response = self.session.post(url, headers=headers, data=payload)
        if not response.ok:
            print("[X] An error has occured!")
        data = json.loads(response.text)["sessionid"]

        headers = {
            "Content-Type": "application/json",
            "Cookie": "NITRO_AUTH_TOKEN={}".format(data)
            }
        self.session.headers.update(headers)

    def get_route(self):
        url = "https://{}/nitro/v1/config/route".format(self.snip)
        response = self.session.get(url)
        if response.ok:
            routes = json.loads(response.text)["route"]
            print("{0:10s}{1:14s}{2:10s}{3:8s}{4:17s}".format("Network", "Netmask", "Gateway", "Route Type"))
            for route in routes:
                network = route["network"]
                netmask = route["netmask"]
                gw = route["gateway"]
                type = route["routetype"]
                print("{0:10s}{1:14s}{2:10s}{3:8s}{4:17s}".format(network, netmask, gw, type))

                        


lb = adc("192.168.100.1", "nsroot", "iamgroot")



