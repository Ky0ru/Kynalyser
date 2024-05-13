import nmap

# Fonction pour afficher les résultats de Nmap sous forme de tableau
def debug_print_all_nmap_info(results):
    for target, data in results.items():
        print(f"Nmap scan report for {target}:")

        nmap_info = data.get('nmap', {})
        scan_info = nmap_info.get('scaninfo', {})
        command_line = nmap_info.get('command_line', 'N/A')

        print(f"Command Line: {command_line}")

        tcp_scan_info = scan_info.get('tcp', {})
        method = tcp_scan_info.get('method', 'N/A')
        services = tcp_scan_info.get('services', 'N/A')

        print(f"Scan Info - Method: {method}, Services: {services}")

        scan_stats = nmap_info.get('scanstats', {})
        timestr = scan_stats.get('timestr', 'N/A')
        elapsed = scan_stats.get('elapsed', 'N/A')
        uphosts = scan_stats.get('uphosts', 'N/A')
        downhosts = scan_stats.get('downhosts', 'N/A')
        totalhosts = scan_stats.get('totalhosts', 'N/A')

        print(
            f"Scan Stats - Time: {timestr}, Elapsed: {elapsed}s, Up Hosts: {uphosts}, Down Hosts: {downhosts}, Total Hosts: {totalhosts}")

        scan_data = data.get('scan', {})
        for ip, info in scan_data.items():
            print(f"  IP Address: {ip}")
            hostnames = info.get('hostnames', [])
            if hostnames:
                print("  Hostnames:")
                for hostname in hostnames:
                    name = hostname.get('name', 'N/A')
                    htype = hostname.get('type', 'N/A')
                    print(f"    {name} ({htype})")
            else:
                print("  No hostnames found.")

            status = info.get('status', {})
            state = status.get('state', 'N/A')
            reason = status.get('reason', 'N/A')
            print(f"  Status: {state} ({reason})")

            ports = info.get('tcp', {})
            if ports:
                print("  Open Ports:")
                for port, port_info in ports.items():
                    service = port_info.get('name', 'N/A')
                    product = port_info.get('product', 'N/A')
                    version = port_info.get('version', 'N/A')
                    print(f"    Port: {port}/tcp")
                    print(f"      Service: {service}")
                    print(f"      Product: {product}")
                    print(f"      Version: {version}")
            else:
                print("  No open ports found.")


# Fonction pour exécuter le scan Nmap sur plusieurs cibles
def run_nmap_scan(targets):
    print(f"Running Nmap scan on {targets}...")
    nm = nmap.PortScanner()
    results = {}
    for target in targets.split(','):
        scan_result = nm.scan(target.strip(), arguments="-sV")
        results[target] = scan_result
        #print(results)
    return results

