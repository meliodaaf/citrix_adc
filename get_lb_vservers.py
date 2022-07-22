#!/usr/bin/python3

import requests
import json
import csv
from auth import token

base_path = "https://glpdpalb001.logistics.corp/nitro/v1/config/lbvserver_service_binding"

headers = {
  'Content-Type': 'application/json',
  'Cookie': f'NITRO_AUTH_TOKEN={token}'
}

def main():
    iterate()


def iterate():
    file = open("lb_vservers.txt", "r")
    for lb in file.readlines():
        lb = lb.strip("\n")
        get_bindings(lb)


def get_bindings(lb):
    requests.packages.urllib3.disable_warnings()
    response = requests.get(f"{base_path}/{lb}", headers=headers, verify=False)

    data = json.loads(response.text)["lbvserver_service_binding"]

    for item in data:
        name = item["name"]
        service = item["servicename"]
        ip = item["ipv46"]
        port = item["port"]

        output = name, service, ip, port
        write(output)


def write(output):
    with open("lb_vserver_bindins.csv", "a") as handle:
        csv_writer = csv.writer(handle)
        
        csv_writer.writerow(output)


if __name__ == '__main__': 
    main()