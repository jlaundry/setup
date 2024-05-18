
import json
import urllib3

from helpers import create_rule

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


RULESET_CACHE = {}


def get_ruleset(url:str):
    if url not in RULESET_CACHE.keys():
        print(f"Downloading {url} into the cache")
        resp = urllib3.request("GET", url)

        if resp.status != 200:
            raise Exception(f"GET {url} returned {resp.status}: {resp.data}")

        RULESET_CACHE[url] = resp.json()

    return RULESET_CACHE[url]


def create_app_rules(app_config:dict):
    rules = []

    for rule_config in app_config['rules']:
        ruleset = get_ruleset(rule_config['url'])
        filtered_ruleset = [x for x in ruleset if x['id'] in rule_config['rule_ids']]

        if "processes" in rule_config.keys():
            processes = rule_config['processes']
        else:
            processes = app_config['processes']

        for process in processes:
            for input_rule in filtered_ruleset:
                print(f"Working on rule.id={input_rule['id']} process={process}")
                notes = f"rule {input_rule['id']} - {input_rule['serviceAreaDisplayName']}"
                rules += create_msendpoint_rules(input_rule, process, notes)
    
    return rules


if __name__ == '__main__':

    with open("config.json", "r") as of:
        config = json.load(of)

        for app in config["applications"]:
            print(f"Working on {app['name']}")
            if "filename" in app.keys():
                with open(app['filename'], "w") as of:
                    lsrules = {
                        "name": app['name'],
                        "description": "",
                        "rules": create_app_rules(app)
                    }
                    of.write(json.dumps(lsrules, indent=4))
            else:
                print(f"...filename not set, skipping")
