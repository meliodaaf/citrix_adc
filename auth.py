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
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url, headers=headers, data=payload, verify=False)
    if response.ok:
        res_json = json.loads(response.text)
        token = res_json['sessionid']
        return token