
import json
import urllib3

from helpers import create_rule

lsrules = {
    "name": "STUN",
    "description": "STUN / WebRTC services",
    "rules": []
}

processes = [
    "/Applications/Firefox.app/Contents/MacOS/firefox",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]

for process in processes:
    rule = create_rule(
        process,
        19302,
        protocol="udp",
        dest_host="stun.cloudflare.com",
    )
    lsrules['rules'].append(rule)


hosts = [
    "stun.l.google.com",
    "stun1.l.google.com",
]

for process in processes:
    rule = create_rule(
        process,
        3478,
        protocol="udp",
        dest_host=hosts,
    )
    lsrules['rules'].append(rule)


# https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060548#h_01EEBSGCKBYVB20MCVPR78T0NN
zoom_stun_hosts = [
    "144.195.0.0/16",
    "147.124.96.0/19",
    "170.114.0.0/16",
    "173.231.92.0/24",
    "206.247.0.0/16",
]

for process in processes:
    rule = create_rule(
        process,
        3478,
        protocol="udp",
        dest_ip=zoom_stun_hosts,
        notes="Zoom",
    )
    lsrules['rules'].append(rule)


with open("rules/stun.lsrules", "w") as of:
    of.write(json.dumps(lsrules, indent=4))
