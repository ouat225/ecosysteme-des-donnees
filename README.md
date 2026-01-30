# ÉCOSYSTÈME WYVERNE

Un outil interactif pour simuler la dynamique de population des wyvernes.

## Aperçu

L’écosystème Wyverne fournit une application conteneurisée permettant de simuler et visualiser l’interaction entre une population de Wyvernes (N_i) et une population de Dragons de contrôle (N_j) à l’aide d’un modèle mathématique.
Il permet de :
- Calculer l’évolution des populations selon les taux de croissance et de compétition
- Exposer les données via une API REST (FastAPI) pour l’interopérabilité.
- Visualiser l’évolution temporelle via un tableau de bord interactif

## Fonctionnalités

- **Modélisation mathématique**: Simulation de la dynamique des populations dans le temps (t = 0 à 10)
- **API REST**: Expose les métriques clés (taille, taux_de_competition, taux_de_croissance) au format JSON
- **Visualisation interactive**: Graphiques en temps réel de la courbe de population via Streamlit
- **Conteneurisation**: Environnement totalement isolé grâce à Docker avec mappage automatique des ports.

## Prérequis

- Dépendances internes : 
- Python 3.12+
- Docker 
- FastAPI & Uvicorn
- Streamlit
- Pandas & NumPy

## Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://gitlab-mi.univ-reims.fr/musi0005/projet_eco_sys.git
   ```

2. **Installation**
   ```bash
   docker build -t wyverne-python .
   ```

3. **Lancement**
   ```bash
   .\launcher.ps1
   ```

4. **Utilisation de l’application**

L’application s’ouvrira automatiquement dans votre navigateur :
Tableau de bord (Frontend): http://localhost:16080
API (Backend): http://localhost:16081/population
Naviguez dans le tableau de bord pour visualiser la courbe de population ou accédez à l’API pour obtenir les données brutes.

## Structure du projet

```

Projet_éco_sys/
├── main.py                     
├── api.py                      
├── app.py                       
├── Dockerfile                   
├── start.sh                    
├── launcher.ps1                 
├── requirements.txt             
└── README.md                    

```

## Jeu de données

### Source

Les données sont générées mathématiquement selon le modèle d’interaction défini dans les spécifications du Projet I :
- Ports Réseau (16080 & 16081)
- Population (Wyverne)
- Google Cloud Platform

### Description des variables

| Variable | Type | Description |
|----------|------|-------------|
| taille | valeur flottante | Taille actuelle de la population de Wyvernes (N_i) |
| taux_de_competition | valeur flottante | Taux de compétition (\$alpha_i$ = 0.02) |
| taux_de_croissance | valeur flottante | Taux de croissance (r_i = 0.05) |
| temps | tableau | Échelle temporelle de 0 à 10 |

## Auteurs

- Oumar Abdramane ALLAWAN
- Dominique MUSITELLI
- Jean-Marc OUATTARA