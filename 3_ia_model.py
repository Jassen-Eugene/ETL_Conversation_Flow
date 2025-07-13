
import streamlit as st
import sqlite3
import pandas as pd
import random
import textwrap

# Connexion à la base de données
conn = sqlite3.connect("data_comments.db")

# Fonction pour charger les données
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_sql_query("SELECT * FROM comments", conn)
    return df

# Fonction pour générer un texte de publication
def generate_post(category, sentiment_label, nb_comments, df):
    filtered = df.copy()
    if category != "Toutes":
        filtered = filtered[filtered["category"] == category]
    if sentiment_label != "Tous":
        filtered = filtered[filtered["sentiment_label"] == sentiment_label]
    
    if filtered.empty:
        return "Aucun commentaire ne correspond à ces critères."

    selected_comments = filtered["body"].dropna().tolist()
    random.shuffle(selected_comments)
    chosen = selected_comments[:nb_comments]
    
    post = "\n\n".join(f"- {textwrap.fill(comment.strip(), width=100)}" for comment in chosen)
    return post

# Interface Streamlit
st.set_page_config(page_title="Générateur de publication", layout="centered")
st.title("Générateur de publication à partir des commentaires")
st.markdown("Sélectionnez des critères pour générer une publication textuelle à partir des commentaires collectés.")

# Chargement des données
df = load_data()

# Sélecteurs
col1, col2 = st.columns(2)
with col1:
    categories = ["Toutes"] + sorted(df["category"].dropna().unique().tolist())
    selected_category = st.selectbox("Catégorie", categories)

with col2:
    sentiments = ["Tous", "Positif", "Neutre", "Négatif"]
    selected_sentiment = st.selectbox("Filtrer par sentiment", sentiments)

nb_comments = st.slider("Nombre de commentaires à inclure", 1, 20, 5)

# Génération
if st.button("Générer la publication"):
    post = generate_post(selected_category, selected_sentiment, nb_comments, df)
    st.subheader("Publication générée :")
    st.code(post, language="markdown")

# Astuce
st.info("Astuce : utilisez cette génération pour alimenter des publications, résumés, ou synthèses de tendance.")
