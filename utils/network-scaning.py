import nmap


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
nm = nmap.PortScanner()
scnan = nm.scan(['127.0.0.1','127.0.0.2'], '22-443')
print(scnan)