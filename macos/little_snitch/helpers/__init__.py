
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

