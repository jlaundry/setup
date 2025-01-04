
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
        for node in region['Nodes']:
            node_name = node['Name']
            ports = [80, 443] if node['CanPort80'] else [443]
            notes = f"DERP {region_code}-{node_name}"
            rules += [
                create_rule(
                    process=process,
                    ports=ports,
                    protocol="tcp",
                    dest_ip=[node['IPv4'], node['IPv6']],
                    owner=None,
                    notes=notes,
                ),
                create_rule(
                    process=process,
                    ports=ports,
                    protocol="tcp",
                    dest_host=[node['HostName']],
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
