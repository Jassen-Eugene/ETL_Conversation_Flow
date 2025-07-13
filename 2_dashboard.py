import streamlit as st
import pandas as pd
import sqlite3
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Connexion à la base de données
conn = sqlite3.connect("data_comments.db")
cursor = conn.cursor()

# Fonction pour récupérer les données
@st.cache_data(ttl=60)
def get_data():
    query = "SELECT * FROM comments"
    df = pd.read_sql_query(query, conn)
    return df

# Fonction pour générer un nuage de mots
def generate_wordcloud(text_series, title=""):
    all_text = " ".join(text_series.dropna().tolist())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
    if title:
        st.caption(title)

# Interface Streamlit
st.set_page_config(page_title="Analyse des commentaires", layout="wide")
st.title("Analyse des données de commentaires")
st.write("Ce tableau de bord fournit une analyse en temps réel des commentaires collectés.")

# Récupération des données
data = get_data()

# Affichage du tableau brut
with st.expander("Aperçu brut des données"):
    st.dataframe(data.sort_values(by="created_utc", ascending=False), use_container_width=True)

# Statistiques générales
st.subheader("Statistiques globales")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Nombre total de commentaires", len(data))
with col2:
    st.metric("Nombre de catégories détectées", data['category'].nunique())
with col3:
    sentiment_counts = data['sentiment_label'].value_counts()
    st.metric("Commentaires positifs", sentiment_counts.get("Positif", 0))

# Répartition des sentiments
st.subheader("Répartition des sentiments")
sentiment_chart = data['sentiment_label'].value_counts().reset_index()
sentiment_chart.columns = ['Sentiment', 'Nombre']
st.bar_chart(sentiment_chart.set_index('Sentiment'))

# Répartition des catégories
st.subheader("Répartition par catégorie")
category_chart = data['category'].value_counts().head(10).reset_index()
category_chart.columns = ['Catégorie', 'Nombre']
st.bar_chart(category_chart.set_index('Catégorie'))

# Nuage de mots par catégorie
st.subheader("Nuage de mots par catégorie")
selected_category = st.selectbox("Choisir une catégorie", sorted(data['category'].dropna().unique()))
filtered = data[data['category'] == selected_category]
generate_wordcloud(filtered['body'], title=f"Nuage de mots pour la catégorie '{selected_category}'")

# Rafraîchissement automatique
st.caption("Actualisation automatique des données toutes les 60 secondes.")
