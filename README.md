# WYVERNE ECOSYSTEM

An interactive tool for simulating Wyverne population dynamics.

## Overview

Wyverne ecosystem provides a containerized application to simulate and visualize the interaction between a Wyverne population ($N_i$) and a control Dragon population ($N_j$) using a mathematical model.
It allows you to:
- Calculate population evolution based on growth and competition rates
- Expose data via a REST API (FastAPI) for interoperability
- Visualize temporal evolution through an interactive dashboard

## Features

- **Mathematical Modeling**: Simulation of population dynamics over time ($t=0$ to $10$)
- **REST API**: Exposes key metrics (taille, taux_de_competition, taux_de_croissance) in JSON format
- **Interactive Visualization**: Real-time charting of the population curve using Streamlit
- **Containerization**: Fully isolated environment using Docker with automated port mapping

## Requirements

- Docker Desktop (Required for containerization)
- PowerShell (For automated deployment script)
- Internal dependencies (managed by Docker): 
- Python 3.12+
- FastAPI & Uvicorn
- Streamlit
- Pandas & NumPy

## Installation and Usage

1. **Clone the repository**
   ```bash
   git clone https://gitlab-mi.univ-reims.fr/musi0005/projet_eco_sys.git
   ```

2. **If script execution is disabled (run this command)**
   ```bash
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Automated Launch (Recommended)**
   ```bash
   .\launcher.ps1
   ```

4. **Installation (Docker CLI)**
   ```bash
   docker build -t wyverne-python .
   ```

   ```bash
   docker run -p 16080:8501 -p 16081:8000 wyverne-python
   ```

5. **Manual Access to the Application**
- Dashboard	
   ```bash
   http://localhost:16080
   ```

- API Data
   ```bash
   http://localhost:16081/population
   ```


6. **Use of the application**

The application will automatically open in your browser
Dashboard (Frontend): http://localhost:16080
API (Backend): http://localhost:16081/population
Navigate through the dashboard to view the population curve or access the API for raw data.

## Project structure

```

Projet_éco_sys/
├── main.py                      # Simulation logic 
├── api.py                       # FastAPI Backend 
├── app.py                       # Streamlit Frontend 
├── Dockerfile                   # Container configuration
├── start.sh                     # Internal entrypoint script
├── launcher.ps1                 # Windows deployment automation script
├── requirements.txt             
└── README.md                    

```

## Dataset

### Source
The data is generated mathematically based on the interaction model defined in the specifications of Project I :
- Network Ports (16080)
- Population (Wyverne)
- Google Cloud Platform

### Variable Descriptions

| Variable | Type | Description |
|----------|------|-------------|
| taille | float | Current size of the Wyverne population ($N_i$) |
| taux_de_competition | float | Competition rate ($\alpha_i = 0.02$) |
| taux_de_croissance | float | Growth rate ($r_i = 0.05$) |
| temps | array | Time scale from 0 to 10 |

## Authors

- Oumar Abdramane ALLAWAN
- Dominique MUSITELLI
- Jean-Marc OUATTARA