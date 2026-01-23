library(plumber)

# Paramètres globaux du projet I
r_i <- 0.5
K_i <- 1000
DB_FILE <- "wyverne_history.csv"

#* @apiTitle API Wyverne - Projet I
#* @get /calculer
#* @param Ni_prev Taille population précédente
#* @param alpha_ij Paramètre de compétition
#* @param t Temps (pour calculer Nj)
function(Ni_prev=100, alpha_ij=0.1, t=1) {
  Ni_prev <- as.numeric(Ni_prev)
  alpha_ij <- as.numeric(alpha_ij)
  t <- as.numeric(t)
  
  # Nj(t) = Kj * cos(t) selon consigne (on prend Kj = Ki pour le test)
  Nj_t <- K_i * cos(t)
  
  # Formule Lotka-Volterra du sujet
  Ni_curr <- Ni_prev * (1 + r_i * (1 - (Ni_prev + alpha_ij * Nj_t) / K_i))
  
  # Stockage complet (données perçues + calculées)
  donnees <- data.frame(
    date = Sys.time(),
    temps_t = t,
    Ni_precedent = Ni_prev,
    taux_competition = alpha_ij,
    taille = Ni_curr
  )
  write.table(donnees, DB_FILE, append = TRUE, sep = ",", 
              col.names = !file.exists(DB_FILE), row.names = FALSE)
  
  # Retourne les champs exacts demandés
  list(
    taille = Ni_curr,
    taux_de_competition = alpha_ij,
    taux_de_croissance = r_i
  )
}
