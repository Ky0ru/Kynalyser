from flask import Flask, render_template, request, jsonify
import nmap

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


# Route pour l'analyse Nmap
@app.route('/nmap')
def nmap_scan():
    target = request.args.get('target')  # Obtenez la cible à partir de la requête
    if not target:
        return "Veuillez fournir une cible IP ou un nom de domaine."

    # Utilisez nmap pour effectuer un scan
    nm = nmap.PortScanner()
    nm.scan(target)

    # Traitez les résultats et retournez-les
    return jsonify(nm.all_hosts())


if __name__ == "__main__":
    app.run(port=8080, debug=True)