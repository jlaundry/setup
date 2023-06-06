
import ipaddress
import json


def normalize_ipaddr(address:str) -> str:
    if "-" in address:
        (start, end) = address.split("-", 1)
        ranges = [ipaddr for ipaddr in ipaddress.summarize_address_range(ipaddress.ip_address(start), ipaddress.ip_address(end))]
        return str(ranges[0])
    elif "*" in address:
        #2600:1000:0:*:*:*:*:*
        return address
        (start, end) = address.split("*", 1)
        start += ":"
    else:
        return str(ipaddress.ip_address(address))


def output_rule(process, dest, ports=None, protocol=None):
    out = f"{process}\t"

    if protocol is not None:
        out += f"{protocol}://"

    out += dest

    if ports is not None:
        out += f":{ports}"

    print(out)
    return out


with open('backup.xpl', 'r') as of:
    backup_data = json.load(of)

rule_i = -1
for rule in backup_data['rules']:
    rule_i += 1
    # {
    #   "action" : "allow",
    #   "approved" : false,
    #   "creationDate" : "2023-04-08T23:52:13Z",
    #   "factoryHelpText" : "#generated\naction: allow\ndate: 702690733.973182\ndirection: outgoing\norigin: alert\npeer: app-updates.agilebits.com\nport: 443\nprocessPath: /Applications/1Password.app/Contents/MacOS/1Password\nprotocol: 6\n",
    #   "modificationDate" : "2023-04-08T23:52:13Z",
    #   "origin" : "alert",
    #   "ports" : "443",
    #   "process" : "/Applications/1Password.app/Contents/MacOS/1Password",
    #   "protocol" : "tcp",
    #   "remote-hosts" : "app-updates.agilebits.com",
    #   "uid" : 501
    # },

    if rule['action'] != "allow":
        continue

    if rule['origin'] in ['factory']:
        continue

    process = rule['process']

    protocol = None
    if 'protocol' in rule:
        protocol = rule['protocol']

    ports = None
    if 'ports' in rule:
        ports = rule['ports']

    if 'remote' in rule:
        if rule['remote'] == "any":
            dest = "*"
            output_rule(process, dest, ports, protocol)
    elif 'remote-domains' in rule:
        if isinstance(rule['remote-domains'], str):
            domain = rule['remote-domains']
            dest = f"*.{domain.strip()}"
            output_rule(process, dest, ports, protocol)
        elif isinstance(rule['remote-domains'], list):
            for domain in rule['remote-domains']:
                dest = f"*.{domain.strip()}"
                output_rule(process, dest, ports, protocol)
    elif 'remote-addresses' in rule:
        for address in rule['remote-addresses'].split(","):
            dest = normalize_ipaddr(address.strip())
            output_rule(process, dest, ports, protocol)
    elif 'remote-hosts' in rule:
        for host in rule['remote-hosts'].split(","):
            dest = host.strip()
            output_rule(process, dest, ports, protocol)
    else:
        raise Exception(f"Rule was missed: {rule}")