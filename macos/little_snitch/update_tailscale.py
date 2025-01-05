
import json
import urllib3

from helpers import create_rule


if __name__ == '__main__':
    rules = []

    process = "identifier.W5364U7YZB/io.tailscale.ipn.macos.network-extension"

    rules += [
        create_rule(
            process=process,
            ports=[443],
            protocol="tcp",
            dest_host=[
                "login.tailscale.com",
                "controlplane.tailscale.com",
                "log.tailscale.com",
                "log.tailscale.io",
            ],
            owner=None,
            notes="Tailscale coordination servers",
        ),
    ]

    url = "https://login.tailscale.com/derpmap/default"
    resp = urllib3.request("GET", url)

    if resp.status != 200:
        raise Exception(f"GET {url} returned {resp.status}: {resp.data}")

    derpmap = resp.json()

    for region_id in derpmap['Regions'].keys():
        region = derpmap['Regions'][region_id]
        region_code = region['RegionCode']
        dest_ips = []
        dest_hostnames = []
        notes = f"DERP {region_code} ({region_id})"

        for node in region['Nodes']:
            dest_ips += [node['IPv4'], node['IPv6']]
            dest_hostnames += [node['HostName']]
    
        rules += [
            create_rule(
                process=process,
                ports=[80, 443],
                protocol="tcp",
                dest_ip=sorted(dest_ips),
                owner=None,
                notes=notes,
            ),
            create_rule(
                process=process,
                ports=[41641],
                protocol="udp",
                dest_ip=sorted(dest_ips),
                owner=None,
                notes=notes,
            ),
            create_rule(
                process=process,
                ports=[80, 443],
                protocol="tcp",
                dest_host=sorted(dest_hostnames),
                owner=None,
                notes=notes,
            ),
        ]

    lsrules = {
        "name": "Tailscale",
        "description": "Tailscale",
        "rules": rules,
    }

    with open("rules/Tailscale.lsrues", "w") as of: 
        json.dump(lsrules, of, indent=4)
