# 🎬 Projet : Score Éditorial Anime
"Comment identifier les pépites d'un catalogue sans tout regarder ?"

## 🎯 Problématique Métier
Une plateforme de streaming souhaite mettre en avant des animes de qualité pour fidéliser ses abonnés.

Le problème : Se baser uniquement sur la "Note Moyenne" (IMDb/MAL) est risqué. Un anime noté 8/10 peut être excellent tout du long, ou très inégal (épisodes géniaux mélangés à des épisodes médiocres).

La solution : Créer un Score Éditorial qui pondère la qualité globale par la régularité.

Objectif : Fournir un outil d'aide à la décision pour les curateurs (humains) de la plateforme.

## 📊 Hypothèses de Travail
H1 : La moyenne ment. Deux animes avec la même note globale (ex: 8.5) n'ont pas la même valeur. Celui qui est stable est "plus sûr" que celui qui fait le yoyo.

H2 : La régularité est un gage de qualité. Un faible écart entre le meilleur et le pire épisode indique une maîtrise de la production.

H3 : Un score composite est nécessaire. Il faut mélanger la popularité (Note Globale) et la fiabilité (Régularité).

## 🛠️ Méthodologie & Étapes du Projet
### 1. Nettoyage & Exploration (Data Cleaning)
Quoi : Correction des dates, gestion des valeurs manquantes, suppression des doublons et anomalies (ex: notes impossibles).

Pourquoi : Des données sales faussent les calculs. On ne peut pas calculer un score fiable sur des doublons ou des erreurs de saisie.

### 2. Feature Engineering (Construction du Score)
Nous avons créé de nouvelles variables pour mesurer la stabilité :

Ecart = Note_Meilleur_Ep - Note_Pire_Ep (Plus c'est grand, plus c'est risqué).

Score_Regularite = 10 - Ecart (Note sur 10 de la stabilité).

Score_Editorial = (0.6 * Note_Globale) + (0.4 * Score_Regularite).

Choix de pondération : On privilégie la qualité intrinsèque (60%) tout en pénalisant fortement l'irrégularité (40%).

### 3. Validation Statistique
Quoi : Comparaison graphique (Scatter Plot) entre la Note Globale et le Score Éditorial.

Résultat : Les animes "instables" (ex: Naruto, Black Clover) tombent dans le classement, tandis que les œuvres maîtrisées (Frieren, Vinland Saga) restent au sommet. L'hypothèse est validée.

### 4. Segmentation Métier
Pour aider la décision, nous avons classé les animes en 4 catégories claires :

💎 Chef-d'œuvre (Score ≥ 8.5)

✅ Très bon (Score 8.0 - 8.5)

⚠️ Bon mais risqué (Score 7.0 - 8.0)

❌ À éviter (Score < 7.0)

### 5. Moteur de Recommandation
Fonctionnement : Un système de filtrage qui suggère des animes du même genre, mais uniquement s'ils ont un Score Éditorial élevé.

Exemple : Si un utilisateur aime One Piece, on ne lui recommande pas juste un autre anime de pirates, mais un anime d'aventure fiable et régulier.

## 🚀 Résultats & Conclusion
Ce projet prouve qu'avec des données limitées (Notes Min/Max/Moyenne), on peut affiner considérablement la sélection éditoriale.

**Top 3 Fiables** : Frieren, Vinland Saga, Fullmetal Alchemist: Brotherhood.

**Piège évité** : Les longues séries (Shonen fleuves) sont souvent surcotées par leur moyenne globale mais sanctionnées par notre score de régularité.

**Perspectives** : Pour aller plus loin, on pourrait intégrer l'analyse de sentiment des commentaires textuels pour détecter pourquoi un épisode a été mal noté (Budget ? Scénario ? Filler ?).

*Projet réalisé dans le cadre du module Python pour la Data Science.*
