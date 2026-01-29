# Image de base Python
FROM python:3.10-slim

# Installation des dépendances
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie des fichiers
COPY . .

# Génération initiale des données
RUN python main.py

# Exposition des ports (API et Streamlit)
EXPOSE 8000
EXPOSE 8501

# Script pour lancer l'API et Streamlit en même temps
CMD uvicorn api:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0