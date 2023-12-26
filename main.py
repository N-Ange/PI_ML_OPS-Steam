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
    '''
    Datos:
    - genero (str): Género para el cual se busca el usuario con más horas jugadas y la acumulación de horas por año.

    Funcionalidad:
    - Devuelve el usuario con más horas jugadas y una lista de la acumulación de horas jugadas por año para el género especificado.

    Return:
    - Dict: {"Usuario con más horas jugadas para Género X": List, "Horas jugadas": List}
    '''

    try:
        # Cargar solo las columnas necesarias para esta función
        juegos_genero = df_data_muestra[['genres', 'release_year', 'playtime_forever', 'user_id']].copy()

        condition = juegos_genero['genres'].apply(lambda x: genero in x)
        juegos_genero = juegos_genero[condition]

        juegos_genero['playtime_forever'] = juegos_genero['playtime_forever'] / 60
        juegos_genero['release_year'] = pd.to_numeric(juegos_genero['release_year'], errors='coerce')
        juegos_genero = juegos_genero[juegos_genero['release_year'] >= 100]
        juegos_genero['Año'] = juegos_genero['release_year']

        horas_por_usuario = juegos_genero.groupby(['user_id', 'Año'])['playtime_forever'].sum().reset_index()

        if not horas_por_usuario.empty:
            usuario_max_horas = horas_por_usuario.groupby('user_id')['playtime_forever'].sum().idxmax()
            usuario_max_horas = horas_por_usuario[horas_por_usuario['user_id'] == usuario_max_horas]
        else:
            usuario_max_horas = None

        acumulacion_horas = horas_por_usuario.groupby(['Año'])['playtime_forever'].sum().reset_index()
        acumulacion_horas = acumulacion_horas.rename(columns={'Año': 'Año', 'playtime_forever': 'Horas'})

        resultado = {
            "Usuario con más horas jugadas para " + genero: {"user_id": usuario_max_horas.iloc[0]['user_id'], "Año": int(usuario_max_horas.iloc[0]['Año']), "playtime_forever": usuario_max_horas.iloc[0]['playtime_forever']},
            "Horas jugadas": [{"Año": int(row['Año']), "Horas": row['Horas']} for _, row in acumulacion_horas.iterrows()]
        }

        return resultado

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Error al cargar los archivos de datos")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/UsersRecommend/{anio}")
def UsersRecommend(anio:int):
        
    '''
  Devuelve los 3 de juegos MAs recomendados por usuarios para el año dado.

   parameters::
    anio (int): Año para el cual se buscan los juegos menos recomendados.

  Returns:
    dict: Diccionario con los 3 juegos mas recomendados.
    '''
    try:
        # Filtrar el DataFrame
        filtro = df_data_muestra.query(f"reviews_year == {anio}")
        filtro = filtro[filtro['reviews_recommend'] == False]
        filtro = filtro[filtro['sentiment_analysis'] >= 1]
        

        # Obtener los juegos menos recomendados
        games = filtro.groupby('item_name')['item_name'].count().reset_index(name="count").sort_values(by="count", ascending=True).head(3)
        

        # Convertir el DataFrame a una lista
        list_game = {f"Puesto {i+1}": juego for i, juego in enumerate(games['item_name'])}
        
        return list_game
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener los juegos menos recomendados.")
    

@app.get("/UsersNotRecommend/{anio}")
def UsersNotRecommend(anio):
    
    '''
  Devuelve los 3 de juegos MENOS recomendados por usuarios para el año dado.

   parameters::
    anio (int): Año para el cual se buscan los juegos menos recomendados.

  Returns:
    dict: Diccionario con el top 3 de juegos menos recomendados.
    '''
    try:
        # Filtrar el DataFrame
        filtro = df_data_muestra.query(f"reviews_year == {anio}")
        filtro = filtro[filtro['reviews_recommend'] == False]
        filtro = filtro[filtro['sentiment_analysis'] == 0]
        

        # Obtener los juegos menos recomendados
        games = filtro.groupby('item_name')['item_name'].count().reset_index(name="count").sort_values(by="count", ascending=False).head(3)
        

        # Convertir el DataFrame a una lista
        list_game = {f"Puesto {i+1}": juego for i, juego in enumerate(games['item_name'])}
        
        return list_game
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener los juegos menos recomendados.")


@app.get("/sentiment_analysis/{anio}")
def sentiment_analysis(anio):
    try:
        positive = 0
        negative = 0
        neutral = 0
        filtro = (df_data_muestra["reviews_posted == {anio}"])
        reviews = df_data_muestra[filtro]
        
        for i in  reviews["sentiment_analysis"]:
            if i == 2:
                positive +=1
            elif i == 1:
                neutral +=1
            elif i == 0:
                negative +=1
        resultado = [
        {"Negativas: ",negative," Positivas: ",positive," Neutrales: ",neutral}]
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener los juegos menos recomendados.")
