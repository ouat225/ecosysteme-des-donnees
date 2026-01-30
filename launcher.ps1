Write-Host "🐉 --- DÉMARRAGE DU PROJET WYVERNE ---" -ForegroundColor Green

# 1. Arrêter les anciens conteneurs (Le grand ménage)
Write-Host "1. Nettoyage des anciens conteneurs..."
docker ps -q | ForEach-Object { docker stop $_ }

# 2. Lancer le conteneur en mode DÉTACHÉ (-d)
# Ports : 16080 (Dashboard) et 16081 (API)
Write-Host "2. Lancement du conteneur..."
docker run -d -p 16080:16080 -p 16081:16081 wyverne-python

# 3. Petite pause pour laisser le temps au serveur de démarrer
Write-Host "3. Attente du démarrage du serveur (5 secondes)..."
Start-Sleep -Seconds 5

# 4. Ouverture automatique du navigateur
Write-Host "4. Ouverture des pages Web..."
Start-Process "http://localhost:16080"
Start-Process "http://localhost:16081/population"