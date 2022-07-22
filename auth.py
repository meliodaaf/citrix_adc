import requests
import json


def auth(adc, uname, passwd):
    url = f"{adc}/login"

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
    res_json = json.loads(response.text)
    token = res_json['sessionid']
    return token