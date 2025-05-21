import streamlit as st
import pandas as pd
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide", page_title="Dashboard Feedback IA")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_excel("TestIA.xlsx", engine='openpyxl')
    df.replace("NR", pd.NA, inplace=True)
    return df

df = load_data()

# Analyse de sentiment
def get_sentiment(text):
    if pd.isna(text):
        return "Inconnu"
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positif"
    elif polarity < -0.1:
        return "Négatif"
    else:
        return "Neutre"

df["Sentiment"] = df["FeedBack"].apply(get_sentiment)

# =====================================
# 🧩 Filtres en haut
# =====================================

st.title("📊 Tableau de bord interactif des feedbacks IA")

col1, col2, col3, col4 = st.columns(4)

with col1:
    site_filter = st.selectbox("Filtrer par site", ["Tous"] + sorted(df["Emplacement"].dropna().unique().tolist()))

with col2:
    type_filter = st.selectbox("Filtrer par type de client", ["Tous"] + sorted(df["Type de Client"].dropna().unique().tolist()))

with col3:
    sentiment_filter = st.selectbox("Filtrer par sentiment", ["Tous", "Positif", "Neutre", "Négatif"])

# Application des filtres
filtered_df = df.copy()
if site_filter != "Tous":
    filtered_df = filtered_df[filtered_df["Emplacement"] == site_filter]
if type_filter != "Tous":
    filtered_df = filtered_df[filtered_df["Type de Client"] == type_filter]
if sentiment_filter != "Tous":
    filtered_df = filtered_df[filtered_df["Sentiment"] == sentiment_filter]

st.markdown("### 🎯 Résultats après filtrage :")

# =====================================
# 🔍 3 visualisations côte à côte
# =====================================

colA, colB, colC = st.columns(3)

# 1. Histogramme des sentiments
with colA:
    st.markdown("#### 📈 Distribution des sentiments")
    sentiment_counts = filtered_df["Sentiment"].value_counts()
    fig1 = plt.figure(figsize=(4, 3))
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette="Set2")
    plt.title("Répartition des sentiments")
    plt.ylabel("Nombre de feedbacks")
    plt.xlabel("Sentiment")
    st.pyplot(fig1)

# 2. WordCloud
with colB:
    st.markdown("#### ☁️ Nuage de mots")
    all_text = " ".join(filtered_df["FeedBack"].dropna().astype(str))
    if all_text:
        wordcloud = WordCloud(background_color="white", width=400, height=300).generate(all_text)
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        ax2.imshow(wordcloud, interpolation='bilinear')
        ax2.axis("off")
        st.pyplot(fig2)
    else:
        st.info("Aucun texte disponible pour le nuage de mots.")

# 3. Données résumées
with colC:
    st.markdown("#### 🧮 Statistiques")
    st.metric("Feedbacks totaux", len(filtered_df))
    st.metric("Feedbacks positifs", (filtered_df["Sentiment"] == "Positif").sum())
    st.metric("Feedbacks négatifs", (filtered_df["Sentiment"] == "Négatif").sum())
    st.metric("Feedbacks neutres", (filtered_df["Sentiment"] == "Neutre").sum())

# =====================================
# 📋 Affichage des feedbacks filtrés
# =====================================
st.markdown("### 💬 Feedbacks correspondants")
st.dataframe(filtered_df[["Emplacement", "Type de Client", "FeedBack", "Sentiment"]], use_container_width=True)
