import json

import netifaces
import requests
import re

from requests_toolbelt.adapters import source

url = 'http://192.168.200.2:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=%2C{}%2C{}' \
      '%40{}&user_password={}&wlan_user_ip={}&wlan_user_ipv6=&wlan_user_mac' \
      '=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.3.3&v=8263'

# Network Type
TYPE_TELECOM = 'telecom'
TYPE_MOBILE = 'mobile'

# Device Type
PC = 0
MOBILE = 1


def eth2ipv4(eth_name: str):
    # reference: https://juejin.cn/post/6844903955143770126
    avaliable_eths = netifaces.interfaces()
    if eth_name not in avaliable_eths:
        raise Exception(f"{eth_name} not in avaliable eths!")
    return netifaces.ifaddresses(eth_name)[netifaces.AF_INET][0]['addr']


def login(device_type, user, pwd, net_type, card):
    s = requests.Session()

    # Get ip address from nic
    ip = eth2ipv4(card)
    new_source = source.SourceAddressAdapter(ip)
    s.mount('http://', new_source)
    s.mount('https://', new_source)

    purl = url.format(device_type, user, net_type, pwd, ip)
    res = s.get(purl).text
    res = re.search(r'dr1003\((.*)\)', res).group(1)
    print(json.loads(res))
