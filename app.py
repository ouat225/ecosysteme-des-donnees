import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Wyverne Dashboard", page_icon="🐉")

st.title("📊 Suivi de la Population : Wyverne")

# Récupération via l'API 
try:
    res = requests.get("http://localhost:8000/population")
    data = res.json()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Taille actuelle", f"{data['taille']:.2f}")
    col2.metric("Taux de compétition (α)", data['taux_de_competition'])
    col3.metric("Taux de croissance (r)", data['taux_de_croissance'])
except:
    st.warning("L'API Backend n'est pas encore lancée.")

# Graphique d'évolution  
st.subheader("📈 Évolution temporelle")
df = pd.read_csv("wyverne_history.csv")
st.line_chart(df.set_index('temps')['taille'])