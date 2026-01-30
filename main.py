import math

def calcul_lotka_volterra(Ni, Nj, r, K, alpha):
    """
    Calcule la population au temps t+1 selon la formule discrète du sujet :
    Nt+1 = Nt * (1 + r * (1 - (Nt + alpha * N_adverse) / K))
    """
    # 1. Calcul de la densité (compétition intra + inter-spécifique)
    term_densite = (Ni + (alpha * Nj)) / K
    
    # 2. Calcul du facteur de croissance
    facteur = 1 + (r * (1 - term_densite))
    
    # 3. Application
    Ni_next = Ni * facteur
    
    # Sécurité : Pas de population négative
    return max(0, Ni_next)

def get_simulation_nj(temps):
    """
    Simule la population adverse (Groupe H - Zombies) pour la phase de test.
    Oscille entre 800 et 1200 pour voir l'impact sur la Wyverne.
    """
    base = 1000
    amplitude = 200
    # Cosinus pour faire des vagues
    return base + amplitude * math.cos(temps / 5.0)