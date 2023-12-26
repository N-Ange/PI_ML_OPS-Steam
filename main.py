from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import HTMLResponse
import asyncio
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import re
import functions
import warnings
import os
warnings.filterwarnings("ignore")


app = FastAPI()
ruta_revieews_year = 'data/df_reviews_year.parquet'
ruta_horas_juego = 'data/df_reviews_year.parquet'
try:
    df_reviews_year = pd.read_parquet(ruta_revieews_year)
    df_horas_juego = pd.read_parquet(ruta_horas_juego)
except FileNotFoundError:
    # Si el archivo no se encuentra, maneja la excepción
    raise HTTPException(status_code=500, detail="Error al cargar el archivo de datos")

@app.get("/")
def index():
    return "hola"




@app.get("/PlayTimeGenre/{genero}")
def PlayTimeGenre(genero:str):
    
    

    gener = df_horas_juego[df_horas_juego["genres"].str.lower() ==genero.lower()]
    if not gener.empty:
        horas_anio = gener.groupby("release_year")["playtime_forever"].sum().reset_index()
        max_horas  = horas_anio["playtime_forever"].max()
        anio = horas_anio.loc[horas_anio["playtime_forever"] == max_horas,"release_year"].iloc[0]
        
        return  {
            anio,"Año de lanzamiento con mas horas jugadas para el Genero: {}".format(genero) 
            }
    
@app.get("/UserForGenre{genero}")
def UserForGenre(genero:str):
  
    # Filtrar las horas de juego para el género especificado
    horas = df_horas_juego[df_horas_juego['genres'] == genero][["playtime_forever", "release_year", "user_id"]]

    # Agrupar por usuario y sumar las horas jugadas
    player = horas.groupby("user_id")["playtime_forever"].sum()

    # Obtener el usuario con más horas jugadas
    player_max = player.idxmax()

    # Obtener la acumulación de horas jugadas por año
    year = horas.groupby("release_year")["playtime_forever"].sum().reset_index()

    # Filtrar las horas jugadas del usuario con más horas
    horas_player = horas[horas["user_id"] == player_max]

    # Crear el diccionario de retorno
    resultado = {
        "Usuario con más horas jugadas para " + genero: player_max,
        "Horas jugadas": year.to_dict(orient="records")
    }

    return resultado


    

@app.get("/UsersNotRecommend/{anio}")
def UsersNotRecommend(anio):
    
    filtro = (df_reviews_year["reviews_posted"] == anio) & (df_reviews_year["reviews_recommend"] == False) & (df_reviews_year["sentiment_analysis"] == 0)
    reviews = df_reviews_year[filtro]

    games = reviews.groupby(df_reviews_year["item_id"]).size().reset_index(name="count")
    games = games.sort_values(by="count", ascending=False)
      
    top_por_anio = {} 
    for index, row in resultado.iterrows():
       anio_info={
        "item_id": row["item_id"],
        }
    resultado = games.head(3)

@app.get("/UsersNotRecommend2/{anio}")
def UsersNotRecommend2(anio):
   
    filtro = (df_reviews_year["reviews_posted"] == anio) & (df_reviews_year["reviews_recommend"] == False) & (df_reviews_year["sentiment_analysis"] == 0  )
    reviews = df_reviews_year[filtro] 

    games = reviews.groupby(df_reviews_year["title"]).size().reset_index(name="count")
    games = games.sort_values(by = "count",ascending = False)
    return games.head(3)