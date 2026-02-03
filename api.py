# Importation les bibliothèques nécessaires (FASTAPI, CORS, pandas)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Autoriser les requêtes CORS depuis n'importe quelle origine
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- CHARGEMENT DES DONNÉES ---
try:
    df = pd.read_csv('data/animes_cleaned.csv')
    
    df['Ecart'] = df['Note_Meilleur_Ep'] - df['Note_Pire_Ep']
    df['Score_Regularite'] = 10 - df['Ecart']
    df['Score_Editorial'] = (0.6 * df['Note_Globale']) + (0.4 * df['Score_Regularite'])
    # On redéfinit les labels
    def definir_label(score):
        if score >= 8.5: return "💎 Chef-d'œuvre"
        elif score >= 8.0: return "✅ Très bon"
        elif score >= 7.0: return "⚠️ Bon mais risqué"
        else: return "❌ À éviter"
    
    df['Label_Editorial'] = df['Score_Editorial'].apply(definir_label)
    df['Genre_Principal'] = df['Genre_Tags'].apply(lambda x: x.split(' / ')[0] if isinstance(x, str) else "Autre")

except Exception as e:
    print(f"Erreur lors du chargement des données : {e}")

# Routes de l'API

# Point d'entrée principal
@app.get("/")
def home():
    return {"message": "Bienvenue à l'API Anime Score"}

# Obtenir la liste de tous les animes
@app.get("/animes")
def get_all_animes(genre: str = None):
    return df['Anime'].unique().tolist()

# Obtenir les détails d'un anime spécifique
@app.get("/recommend/{titre}")
def recommend(titre:str):
    if titre not in df ['Anime'].values:
        return {"error": "Anime non trouvé"}
    
    anime_info = df[df['Anime'] == titre].iloc[0]
    genre_cible = anime_info['Genre_Principal']

    recos = df[
        (df['Genre_Principal'] == genre_cible) & 
        (df['Anime'] != titre) &
        (df['Score_Editorial'] >= 7.0)
    ].sort_values(by='Score_Editorial', ascending=False).head(5)

    # Retourner les recommandations sous forme de liste de dictionnaires
    return recos[['Anime', 'Score_Editorial', 'Label_Editorial', 'Genre_Tags']].to_dict(orient='records')