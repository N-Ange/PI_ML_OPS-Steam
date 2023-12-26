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
'''ruta_reviews_year = 'data/df_reviews_year.parquet'
ruta_horas_juego = 'data/horas_juego.parquet'
try:
    df_reviews_year = pd.read_parquet(ruta_reviews_year)
    df_horas_juego = pd.read_parquet(ruta_horas_juego)
except FileNotFoundError:
    # Si el archivo no se encuentra, maneja la excepción
    raise HTTPException(status_code=500, detail="Error al cargar el archivo de datos")'''

parquet_gzip_file_path = 'data/data_export_api_gzip.parquet'

try:
    # Especificar el porcentaje de datos a cargar
    sample_percent = 5  # Ajusta según tus necesidades

    # Leer una muestra del archivo Parquet directamente con pyarrow
    parquet_file = pq.ParquetFile(parquet_gzip_file_path)

    # Obtener la cantidad total de grupos de filas en el archivo
    total_row_groups = parquet_file.num_row_groups

    # Calcular la cantidad de grupos de filas a incluir en la muestra
    sample_row_groups = [i for i in range(total_row_groups) if i % (100 // sample_percent) == 0]

    # Leer solo los grupos de filas incluidos en la muestra
    df_data_muestra = parquet_file.read_row_groups(row_groups=sample_row_groups).to_pandas()
except FileNotFoundError:
    # Si el archivo no se encuentra, maneja la excepción
    raise HTTPException(status_code=500, detail="Error al cargar el archivo de datos comprimido con Gzip")

@app.get("/")
def index():
    return "hola"




@app.get("/PlayTimeGenre/{genero}")
def PlayTimeGenre(genero:str):

    try:
        gener = df_data_muestra.query(f"genres=='{genero}'")
        #gener = df_horas_juego[df_horas_juego["genres"].str.lower() ==genero.lower()]
        if not gener.empty:
            horas_anio = gener.groupby("release_year")["playtime_forever"].sum().reset_index()
            max_horas  = horas_anio["playtime_forever"].max()
            anio = horas_anio.loc[horas_anio["playtime_forever"] == max_horas,"release_year"].iloc[0]
            
            return  {"Año de lanzamiento con mas horas jugadas para el Genero:" + genero: int(anio)                 }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/UserForGenre{genero}")
def UserForGenre(genero:str):
   try:
    # Filtrar las horas de juego para el género especificado
    horas =df_data_muestra[df_data_muestra['genres'] == genero][["playtime_forever", "release_year", "user_id"]]

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
        "Horas jugadas":[{"Año": int(row["release_year"]), "Horas": int(row["playtime_forever"])} for _, row in year.iterrows()]
    }

    return resultado
   except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    

@app.get("/UsersNotRecommend/{anio}")
def UsersNotRecommend(anio):
    try:
    
        filtro = (df_data_muestra["reviews_posted"] == anio) & (df_data_muestra["reviews_recommend"] == False) & (df_data_muestra["sentiment_analysis"] == 0)
        reviews = df_data_muestra[filtro]

        games = reviews.groupby(df_data_muestra["item_id"]).size().reset_index(name="count")
        games = games.sort_values(by="count", ascending=False)
        
        top_por_anio = []
        for index, row in games.head(3).iterrows():
            anio_info={
                "Puesto": index + 1,
                "item_id": row["item_id"],
            }
            top_por_anio.append(anio_info)
        return top_por_anio
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/UsersNotRecommend2/{anio}")
def UsersNotRecommend2(anio):
   
    filtro = (df_data_muestra["reviews_posted"] == anio) & (df_data_muestra["reviews_recommend"] == False) & (df_data_muestra["sentiment_analysis"] == 0  )
    reviews = df_data_muestra[filtro] 

    games = reviews.groupby(df_data_muestra["title"]).size().reset_index(name="count")
    games = games.sort_values(by = "count",ascending = False)
    return games.head(3)