# get_data_pipeline.py

import sqlite3
import time
import os
from dotenv import load_dotenv
from textblob import TextBlob
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import re

# --------- EXTRACTION ---------
# Chargement des variables d'environnement
load_dotenv()
MODEL_NAME = os.getenv("SequenceClassification_name")

# Connexion SQLite
conn = sqlite3.connect("data_comments.db")
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute('''
CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    author TEXT,
    body TEXT,
    score INTEGER,
    created_utc INTEGER,
    category TEXT,
    sentiment REAL,
    sentiment_label TEXT
)
''')
conn.commit()

# Simulateur de flux de commentaires
def extract_comments(source):
    """
    Simule ou interagit avec une API pour streamer des messages en temps réel.
    Chaque commentaire est un dictionnaire avec : id, author, body, score, created_utc
    """
    while True:
        comment = get_next_comment_from_source(source)  # À remplacer avec l'implémentation réelle
        if comment:
            yield comment
        time.sleep(1)

# --------- TRANSFORMATION ---------

# Chargement du modèle de classification
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
intent_classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

def categorize_text(text):
    text = text[:1000]
    prediction = intent_classifier(text)[0]
    label = prediction['label']
    score = prediction['score']
    return label if score >= 0.5 else "Inconnu"

def sentiment_analysis(text):
    return TextBlob(text).sentiment.polarity

def sentiment_label(polarity):
    if polarity < -0.1:
        return "Négatif"
    elif polarity <= 0.1:
        return "Neutre"
    else:
        return "Positif"

def transform_comment(comment):
    if comment["score"] < 1:
        return None

    body = re.sub(r'\s+', ' ', comment["body"]).strip()

    category = categorize_text(body)
    polarity = sentiment_analysis(body)
    sentiment_lbl = sentiment_label(polarity)

    return {
        "id": comment["id"],
        "author": comment["author"],
        "body": body,
        "score": comment["score"],
        "created_utc": comment["created_utc"],
        "category": category,
        "sentiment": polarity,
        "sentiment_label": sentiment_lbl
    }

# --------- LOAD ---------
def load_comment(comment):
    try:
        cursor.execute('''
            INSERT INTO comments (id, author, body, score, created_utc, category, sentiment, sentiment_label)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            comment["id"], comment["author"], comment["body"], comment["score"],
            comment["created_utc"], comment["category"], comment["sentiment"], comment["sentiment_label"]
        ))
        conn.commit()
        print(f'Commentaire sauvegardé : {comment["id"]} | Catégorie : {comment["category"]}')
    except sqlite3.IntegrityError:
        # Commentaire déjà enregistré
        pass

# --------- PIPELINE PRINCIPAL ---------
def etl(source):
    for raw_comment in extract_comments(source):
        transformed = transform_comment(raw_comment)
        if transformed:
            load_comment(transformed)

if __name__ == "__main__":
    print("Démarrage du flux de commentaires...")
    try:
        simulated_source = "your_data_stream_or_api"
        etl(simulated_source)
    except KeyboardInterrupt:
        print("Arrêt demandé par utilisateur")
    finally:
        conn.close()
