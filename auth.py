#!/usr/bin/env python3

import requests
import json


def auth(adc, uname, passwd):
    url = "{}/login".format(adc)

    payload = json.dumps({
    "login": {
        "username": uname,
        "password": passwd
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.ok:
        print("[*] Connection successful!")
        res_json = json.loads(response.text)
        token = res_json['sessionid']
        return token
    else:
        print("[*] Error occured: {}".format(json.loads(response.text)["message"]))