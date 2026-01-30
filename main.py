import numpy as np

def calcul_lotka_volterra(Ni_prev, Nj_curr, r_i=0.05, alpha_i=0.02):
    """
    Calcule la nouvelle population Ni en fonction de la compétition avec Nj.
    Formule simplifiée pour la simulation : Ni(t+1) = Ni(t) + croissance - competition
    """
    # Modèle discret simple :
    # La population change selon son taux de croissance, freinée par la compétition avec Nj
    delta = (r_i * Ni_prev) - (alpha_i * Ni_prev * Nj_curr / 20000) 
    
    Ni_new = Ni_prev + delta
    
    # On évite les populations négatives ou explosives pour la démo
    return max(0, Ni_new)

def get_simulation_nj(temps):
    """
    Simule la population adverse (Dragon) si l'API B n'est pas disponible.
    Utilise la fonction Cosinus demandée.
    """
    Kj = 16080
    return abs(Kj * np.cos(temps))