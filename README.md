# Veille Narrative en Temps Réel — Un Projet ETL Intelligent

Imaginez pouvoir capter **en temps réel** ce que des milliers de personnes pensent, ressentent ou questionnent autour d’un sujet. Imaginez transformer ce flux d’opinions en une **synthèse claire, catégorisée et exploitable**. Ce projet le rend possible.

Ce système **ETL (Extract, Transform, Load)** vous permet de surveiller une thématique choisie, d’extraire les commentaires récents d’une source dynamique en ligne, de les structurer, les analyser et de produire automatiquement des **publications synthétiques** à fort impact.

---

## Architecture du projet

Ce projet se compose de 3 modules principaux :

### 1. `1_get_website_data.py` — Extraction & Enrichissement
- Interroge une source dynamique pour obtenir des commentaires récents liés à une thématique.
- Nettoie et normalise les textes.
- Classe par catégorie sémantique, et analyse le **sentiment**.
- Stocke les données dans une base locale SQLite pour un accès rapide et structuré.

### 2. `2_dashboard.py` — Interface d’Exploration Interactive
- Interface Streamlit permettant de filtrer les commentaires par date, tonalité, ou catégorie.
- Affiche les métadonnées utiles pour analyser rapidement une conversation ou un ressenti global.
- Parfait pour **explorer le terrain** avant rédaction ou synthèse.

### 3. `3_ia_model.py` — Générateur de Contenu Narratif
- Utilise des échantillons filtrés pour créer automatiquement un **post éditorial synthétique**.
- Peut simuler un ton journalistique, éditorial, ou informatif.
- Génère un texte fluide, prêt à être partagé.

Remarque : Par souci de clarté et de respect des conditions d’utilisation des plateformes, certaines portions du code utilisent des pseudo-codes à la place d’appels directs aux sources externes.

## Technologies utilisées

- **Python** (Pandas, SQLite, Streamlit)
- **NLP** : SpaCy, TextBlob, Regex
- **Data Cleaning** : normalisation, unicodage, suppression du bruit
- **Stockage** : SQLite

---

## Points forts

- **Temps réel** : chaque relance recharge les données les plus récentes.
- **Analyse fine** : catégorisation sémantique et sentimentale.
- **Intelligence de synthèse** : génère un discours structuré à partir de bruit textuel.
- **Modulaire** : chaque script est autonome et peut s’intégrer dans un workflow plus large.

---

## Légalité et éthique

> Ce projet est fourni à titre d’exemple technique.  
> L’usage réel des données issues de plateformes publiques doit impérativement respecter :
>
> - Le cadre légal (conditions d’utilisation des plateformes, RGPD)
> - Le droit à la vie privée des individus
> - Les bonnes pratiques éthiques en matière de traitement de données textuelles

Aucune donnée sensible, personnelle ou nominative ne doit être exploitée sans consentement clair et explicite.

---

## Démarrage rapide

```bash
# Exécution des scripts
python 1_get_website_data.py  # Extraction et enrichissement
streamlit run 2_dashboard.py  # Interface de visualisation
streamlit run 3_ia_model.py  # Générateur de publication
