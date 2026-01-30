import streamlit as st
import pandas as pd
import time
import requests
import os

# --- CONFIG PAGE ---
st.set_page_config(page_title="Wyverne Monitor (Gr. I)", page_icon="🐉", layout="wide")
st.title("🐉 Tableau de Bord : Wyverne vs Zombies (Groupe H)")
st.markdown("---")

# --- CONFIG RÉSEAU ---
API_URL = os.getenv("API_URL", "http://api:8000/population")

# --- CONFIG HISTORIQUE ---
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["temps", "Wyverne", "Zombies"])

# --- LAYOUT ---
col1, col2, col3 = st.columns(3)
metric_wyverne = col1.empty()
metric_zombie = col2.empty()
metric_temps = col3.empty()

st.subheader("📈 Évolution en Temps Réel")
chart_placeholder = st.empty()

# --- BOUCLE ---
while True:
    try:
        response = requests.get(API_URL, timeout=2)
        if response.status_code == 200:
            data = response.json()
            
            # MÉTRIQUES
            metric_wyverne.metric("🐉 Wyverne (Nous)", f"{data['taille']:.2f}")
            metric_zombie.metric("🧟 Zombies (Cible)", f"{data['population_cible_nj']:.2f}")
            metric_temps.metric("⏱️ Temps", f"t = {data['temps']}")

            # GRAPHIQUE
            new_row = pd.DataFrame({
                "temps": [data["temps"]],
                "Wyverne": [data["taille"]],
                "Zombies": [data["population_cible_nj"]]
            })
            
            if st.session_state.history.empty:
                st.session_state.history = new_row
            else:
                st.session_state.history = pd.concat([st.session_state.history, new_row], ignore_index=True)

            # On utilise le temps comme axe X
            chart_data = st.session_state.history.set_index("temps")
            
            with chart_placeholder:
                # Vert pour Wyverne, Rouge pour Zombies
                st.line_chart(chart_data, color=["#00FF00", "#FF0000"]) 
        
        # ATTENTE 5 SECONDES
        time.sleep(5)

    except Exception as e:
        with chart_placeholder:
            st.warning(f"⏳ Démarrage API... ({e})")
        time.sleep(5)