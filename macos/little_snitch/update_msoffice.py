
import json



def get_app_config(app_name):
    with open("config.json", "r") as of:
        config = json.load(of)

    return [app for app in config['applications'] if app["name"] == app_name][0]

def create_rule(process, ports, protocol="tcp", dest_ip=None, dest_host=None, dest_domain=None):
    if dest_ip is not None:
        rule = {
            "action": "allow",
            "ports": ports,
            "process": process,
            "protocol": protocol,
            "remote-addresses": dest_ip
        }
        return rule
    elif dest_host is not None:
        rule = {
            "action": "allow",
            "ports": ports,
            "process": process,
            "protocol": protocol,
            "remote-hosts": dest_host
        }
        return rule
    else:
        raise Exception("ip, host, or domain must be specified")

def create_onedrive_rules():
    rules = []

    # curl https://raw.githubusercontent.com/jlaundry/aadinfo/main/network/onedrive_blobs.txt > onedrive_blobs.txt
    with open("onedrive_blobs.txt", "r") as of:
        onedrive_blobs = [line.strip() for line in of.readlines()]

    onedrive = get_app_config("Microsoft OneDrive")
    for process in onedrive['processes']:
        for host in onedrive_blobs:
            rules.append(create_rule(
                process=process,
                dest_host=host,
                ports="443",
                protocol="tcp",
            ))

    output = {
        "description": "",
        "name": "Microsoft OneDrive",
        "rules": rules,
    }

    return json.dumps(output, indent=4)

def create_msendpoint_rules(input_rule, process):
    rules = []

    for protocol in ("tcp", "udp"):
        if f"{protocol}Ports" in input_rule.keys():
            if 'ips' in input_rule.keys():
                rules.append(create_rule(
                    process=process,
                    dest_ip=",".join(input_rule['ips']),
                    ports=input_rule[f"{protocol}Ports"],
                    protocol=protocol,
                ))
            if 'urls' in input_rule.keys():
                rules.append(create_rule(
                    process=process,
                    dest_host=",".join(input_rule['urls']),
                    ports=input_rule[f"{protocol}Ports"],
                    protocol=protocol,
                ))

    return rules

def create_teams_rules():
    rules = []

    teams = get_app_config("Microsoft Teams")
    teams_ui = get_app_config("Microsoft Teams (UI)")

    # curl https://raw.githubusercontent.com/jlaundry/aadinfo/main/network/onedrive_hosts.txt > onedrive_hosts.txt
    with open("onedrive_hosts.txt", "r") as of:
        onedrive_hosts = [line.strip() for line in of.readlines()]

    for process in teams_ui['processes']:
        for host in onedrive_hosts:
            rules.append(create_rule(
                process=process,
                dest_host=host,
                ports="443",
                protocol="tcp",
            ))

    # curl https://endpoints.office.com/endpoints/worldwide?clientrequestid=7f74198b-51f7-4caf-ad3f-736180888dd7 > office.json
    with open("office.json", "r") as of:
        msoffice_endpoints_worldwide = json.load(of)

    teams_ui_rules = [x for x in msoffice_endpoints_worldwide if x['id'] in (11, )]
    for process in teams_ui['processes']:
        for input_rule in teams_ui_rules:
            print(f"Working on rule.id={input_rule['id']} process={process}")
            rules += create_msendpoint_rules(input_rule, process)

    output = {
        "description": "",
        "name": "Microsoft Teams",
        "rules": rules,
    }

    return json.dumps(output, indent=4)

with open("rules/Microsoft OneDrive.lsrules", "w") as of:
    of.write(create_onedrive_rules())

with open("rules/Microsoft Teams.lsrules", "w") as of:
    of.write(create_teams_rules())

