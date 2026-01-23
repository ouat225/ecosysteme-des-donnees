library(shiny)
library(ggplot2)
library(dplyr)
library(shinydashboard)

# Interface utilisateur
ui <- dashboardPage(
  dashboardHeader(title = "Modélisation Éco-système"),
  
  dashboardSidebar(
    sidebarMenu(
      menuItem("Simulation", tabName = "simulation", icon = icon("chart-line")),
      menuItem("Visualisation", tabName = "visualisation", icon = icon("chart-bar")),
      menuItem("À propos", tabName = "about", icon = icon("info-circle"))
    )
  ),
  
  dashboardBody(
    tabItems(
      # Onglet Simulation
      tabItem(tabName = "simulation",
              fluidRow(
                box(
                  title = "Paramètres de simulation",
                  status = "primary",
                  solidHeader = TRUE,
                  width = 4,
                  numericInput("ni_prev", "Taille initiale de la population (Ni_prev):", 100, min = 1),
                  numericInput("alpha_ij", "Taux de compétition (α_ij):", 0.1, min = 0, max = 1, step = 0.01),
                  numericInput("t_final", "Période de simulation (t):", 50, min = 1, max = 200),
                  actionButton("run_sim", "Lancer la simulation", class = "btn-success")
                ),
                box(
                  title = "Résultats de la simulation",
                  status = "info",
                  solidHeader = TRUE,
                  width = 8,
                  plotOutput("simulation_plot", height = "400px"),
                  hr(),
                  tableOutput("results_table")
                )
              )
      ),
      
      # Onglet Visualisation
      tabItem(tabName = "visualisation",
              fluidRow(
                box(
                  title = "Paramètres de visualisation",
                  status = "primary",
                  solidHeader = TRUE,
                  width = 12,
                  dateRangeInput("date_range", "Période d'analyse:", 
                               start = Sys.Date() - 30, 
                               end = Sys.Date()),
                  selectInput("plot_type", "Type de graphique:",
                              choices = c("Lignes" = "line", 
                                         "Points" = "point",
                                         "Aires" = "area")),
                  actionButton("update_plot", "Mettre à jour")
                ),
                box(
                  title = "Évolution des populations",
                  status = "info",
                  solidHeader = TRUE,
                  width = 12,
                  plotOutput("population_plot", height = "400px")
                )
              )
      ),
      
      # Onglet À propos
      tabItem(tabName = "about",
              h2("À propos de l'application"),
              p("Cette application permet de modéliser et visualiser la dynamique des populations en utilisant le modèle de compétition interspécifique de Lotka-Volterra."),
              h3("Paramètres du modèle"),
              p("- Ni_prev: Taille initiale de la population"),
              p("- α_ij: Taux de compétition entre les espèces"),
              p("- r_i: Taux de croissance intrinsèque"),
              p("- K_i: Capacité de charge de l'environnement"),
              h3("Équations"),
              withMathJax(helpText("$$N_i(t+1) = N_i(t) \\cdot \\left[1 + r_i \\cdot \\left(1 - \\frac{N_i(t) + \\alpha_{ij} \\cdot N_j(t)}{K_i}\\right)\\right]$$")),
              p("où \(N_j(t) = K_i \\cdot \\cos(t)\)"),
              h3("Auteur"),
              p("Projet réalisé dans le cadre du Master 2 Analyse et Politique Économique, parcours Statistique pour l'évaluation et la prévision")
      )
    )
  )
)

# Serveur
server <- function(input, output, session) {
  
  # Simulation réactive
  sim_data <- eventReactive(input$run_sim, {
    # Paramètres initiaux
    Ni_prev <- input$ni_prev
    alpha_ij <- input$alpha_ij
    t_final <- input$t_final
    
    # Vecteur temps
    t_vals <- 1:t_final
    
    # Initialisation des vecteurs de résultats
    Ni <- numeric(t_final)
    Nj <- numeric(t_final)
    Ni[1] <- Ni_prev
    
    # Simulation
    for (t in 2:t_final) {
      Nj[t-1] <- 1000 * cos(t-1)  # K_i = 1000 comme dans api.R
      Ni[t] <- Ni[t-1] * (1 + 0.5 * (1 - (Ni[t-1] + alpha_ij * Nj[t-1]) / 1000))
      Nj[t] <- 1000 * cos(t)  # Mise à jour de Nj pour le pas de temps suivant
    }
    
    # Création du dataframe de résultats
    data.frame(
      temps = 1:t_final,
      Population_Ni = Ni,
      Population_Nj = Nj[1:t_final]
    )
  })
  
  # Graphique de simulation
  output$simulation_plot <- renderPlot({
    data <- sim_data()
    
    ggplot(data, aes(x = temps)) +
      geom_line(aes(y = Population_Ni, color = "Population Ni"), size = 1.2) +
      geom_line(aes(y = Population_Nj, color = "Population Nj"), size = 1.2) +
      labs(title = "Dynamique des populations au cours du temps",
           x = "Temps (t)",
           y = "Taille de la population",
           color = "Légende") +
      theme_minimal() +
      theme(
        legend.position = "bottom",
        plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
        axis.title = element_text(size = 12),
        legend.text = element_text(size = 11)
      ) +
      scale_color_manual(values = c("Population Ni" = "#1f77b4", 
                                  "Population Nj" = "#ff7f0e"))
  })
  
  # Tableau des résultats
  output$results_table <- renderTable({
    data <- sim_data()
    tail(data, 5)  # Afficher les 5 dernières lignes
  }, striped = TRUE, hover = TRUE, bordered = TRUE)
  
  # Graphique de visualisation des données historiques
  output$population_plot <- renderPlot({
    # Lire les données historiques
    if (file.exists("wyverne_history.csv")) {
      hist_data <- read.csv("wyverne_history.csv")
      
      # Filtrer par date si nécessaire
      hist_data$date <- as.Date(hist_data$date)
      hist_data <- hist_data %>% 
        filter(date >= input$date_range[1] & date <= input$date_range[2])
      
      # Créer le graphique en fonction du type sélectionné
      p <- ggplot(hist_data, aes(x = date, y = taille)) +
        labs(title = "Évolution historique de la population",
             x = "Date",
             y = "Taille de la population") +
        theme_minimal() +
        theme(
          plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
          axis.title = element_text(size = 12)
        )
      
      if (input$plot_type == "line") {
        p <- p + geom_line(color = "#1f77b4", size = 1)
      } else if (input$plot_type == "point") {
        p <- p + geom_point(color = "#1f77b4", size = 2)
      } else {
        p <- p + geom_area(fill = "#1f77b4", alpha = 0.5)
      }
      
      p
    }
  })
}

# Lancer l'application
shinyApp(ui, server)
