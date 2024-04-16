from flask import Flask, render_template, request, jsonify
from utils.network_scaning import run_nmap_scan, debug_print_all_nmap_info

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


# Route pour l'analyse Nmap
@app.route('/nmap')
def nmap_scan():
    target = request.args.get('target')  # Obtenez la cible à partir de la requête
    print(f"Scanning target: {target}")
    if not target or target == "":
        return "Veuillez fournir une cible IP ou un nom de domaine."

    results = run_nmap_scan(target)
    debug_print_all_nmap_info(results)

    # Traitez les résultats et retournez-les
    return jsonify(results)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
#     app.run(port=8080)