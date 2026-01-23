# 1. Installer le package (à ne faire qu'une seule fois sur votre PC/VDI)
install.packages("plumber")

# 2. Charger la bibliothèque (indispensable à chaque nouvelle session)
library(plumber)

# 3. Créer l'objet API (assurez-vous que le fichier se nomme bien api.R)
pr <- plumb("api.R")

# 4. Lancer le serveur sur votre port attribué
pr$run(host = "0.0.0.0", port = 16080)
