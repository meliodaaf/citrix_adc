
# Load Balancer Vserver Stats Checker

This is a tool for retrieving stats for a load balancer vserver. It also gets all the vserver bound to it as well as their stats.



## Usage/Examples

### Python version support and modules:
```python
#!/usr/bin/env python3

import requests
import json
import sys
import argparse
import getpass
from auth import auth 
```

### Getting help
```bash
./lbstats.py --help

usage: lbstats.py [-h] -t  -u  [-v]

A tool that will generate all lb vservers and check its backend servers' status.

optional arguments:
  -h, --help        show this help message and exit
  -t , --target     Target LB Vserver (Hostname or IP address)
  -u , --username   Username for logging in.
  -v , --vserver    Check specific LB Vserver

Note: when -v/--vserver is ommited, the script will get all lb vservers.

```
```bash
./sgstats.py --help

usage: sgstats.py [-h] -t  -u  [-sg]

A tool that will generate all service groups and check its backend servers' status.

options:
  -h, --help            show this help message and exit
  -t , --target         Target Citrix ADC(hostname or IP address)
  -u , --username       Username for logging in.
  -sg , --servicegroup
                        Check specific Service Group

```
### Use case 1 - Retrieve all lb vserver stats

```bash
./lbstats.py --username nsroot --target 192.168.203.101
```

### Use case 2 - Retrieve a specific lb vserver

```bash
./lbstats.py --username nsroot --target 192.168.203.101 --vserver lb_vs_server1
```
### Use case 3 - Retrieve all service group stats

```bash
./sgstats.py --username nsroot --target 192.168.203.101
```

### Use case 2 - Retrieve a specific service group

```bash
./sgstats.py --username nsroot --target 192.168.203.101 --vserver servicegroup1
```
## API Reference

#### Login

```http
  POST https://<target lb>/nitro/v1/login
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Username` | `string` | Username |
| `Password`| `string`| Password/OTP|

#### Get item

```http
  GET https://<target lb>/nitro/v1/config/resource
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `target lb`      | `string` | Citrix ADC to be communicated |
| `resource` | string| resource to be retrieved|




## Authors

- [@clarencesubia](https://github.com/meliodaaf)

