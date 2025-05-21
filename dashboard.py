import pandas as pd
import streamlit as st
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Chargement des données
df = pd.read_excel("TestIA.xlsx", engine='openpyxl')
df.replace("NR", pd.NA, inplace=True)

# Sentiment
def get_sentiment(text):
    if pd.isna(text): return "Inconnu"
    blob = TextBlob(str(text))
    p = blob.sentiment.polarity
    return "Positif" if p > 0.1 else "Négatif" if p < -0.1 else "Neutre"

df["Sentiment"] = df["FeedBack"].apply(get_sentiment)

# Affichage Streamlit
st.title("Dashboard IA - Analyse de Satisfaction Client")

# Satisfaction par site
st.subheader("Moyennes par site")
st.dataframe(df.groupby("Emplacement")[["Question 1", "Question 2", "Question 3", "Question 4", "Recommandation"]].mean())

# Type de client
st.subheader("Répartition des clients")
st.bar_chart(df["Type de Client"].value_counts())

# Consentement et Recontact
st.metric("Consentement (%)", f"{df['Consentement'].str.lower().eq('accepted').mean()*100:.1f} %")
st.metric("Souhaitez-vous être recontacté (%)", f"{df['Souhaitez-vous être recontacté?'].str.lower().eq('oui').mean()*100:.1f} %")

# Analyse de sentiments
st.subheader("Sentiment des Feedbacks")
st.dataframe(df[["Emplacement", "FeedBack", "Sentiment"]])

# Wordcloud
st.subheader("Nuage de mots - 'Un petit mot ...'")
text = " ".join(df["Un petit mot ..."].dropna())
wordcloud = WordCloud(background_color="white").generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
st.pyplot(plt)
