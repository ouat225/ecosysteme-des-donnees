#!/bin/bash
# Lancement de l'API sur 16083
uvicorn api:app --host 0.0.0.0 --port 16083 &

# Lancement du Dashboard sur 16082
streamlit run app.py --server.port 16082 --server.address 0.0.0.0