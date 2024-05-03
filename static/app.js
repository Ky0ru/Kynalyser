const cardsContainer = document.getElementById('cardsContainer');
const statusContainer = document.getElementById('statusContainer');
const ErrorContainer = document.getElementById('ErrorContainer');

function createNMAPCard(scan, nmap) {
    const card = document.createElement('div');
    card.innerHTML = `
        <div class="card bg-white rounded-lg shadow-md p-4">
            <h2 class="text-lg font-semibold">Nmap scan report for ${scan.hostnames.map(hostname => hostname.name)[0]} (${scan.addresses.ipv4})</h2>
            <p class="text-sm text-gray-500">Nmap command line used: ${nmap.command_line}</p>
            <p class="text-sm text-gray-500">Host is ${scan.status.state} (${nmap.scanstats.elapsed}s latency).</p>
            <p class="text-sm text-gray-500 mt-2">rDNS record for ${scan.addresses.ipv4}: ${scan.hostnames.map(hostname => hostname.name).join(', ')}</p>
            <ul class="mt-2">
                <li class="text-sm text-gray-500 font-bold">PORT STATE SERVICE VERSION</li>
                ${Object.entries(scan.tcp).map(([port, info]) => `
                <li class="text-sm text-gray-500"><span class="font-bold">${port}/tcp:</span> <span class="ml-1">${info.state}</span> <span class="ml-1">${info.name}</span> <span class="ml-1">${info.product}</span> <span class="ml-1">${info.version}</span></li>`).join('')}
            </ul>
        </div>`;
    return card;

}

document.addEventListener('DOMContentLoaded', function() {
    // Récupère le formulaire
    const form = document.getElementById('nmapForm');

    // Écoute l'événement de soumission du formulaire
    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Empêche le rechargement de la page par défaut

        statusContainer.innerHTML = '';
        ErrorContainer.innerHTML = '';

        const target = document.getElementById('target').value.trim();

         // Vérifie si l'entrée est une adresse IP valide ou un nom de domaine correct
        const isValidInput = isValidIP(target) || isValidDomain(target);

        if (!isValidInput) {
            // Affiche un message d'erreur si l'entrée n'est ni une adresse IP valide ni un nom de domaine correct
            ErrorContainer.innerHTML = '<p class="text-red-400">Invalid IP address or domain name.</p>';
            return;
        }

        // Affiche un message de chargement dans la zone des résultats
        statusContainer.innerHTML = ' <svg aria-hidden="true" class="w-12 h-12 mx-auto text-gray-200 animate-spin fill-teal-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">\n' +
            '        <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>\n' +
            '        <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>\n' +
            '    </svg>\n' +
            '    <span class="sr-only">Loading...</span> <p class="text-gray-300 mt-2 mb-2">NMAP scanning in progress...</p>' +
            '</div>';

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
                console.log(data)
                // Affiche les résultats dans la zone des résultats
                statusContainer.innerHTML = '';

                if (data.nmap && data.nmap.scaninfo && data.nmap.scaninfo.error) {
                    throw new Error(data.nmap.scaninfo.error);
                    //statusContainer.innerHTML += `<p class="text-red-400">${data.nmap.scaninfo.error.join('<br>')}</p>`;
                }
                // Crée et affiche une carte pour chaque hôte scanné
                Object.values(data.scan).forEach(hostData => {
                    const card = createNMAPCard(hostData, data.nmap);
                    cardsContainer.appendChild(card);
                });
            })
            .catch(function(error) {
                // Affiche un message d'erreur en cas d'échec de la requête
                const errorText = error.message || 'Error retrieving results.';
                console.error('Erreur:', errorText);

                const errorMessage = errorText.substring(0, errorText.indexOf("WARNING:"));
                ErrorContainer.innerHTML = `<p class="text-red-400">NMAP: ${errorMessage}</p>`;
            });

        fetch('/whois?' + new URLSearchParams(formData))
            .then(function(response) {
                // Vérifie si la réponse est OK
                if (!response.ok) {
                    throw new Error('Erreur lors de la récupération des résultats.');
                }
                // Convertit la réponse en JSON
                return response.json();
            })
            .then(function(data) {
                console.log(data)

                if (data.error) {
                    throw new Error(data.error);
                }
                // const card = createNMAPCard(whoisData, data.whois);
                // cardsContainer.appendChild(card);
            })
            .catch(function(error) {
                // Affiche un message d'erreur en cas d'échec de la requête
                const errorText = error.message || 'Error retrieving results.';
                console.error('Erreur:', errorText);

                ErrorContainer.innerHTML = `<p class="text-red-400">Whois: ${errorText}</p>`;
            });
    });

    // Fonction pour vérifier si l'entrée est une adresse IP valide
    function isValidIP(input) {
        // Expression régulière pour vérifier une adresse IP
        const ipRegex = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/;
        return ipRegex.test(input);
    }

    // Fonction pour vérifier si l'entrée est un nom de domaine correct
    function isValidDomain(input) {
        // Expression régulière pour vérifier un nom de domaine
        const domainRegex = /^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return domainRegex.test(input);
    }

});
