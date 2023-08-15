
import json

BASE_OFFICE_RULE_IDS = (9, 39, 46, 47, 56, 69, 71, 97, 114, 147)

def get_app_config(app_name):
    with open("config.json", "r") as of:
        config = json.load(of)

    return [app for app in config['applications'] if app["name"] == app_name][0]

def create_rule(process, ports, protocol="tcp", dest_ip=None, dest_host=None, dest_domain=None, owner="me", notes=None):

    rule = {
        "action": "allow",
        "ports": ports,
        "process": process,
        "protocol": protocol,
        "owner": owner,
    }

    if notes is not None:
        rule['notes'] = notes

    if dest_ip is not None:
        if isinstance(dest_ip, list):
            dest_ip = ",".join(dest_ip)
        rule['remote-addresses'] = dest_ip
        return rule
    elif dest_host is not None:
        hosts = []
        for hostname in dest_host:
            if "*" in hostname:
                raise Exception(f"host={hostname} contains wildcard (not supported)")
            else:
                hosts.append(hostname)

        if len(hosts) == 1:
            hosts = hosts[0]

        rule['remote-hosts'] = hosts
        return rule
    elif dest_domain is not None:
        domains = []
        for domainname in dest_domain:
            if "*" in domainname:
                raise Exception(f"domain={domainname} contains wildcard (not supported)")
            else:
                domains.append(domainname)

        if len(domains) == 1:
            domains = domains[0]

        rule["remote-domains"] = domains
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
        rules.append(create_rule(
            process=process,
            dest_host=onedrive_blobs,
            ports="443",
            protocol="tcp",
        ))

    with open("office.json", "r") as of:
        msoffice_endpoints_worldwide = json.load(of)

    onedrive_rules = [x for x in msoffice_endpoints_worldwide if x['id'] in (32, 36, 69, )]
    for process in onedrive['processes']:
        for input_rule in onedrive_rules:
            print(f"Working on rule.id={input_rule['id']} process={process}")
            notes = f"https://endpoints.office.com/endpoints/worldwide rule {input_rule['id']} - {input_rule['serviceAreaDisplayName']}"
            rules += create_msendpoint_rules(input_rule, process, notes)


    output = {
        "description": "",
        "name": "Microsoft OneDrive",
        "rules": rules,
    }

    return json.dumps(output, indent=4)

def create_msendpoint_rules(input_rule, process, notes):
    rules = []

    for protocol in ("tcp", "udp"):
        if f"{protocol}Ports" in input_rule.keys():
            ports = input_rule[f"{protocol}Ports"].split(",")

            # Force remove http
            try:
                ports.remove('80')
            except ValueError:
                pass
            ports = ",".join(ports)

            if 'ips' in input_rule.keys():
                rules.append(create_rule(
                    process=process,
                    dest_ip=",".join(input_rule['ips']),
                    ports=ports,
                    protocol=protocol,
                    notes=notes,
                ))
            if 'urls' in input_rule.keys():
                domains = []
                hosts = []
                for url in input_rule['urls']:
                    if url.startswith("*."):
                        domains.append(url[2:])
                    else:
                        hosts.append(url)
                if len(domains) > 0:
                    rules.append(create_rule(
                        process=process,
                        dest_domain=domains,
                        ports=ports,
                        protocol=protocol,
                        notes=notes,
                    ))
                if len(hosts) > 0:
                    rules.append(create_rule(
                        process=process,
                        dest_host=hosts,
                        ports=ports,
                        protocol=protocol,
                        notes=notes,
                    ))

    return rules

def create_office_rules():
    rules = []

    office_apps = get_app_config("Microsoft Office")

    with open("office.json", "r") as of:
        msoffice_endpoints_worldwide = json.load(of)

    office_rules = [x for x in msoffice_endpoints_worldwide if x['id'] in BASE_OFFICE_RULE_IDS]
    for process in office_apps['processes']:
        for input_rule in office_rules:
            print(f"Working on rule.id={input_rule['id']} process={process}")
            notes = f"https://endpoints.office.com/endpoints/worldwide rule {input_rule['id']} - {input_rule['serviceAreaDisplayName']}"
            rules += create_msendpoint_rules(input_rule, process, notes)

    output = {
        "description": "",
        "name": "Microsoft Office",
        "rules": rules,
    }

    return json.dumps(output, indent=4)

def create_teams_rules():
    rules = []

    teams = get_app_config("Microsoft Teams")
    teams_helper = get_app_config("Microsoft Teams (Helper)")
    teams_ui = get_app_config("Microsoft Teams (UI)")

    # curl https://raw.githubusercontent.com/jlaundry/aadinfo/main/network/onedrive_hosts.txt > onedrive_hosts.txt
    with open("onedrive_hosts.txt", "r") as of:
        onedrive_hosts = [line.strip() for line in of.readlines()]

    for process in teams_ui['processes']:
        rules.append(create_rule(
            process=process,
            dest_host=onedrive_hosts,
            ports="443",
            protocol="tcp",
            notes=None,
        ))

    # curl https://endpoints.office.com/endpoints/worldwide?clientrequestid=7f74198b-51f7-4caf-ad3f-736180888dd7 > office.json
    with open("office.json", "r") as of:
        msoffice_endpoints_worldwide = json.load(of)

    teams_rules = [x for x in msoffice_endpoints_worldwide if x['id'] in (12, )]
    for process in teams['processes']:
        for input_rule in teams_rules:
            print(f"Working on rule.id={input_rule['id']} process={process}")
            notes = f"https://endpoints.office.com/endpoints/worldwide rule {input_rule['id']} - {input_rule['serviceAreaDisplayName']}"
            rules += create_msendpoint_rules(input_rule, process, notes)

    teams_ui_rules = [x for x in msoffice_endpoints_worldwide if x['id'] in (11, )]
    for process in teams_ui['processes']:
        for input_rule in teams_ui_rules:
            print(f"Working on rule.id={input_rule['id']} process={process}")
            notes = f"https://endpoints.office.com/endpoints/worldwide rule {input_rule['id']} - {input_rule['serviceAreaDisplayName']}"
            rules += create_msendpoint_rules(input_rule, process, notes)
            
    combined_teams_helper_rule_ids = (1, ) + BASE_OFFICE_RULE_IDS
    teams_helper_rules = [x for x in msoffice_endpoints_worldwide if x['id'] in combined_teams_helper_rule_ids]
    for process in teams_helper['processes']:
        for input_rule in teams_helper_rules:
            print(f"Working on rule.id={input_rule['id']} process={process}")
            notes = f"https://endpoints.office.com/endpoints/worldwide rule {input_rule['id']} - {input_rule['serviceAreaDisplayName']}"
            rules += create_msendpoint_rules(input_rule, process, notes)

    output = {
        "description": "",
        "name": "Microsoft Teams",
        "rules": rules,
    }

    return json.dumps(output, indent=4)

with open("rules/Microsoft Office.lsrules", "w") as of:
    of.write(create_office_rules())

with open("rules/Microsoft OneDrive.lsrules", "w") as of:
    of.write(create_onedrive_rules())

with open("rules/Microsoft Teams.lsrules", "w") as of:
    of.write(create_teams_rules())

