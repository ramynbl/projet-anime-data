import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Anime Score Éditorial",
    page_icon="🎌",
    layout="wide"
)

# --- TITRE & INTRO ---
st.title("🎌 Projet : Score Éditorial Anime")
st.markdown("""
**Objectif :** Identifier les pépites cachées du catalogue grâce à la Data Science.
Ce projet calcule un **Score Éditorial** qui pénalise les animes irréguliers pour ne recommander que des valeurs sûres.
""")

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data # Garde les données en mémoire pour aller plus vite
def load_data():
    # On charge le CSV nettoyé (assure-toi que le chemin est bon)
    # Si le fichier est dans le dossier 'data', utilise 'data/animes_cleaned.csv'
    # Sinon, mets le fichier au même endroit que app.py
    df = pd.read_csv('data/animes_cleaned.csv') 
    
    # On refait le calcul du score ici (au cas où)
    df['Ecart'] = df['Note_Meilleur_Ep'] - df['Note_Pire_Ep']
    df['Score_Regularite'] = 10 - df['Ecart']
    df['Score_Editorial'] = (0.6 * df['Note_Globale']) + (0.4 * df['Score_Regularite'])
    
    # Segmentation
    def definir_label(score):
        if score >= 8.5: return "💎 Chef-d'œuvre"
        elif score >= 8.0: return "✅ Très bon"
        elif score >= 7.0: return "⚠️ Bon mais risqué"
        else: return "❌ À éviter"
    
    df['Label_Editorial'] = df['Score_Editorial'].apply(definir_label)
    
    # Extraction du genre principal pour les filtres
    df['Genre_Principal'] = df['Genre_Tags'].apply(lambda x: x.split(' / ')[0] if isinstance(x, str) else "Autre")
    
    return df

try:
    df = load_data()
    st.success("✅ Données chargées avec succès !")
except FileNotFoundError:
    st.error("❌ Fichier CSV introuvable. Vérifie qu'il est bien dans le dossier 'data/'.")
    st.stop()

# --- SIDEBAR (Barre latérale) ---
st.sidebar.header("Filtres")
genre_filter = st.sidebar.multiselect(
    "Filtrer par Genre",
    options=df['Genre_Principal'].unique(),
    default=df['Genre_Principal'].unique()[:3] # Sélectionne les 3 premiers par défaut
)

# Filtrage du dataframe
df_filtered = df[df['Genre_Principal'].isin(genre_filter)]

# --- ONGLETS (TABS) ---
tab1, tab2, tab3 = st.tabs(["📊 Analyse & KPI", "🤖 Recommandation IA", "🗺️ Vue Globale"])

# --- ONGLET 1 : ANALYSE ---
with tab1:
    st.header("Analyse de la Qualité")
    
    # KPIs (Indicateurs clés)
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre d'animes", len(df_filtered))
    col2.metric("Score Éditorial Moyen", f"{df_filtered['Score_Editorial'].mean():.2f}/10")
    col3.metric("Nb Chefs-d'œuvre", len(df_filtered[df_filtered['Label_Editorial'] == "💎 Chef-d'œuvre"]))
    
    # Graphique Scatter Plot (Plotly interactif)
    st.subheader("Relation Note Globale vs Stabilité")
    fig_scatter = px.scatter(
        df_filtered, 
        x="Note_Globale", 
        y="Score_Editorial", 
        size="Ecart", 
        color="Label_Editorial",
        hover_name="Anime",
        title="Pourquoi la moyenne ne suffit pas ? (Les points bas sont les animes instables)",
        color_discrete_map={
            "💎 Chef-d'œuvre": "#00CC96",
            "✅ Très bon": "#636EFA",
            "⚠️ Bon mais risqué": "#FFA15A",
            "❌ À éviter": "#EF553B"
        }
    )
    # Ligne de neutralité
    fig_scatter.add_shape(type="line", x0=6, y0=6, x1=10, y1=10, line=dict(color="Red", dash="dash"))
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- ONGLET 2 : RECOMMANDATION ---
with tab2:
    st.header("Moteur de Recommandation")
    st.info("Sélectionnez un anime que vous avez aimé, nous vous proposerons des titres similaires mais **plus fiables**.")
    
    # Liste déroulante pour choisir un anime
    anime_choisi = st.selectbox("Quel anime avez-vous aimé ?", df['Anime'].unique())
    
    if st.button("Lancer la recommandation"):
        # Logique de recommandation
        anime_info = df[df['Anime'] == anime_choisi].iloc[0]
        genre_cible = anime_info['Genre_Principal']
        
        # Filtrage
        recos = df[
            (df['Genre_Principal'] == genre_cible) & 
            (df['Anime'] != anime_choisi) &
            (df['Score_Editorial'] >= 7.0)
        ].sort_values(by='Score_Editorial', ascending=False).head(3)
        
        st.write(f"🔎 Puisque vous aimez **{genre_cible}**, voici le Top 3 Éditorial :")
        
        # Affichage en cartes
        for i, row in recos.iterrows():
            with st.container():
                st.subheader(f"{i+1}. {row['Anime']} {row['Label_Editorial']}")
                st.write(f"**Score :** {row['Score_Editorial']:.2f} | **Genre :** {row['Genre_Tags']}")
                st.progress(row['Score_Editorial']/10)
                st.divider()

# --- ONGLET 3 : TREEMAP ---
with tab3:
    st.header("Cartographie du Catalogue")
    fig_tree = px.treemap(
        df_filtered, 
        path=[px.Constant("Catalogue"), 'Label_Editorial', 'Genre_Principal', 'Anime'],
        values='Score_Editorial',
        color='Score_Editorial',
        color_continuous_scale='RdYlGn',
        title="Où se cachent les pépites ?"
    )
    st.plotly_chart(fig_tree, use_container_width=True)

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("Projet réalisé par [Ton Nom] avec Streamlit")