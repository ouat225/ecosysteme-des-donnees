#!/bin/bash
# Lancement de l'API sur 16081
uvicorn api:app --host 0.0.0.0 --port 16081 &

# Lancement du Dashboard sur 16080
streamlit run app.py --server.port 16080 --server.address 0.0.0.0