from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import requests
import main # On importe nos formules
import csv
import os

app = FastAPI(
    title="Wyverne API",
    description="Simulation Wyverne vs Dragon",
    version="1.0.0"
)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

# État global de la simulation (en mémoire)
simulation_state = {
    "temps": 0,
    "Ni": 13897.0, # Population initiale Wyverne
    "r": 0.05,
    "alpha": 0.02
}

# Nom du fichier CSV pour l'historique
CSV_FILE = "wyverne_history.csv"

# Initialisation du fichier CSV (si vide, on met les entêtes)
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["temps", "taille", "population_adverse_nj", "taux_de_competition", "taux_de_croissance"])

# Adresse de la population B (Dragon - Projet B)
URL_DRAGON = "http://host.docker.internal:16010/population"

@app.get("/population")
def get_population_step():
    global simulation_state
    
    # 1. Récupérer la population adverse (Nj)
    nj_val = 0
    try:
        # TENTATIVE DE CONFRONTATION RÉELLE
        response = requests.get(URL_DRAGON, timeout=1)
        if response.status_code == 200:
            data_dragon = response.json()
            nj_val = data_dragon.get("taille", data_dragon.get("population", 0))
            print(f"🐉 Dragon détecté : {nj_val}")
        else:
            raise Exception("Pas de réponse 200")
    except:
        # FALLBACK : SIMULATION COSINUS
        nj_val = main.get_simulation_nj(simulation_state["temps"])
        print(f"⚠️ Dragon simulé (Cosinus) : {nj_val}")

    # 2. Calculer la nouvelle population Wyverne (Ni)
    ni_next = main.calcul_lotka_volterra(
        simulation_state["Ni"], 
        nj_val, 
        simulation_state["r"], 
        simulation_state["alpha"]
    )
    
    # 3. Sauvegarder dans le CSV (LA CONSIGNE OUBLIÉE)
    with open(CSV_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            simulation_state["temps"], 
            ni_next, 
            nj_val, 
            simulation_state["alpha"], 
            simulation_state["r"]
        ])
    
    # 4. Mettre à jour l'état
    simulation_state["Ni"] = ni_next
    simulation_state["temps"] += 0.5 # On avance le temps

    # 5. Renvoyer les infos JSON
    return {
        "temps": simulation_state["temps"],
        "taille": float(ni_next),
        "population_adverse_nj": float(nj_val),
        "taux_de_competition": simulation_state["alpha"],
        "taux_de_croissance": simulation_state["r"]
    }