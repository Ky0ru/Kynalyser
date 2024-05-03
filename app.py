from flask import Flask, render_template, request, jsonify
from utils.network_scaning import run_nmap_scan, debug_print_all_nmap_info
from utils.dns_scaning import run_whois_scan, debug_whois_scan

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


# Route pour l'analyse Nmap
@app.route('/nmap')
def nmap_scan():
    target = request.args.get('target')  # Obtenez la cible à partir de la requête
    if not target or target == "":
        return

    results = run_nmap_scan(target)
    debug_print_all_nmap_info(results)

    # Traitez les résultats et retournez-les
    return jsonify(results)

@app.route('/whois')
def whois_scan():
    target = request.args.get('target')  # Obtenez la cible à partir de la requête
    if not target or target == "":
        return
    results = run_whois_scan(target)
    debug_whois_scan(results)

    # Traitez les résultats et retournez-les
    return jsonify(results)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
#     app.run(port=8080)