import streamlit as st
import pandas as pd
import time
import requests
import os

st.set_page_config(page_title="Wyverne Real-Time", layout="wide")

st.title("🐉 Wyverne vs Dragon : Suivi Temps Réel")

# Configuration API interne (Port 16083)
API_URL = os.getenv("API_URL", "http://api:8000/population")

# Initialisation de l'historique dans la session Streamlit
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["temps", "Wyverne", "Dragon (Adverse)"])

# Zone d'affichage des indicateurs (Placeholders)
col1, col2, col3 = st.columns(3)
metric_taille = col1.empty()
metric_adv = col2.empty()
metric_temps = col3.empty()

st.divider()
st.subheader("📈 Évolution de la Confrontation")
chart_placeholder = st.empty()

# Boucle de rafraîchissement automatique
# Cette boucle tourne indéfiniment tant que la page est ouverte
while True:
    try:
        # 1. Appel à l'API (ce qui déclenche le calcul de l'étape suivante)
        response = requests.get(API_URL)
        data = response.json()
        
        # 2. Mise à jour des métriques
        metric_taille.metric("Population Wyverne", f"{data['taille']:.2f}")
        metric_adv.metric("Adversaire (Dragon)", f"{data['population_adverse_nj']:.2f}")
        metric_temps.metric("Temps Simulation", f"t = {data['temps']}")

        # 3. Mise à jour de l'historique
        new_row = pd.DataFrame({
            "temps": [data["temps"]],
            "Wyverne": [data["taille"]],
            "Dragon (Adverse)": [data["population_adverse_nj"]]
        })
        
        # Concaténation propre pour éviter les warnings pandas
        if st.session_state.history.empty:
             st.session_state.history = new_row
        else:
             st.session_state.history = pd.concat([st.session_state.history, new_row], ignore_index=True)

        # 4. Affichage du graphique mis à jour
        with chart_placeholder:
            # On affiche les deux courbes pour voir la guerre
            st.line_chart(st.session_state.history.set_index("temps"))

        # 5. Attente de 5 secondes (Consigne transcription)
        time.sleep(5)
        
    except Exception as e:
        st.error(f"Erreur de connexion à l'API : {e}")
        time.sleep(5)