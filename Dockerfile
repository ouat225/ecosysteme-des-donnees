FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh

# Ports officiels du Projet I
EXPOSE 16080
EXPOSE 16081

# Script pour lancer l'API et Streamlit
CMD ["./start.sh"]