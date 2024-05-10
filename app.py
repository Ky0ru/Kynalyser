from flask import Flask, render_template, request, jsonify
from utils.network_scaning import run_nmap_scan, debug_print_all_nmap_info
from utils.dns_scaning import run_whois_scan, debug_whois_scan, run_dns_dumpster_scan, debug_dns_dumpster

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
    debug_print_all_nmap_info(results)
    return jsonify(results)

@app.route('/whois')
def whois_scan():
    target = request.args.get('target')  # Obtenez la cible à partir de la requête
    if not target or target == "":
        return jsonify({"error": "No target provided"})
    results = run_whois_scan(target)
    debug_whois_scan(results)
    return jsonify(results)

@app.route('/dnsrecon')
def dnsrecon_scan():
    target = request.args.get('target')  # Obtenez la cible à partir de la requête
    if not target or target == "":
        return jsonify({"error": "No target provided"})
    results = run_dns_dumpster_scan(target)
    debug_dns_dumpster(results)
    return jsonify(results)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
#     app.run(port=8080)