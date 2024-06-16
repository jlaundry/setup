
import json

from helpers import create_rule

lsrules = {
    "name": "iCloud Storage",
    "description": "Storage accounts for iCloud services",
    "rules": []
}

processes = [
    "identifier.APPLE/com.apple.cloudd",
    "identifier.APPLE/com.apple.imtransferservices.IMTransferAgent",
    "identifier.APPLE/com.apple.nsurlsessiond",
]

with open('icloud-storage-hosts.txt', 'r') as crlf:
    icloud_storage_host = crlf.read().splitlines()

for process in processes:
    for protocol in ["tcp", "udp"]:
        rule = create_rule(
            process,
            443,
            protocol=protocol,
            dest_host=icloud_storage_host,
        )
        lsrules['rules'].append(rule)

with open("rules/icloud_storage.lsrules", "w") as of:
    of.write(json.dumps(lsrules, indent=4))
