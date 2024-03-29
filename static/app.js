 document.addEventListener('DOMContentLoaded', function() {
    // Récupère le formulaire
    const form = document.getElementById('nmapForm');

    // Écoute l'événement de soumission du formulaire
    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Empêche le rechargement de la page par défaut

        // Affiche un message de chargement dans la zone des résultats
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '<p>Scan en cours...</p>';

        // Récupère les données du formulaire
        const formData = new FormData(form);

        // Envoie une requête GET à la vue Flask avec les données du formulaire
        fetch('/nmap?' + new URLSearchParams(formData))
            .then(function(response) {
                // Vérifie si la réponse est OK
                if (!response.ok) {
                    throw new Error('Erreur lors de la récupération des résultats.');
                }
                // Convertit la réponse en JSON
                return response.json();
            })
            .then(function(data) {
                // Affiche les résultats dans la zone des résultats
                const resultsDiv = document.getElementById('results');
                resultsDiv.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            })
            .catch(function(data, error) {
                // Affiche un message d'erreur en cas d'échec de la requête
                console.error('Erreur:', error);
                const resultsDiv = document.getElementById('results');
                resultsDiv.innerHTML = '<p>Erreur lors de la récupération des résultats.</p>';
            });
    });
});
