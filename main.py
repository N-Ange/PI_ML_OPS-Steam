from fastapi import FastAPI
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import re
import functions
import warnings
import os
warnings.filterwarnings("ignore")


app = FastAPI()
#df_horas_juego = pd.read_parquet("data\horas_juego.parquet")
#df_reviews_year = pd.read_parquet("PI_ML_OPS-Steam\data\df_reviews_year.parquet")
#http://127.0.0.1:8000 

@app.get("/")
def index():
    return "hola"




@app.get("/PlayTimeGenre/{genero}")
def PlayTimeGenre(genero:str):
    
    df_horas_juego = pd.read_parquet("data/horas_juego.parquet")

    gener = df_horas_juego[df_horas_juego["genres"].str.lower() ==genero.lower()]
    if not gener.empty:
        horas_anio = gener.groupby("release_year")["playtime_forever"].sum().reset_index()
        max_horas  = horas_anio["playtime_forever"].max()
        anio = horas_anio.loc[horas_anio["playtime_forever"] == max_horas,"release_year"].iloc[0]
        
        return  {
            anio,"Año de lanzamiento con mas horas jugadas para el Genero: {}".format(genero) 
            }
    
'''
@app.get("/UsersNotRecommend/{anio}")
def UsersNotRecommend(anio):
    filtro = (df_reviews_year["reviews_posted"] == anio) & (df_reviews_year["reviews_recommend"] == False) & (df_reviews_year["sentiment_analysis"] == 0)
    reviews = df_reviews_year[filtro]

    games = reviews.groupby(df_reviews_year["item_id"]).size().reset_index(name="count")
    games = games.sort_values(by="count", ascending=False)

    resultado2 = [
        {"Puesto 1": games.iloc[0]["item_id"]},
        {"Puesto 2": games.iloc[1]["item_id"]},
        {"Puesto 3": games.iloc[2]["item_id"]}
    ]
    return resultado2

      
   
  '''  
'''
top_por_anio = {} 
for index, row in resultado.iterrows():
       anio_info={
        "item_id": row["item_id"],
        }
        resultado = games.head(3)

def UsersNotRecommend(anio):

    filtro = (year["reviews_posted"] == anio) & (year["reviews_recommend"] == False) & (year["sentiment_analysis"] == 0  )
    reviews = year[filtro] 

    games = reviews.groupby(df_reviews_year["item_id"]).size().reset_index(name="count")
    games = games.sort_values(by = "count",ascending = False)
    return games.head(3)
    '''