import pandas as pd
import numpy as np

# Point 1 : Paramètres et calcul
Kj = 16080  # Capacité de la population précédente (Dragons)
t = np.linspace(0, 10, 100) # Temps de 0 à 10

# Paramètres 
r_i = 0.05      # taux_de_croissance
alpha_i = 0.02  # taux_de_competition

# Nj(t) = Kj * cos(t) (Population témoin)
Nj_t = Kj * np.cos(t)

# Ni(t) = Population Wyverne (calculée selon l'interaction)
# On utilise la valeur absolue pour éviter les populations négatives
Ni_t = np.abs(Nj_t * (1 + r_i - alpha_i))

# Stockage 
df = pd.DataFrame({
    'temps': t,
    'taille': Ni_t,
    'taux_de_croissance': r_i,
    'taux_de_competition': alpha_i
})

df.to_csv("wyverne_history.csv", index=False)
print("Données sauvegardées dans wyverne_history.csv")