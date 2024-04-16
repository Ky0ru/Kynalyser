import nmap

# Fonction pour afficher les résultats de Nmap sous forme de tableau
def debug_print_all_nmap_info(results):
    print("Nmap scan report results:")
    for host, info in results['scan'].items():
        print(f"Host: {host}")
        print("Hostnames:")
        for hostname in info['hostnames']:
            print(f"  {hostname['name']} ({hostname['type']})")
        print(f"IP Address: {info['addresses']['ipv4']}")
        print(f"Status: {info['status']['state']} ({info['status']['reason']})")
        print("Open Ports:")
        for port, port_info in info['tcp'].items():
            print(f"  Port: {port}/tcp")
            print(f"    State: {port_info['state']}")
            print(f"    Service: {port_info['name']}")
            print(f"    Product: {port_info['product']}")
            print(f"    Version: {port_info['version']}")
            print(f"    Extra Info: {port_info['extrainfo']}")
            print(f"    Conf: {port_info['conf']}")
            print(f"    CPE: {port_info['cpe']}")

# Exemple d'utilisation de Nmap
def run_nmap_scan(target):
    nm = nmap.PortScanner()
    return nm.scan(target, "80-443")