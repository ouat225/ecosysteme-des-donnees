from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import main 
import csv
import os

app = FastAPI(title="Wyverne API (Groupe I)", version="1.0.0")

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

# --- PARAMÈTRES INITIAUX (MODIFIÉS POUR LE MOUVEMENT) ---
simulation_state = {
    "temps": 0,
    "Ni": 10.0,    # <--- DÉPART BAS (10) pour voir la croissance !
    "r": 0.5,      # Taux de croissance rapide
    "Ki": 1000.0,  # Plafond (Capacité)
    "alpha": 0.01  # Impact des Zombies sur nous
}

# --- CONFIGURATION RÉSEAU ---
# Cible : Groupe H (Zombies) = Port 16070
URL_CIBLE = "http://host.docker.internal:16070/population"

# --- STOCKAGE ---
os.makedirs("storage", exist_ok=True)
CSV_FILE = "storage/wyverne_history.csv"

# Création du fichier si inexistant
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["temps", "taille", "population_cible_nj", "taux_de_competition", "taux_de_croissance", "capacite_biotique"])

@app.get("/population")
def get_population_step():
    global simulation_state
    
    # 1. Simulation Zombies (Groupe H)
    # On utilise la simulation mathématique pour l'instant (voir main.py)
    nj_val = main.get_simulation_nj(simulation_state["temps"])

    # 2. Calcul Wyverne (Groupe I)
    ni_next = main.calcul_lotka_volterra(
        simulation_state["Ni"], 
        nj_val, 
        simulation_state["r"],
        simulation_state["Ki"], 
        simulation_state["alpha"]
    )
    
    # 3. Sauvegarde
    with open(CSV_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            simulation_state["temps"], ni_next, nj_val, 
            simulation_state["alpha"], simulation_state["r"], simulation_state["Ki"]
        ])
    
    # 4. Mise à jour État
    simulation_state["Ni"] = ni_next
    simulation_state["temps"] += 1.0

    # 5. Réponse JSON
    return {
        "taille": float(ni_next),
        "taux_de_competition": simulation_state["alpha"],
        "taux_de_croissance": simulation_state["r"],
        "temps": simulation_state["temps"],
        "population_cible_nj": float(nj_val),
        "capacite_biotique": simulation_state["Ki"]
    }