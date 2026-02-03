const API_URL = 'http://127.0.0.1:8000';

// Fonction pour charger les animes depuis l'API
async function loadAnimes() {
    try {
        const response = await fetch(`${API_URL}/animes/`);
        const animes = await response.json();

        const select = document.getElementById('animeSelect');
        select.innerHTML = '';

        animes.forEach(anime => {
            const option = document.createElement('option');
            option.value = anime;
            option.textContent = anime;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('❌ Erreur chargement animes:', error);
        document.getElementById('animeSelect').innerHTML = '<option>Erreur de chargement</option>';
    }
}

// Fonction pour obtenir les recommandations basées sur l'anime sélectionné
async function getRecommendations() {
    const titre = document.getElementById('animeSelect').value;
    const resDiv = document.getElementById('resultats');
    
    if (!titre) {
        resDiv.innerHTML = '⚠️ Veuillez sélectionner un anime.';
        return;
    }
    
    resDiv.innerHTML = '🔍 Recherche en cours...';

    try {
        const response = await fetch(`${API_URL}/recommend/${encodeURIComponent(titre)}`);
        const data = await response.json();

        resDiv.innerHTML = '';

        // Gestion des erreurs
        if (data.error) {
            resDiv.innerHTML = `<div class="card">❌ Erreur : ${data.error}</div>`;
            return;
        }

        // Aucune recommandation trouvée
        if (data.length === 0) {
            resDiv.innerHTML = '<div class="card">⚠️ Aucune recommandation trouvée pour cet anime.</div>';
            return;
        }

        // Affichage des recommandations
        data.forEach(anime => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <strong>${anime.Anime}</strong> 
                <span class="score">${anime.Score_Editorial.toFixed(2)}</span>
                <br>
                <small>${anime.Label_Editorial}</small>
                <br>
                <span style="font-size: 12px; color: #aaa;">${anime.Genre_Tags}</span>
            `;
            resDiv.appendChild(card);
        });
    } catch (error) {
        console.error('❌ Erreur récupération recommandations:', error);
        resDiv.innerHTML = '<div class="card">❌ Erreur lors de la récupération des recommandations.</div>';
    }
}

loadAnimes();