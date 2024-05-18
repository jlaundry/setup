
import json
import urllib3

from helpers import create_rule

lsrules = {
    "name": "Direct CRL and OCSP",
    "description": "Some applications don't use the built-in certificate verification, and therefore need access to CRL / OCSP domains",
    "rules": []
}

processes = [
    "\/Applications\/Firefox.app\/Contents\/MacOS\/firefox",
    "\/Applications\/VMware Fusion.app\/Contents\/MacOS\/VMware Fusion",
]

with open('crl-hosts.txt', 'r') as crlf:
    crldps = crlf.read().splitlines()

for process in processes:
    rule = create_rule(
        process,
        80,
        dest_host=crldps,
    )
    lsrules['rules'].append(rule)

with open("rules/crl.lsrules", "w") as of:
    of.write(json.dumps(lsrules, indent=4))

