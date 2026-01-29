from fastapi import FastAPI
import pandas as pd

app = FastAPI() 

@app.get("/population")
def get_population():
    try:
        # On lit le CSV généré par main.py
        df = pd.read_csv("wyverne_history.csv")
        last_row = df.iloc[-1]
        
        return {
            "taille": float(last_row['taille']),
            "taux_de_competition": float(last_row['taux_de_competition']),
            "taux_de_croissance": float(last_row['taux_de_croissance'])
        }
    except Exception as e:
        return {"error": str(e)}