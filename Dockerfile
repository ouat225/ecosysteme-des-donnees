# Utilisation de l'image Python officielle
FROM python:3.12-slim

WORKDIR /app

# 1. Installation des dépendances système (Pour nettoyer les fichiers Windows)
RUN apt-get update && apt-get install -y dos2unix

# 2. Copie et installation des librairies Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copie de tout le code
COPY . .

# 4. Nettoyage magique du script start.sh (Conversion CRLF -> LF)
RUN dos2unix start.sh
RUN chmod +x start.sh

# 5. Exposition des ports
EXPOSE 16080
EXPOSE 16081

# 6. Lancement
CMD ["./start.sh"]