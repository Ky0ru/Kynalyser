from flask import Flask, render_template, request, jsonify
from utils.network_scaning import run_nmap_scan, debug_print_all_nmap_info
from utils.dns_scaning import run_whois_scan, debug_whois_scan, run_dns_dumpster_scan, debug_dns_dumpster
from utils.search_exploit import search_exploit

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


# Route pour l'analyse Nmap
@app.route('/nmap')
def nmap_scan():
    target = request.args.get('target')  # Obtenez la cible à partir de la requête
    if not target or target == "":
        return jsonify({"error": "No target provided"})
    results = run_nmap_scan(target)
    #debug_print_all_nmap_info(results)
    return jsonify(results)

@app.route('/whois')
def whois_scan():
    target = request.args.get('target')  # Obtenez la cible à partir de la requête
    if not target or target == "":
        return jsonify({"error": "No target provided"})
    results = run_whois_scan(target)
    #debug_whois_scan(results)
    return jsonify(results)

@app.route('/dnsrecon')
def dnsrecon_scan():
    target = request.args.get('target')  # Obtenez la cible à partir de la requête
    if not target or target == "":
        return jsonify({"error": "No target provided"})
    results = run_dns_dumpster_scan(target)
    #debug_dns_dumpster(results)
    return jsonify(results)
@app.route('/sub-domains-nmap')
def sub_domains_nmap():
    target = request.args.get('target')
    if not target or target == "":
        return jsonify({"error": "No target provided"})
    results = run_nmap_scan(target)
    #debug_print_all_nmap_info(results)
    return jsonify(results)

@app.route('/search_exploit')
def search_vuln():
    service = request.args.get('service')
    version = request.args.get('version')
    if not service or service == "":
        return jsonify({"error": "No service provided"})
    if not version or version == "":
        version = ""
    results = search_exploit(service, version)
    return results

if __name__ == "__main__":
    app.run(port=8080, debug=True)
    #app.run(port=8080)