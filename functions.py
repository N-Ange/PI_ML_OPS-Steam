import pandas as pd
from textblob import TextBlob
import re
from dateutil.parser import parse

def tipo_dato(df):
    ''' 
    Realiza el analisis de los tipos de dato del dataframe

    La funcion recibe un DataFrame (df) y devuelve un resumen de su contenido incluyendo infomracion sobre los tipos de datos de cada columna.


    Parameters:
    df(pandas.Dataframe):El DataFrame que se busca analizar.

    Returns: 
        pandas.DataFrame :Un Dataframe con el resumen de cada columna lo cual incluye:

            * nombre_campo: Nombre de columna
            *tipo_dato: Tipo de dato en cada columna
            *nulo: Cantidad de valores nuleos en cada columna
            *no_nulo%: Porcentaje de vaolores no nulos
            *nulo%: Porcentaje de valores Nulos

    '''

    titulos = {"nombre_campo":[], "tipo_dato":[], "nulo":[], "no_nulo%":[], "nulo%":[]}

    for columna in df.columns:
        no_nulos_porc = (df[columna].count()/ len(df)) * 100
        titulos["nombre_campo"].append(columna)
        titulos["tipo_dato"].append(df[columna].apply(type).unique())
        titulos["no_nulo%"].append(round(no_nulos_porc,2))
        titulos["nulo%"].append(round(100-no_nulos_porc,2))
        titulos["nulo"].append(df[columna].isnull().sum())
        
            
    df_info = pd.DataFrame(titulos)

    return df_info



def duplicados(df,column):
    '''
    Revisa y muestra la fila cuyos valores de la columna se reppiten.

    Recibe un dataframe y el nombre de la columna donde se desee revisar si hay datos duplicados.

    parameters:
        df(pandas.DataFrame): El DataFrame en el que se buscaran filas duplicadas.
        coulmn (str): El nombre de la columna donde se buscara los datos duplicados

    returns:
        pandas.Dataframe or str: Un dataframe con las filas duplicadas. En caso de no haber duplicados devuelve el mensaje "No se encontrar duplicados"


    '''

    rows_duplicated = df[df.duplicated(column, False)]

    if rows_duplicated.empty:
        return "No se encontraron duplicados"
    
    return rows_duplicated.sort_values(by=column)



def obtener_anio(fecha):
    '''
        Extrae el año de una fecha con formato Año/Mes/Dia.
        Si la fecha es nula o no tiene el formato deuvelve "No disponible"

        parameters:
        fecha (str o float o None): formato Año/Mes/Dia

        return
            str: El año si esta disponible y es valido, de otra forma devuelve "No disponible" 
    
    
    
    '''
    

    if pd.notna(fecha):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', fecha):
            return fecha.split('-')[0]
    return "Dato no disponible"


def remplazar_precio (value):
    '''
    Remplaza valores de una columna por 0

    La funcion va a tratar de convertir el valor en un numero flotante, si es exitosa se mantiene, si no se deuelve 0


parameters:
    Value: el valor que se intenta convertir.

    Returns: El valor numerico si se pudo convertir o 0 si no.



    '''
    if pd.isna(value):
        return 0
    try:
        flotante = float(value)
        return flotante
    except:
        return 0 
    

def conversion_fecha(fecha):
    '''
    Convierte una fecha de un formato especifico a otro

    args:
        fecha (str): Fecha en formato Monty Day Year
    
    return:
        str:fecha con formato YYYY-MM-DD

    '''
    match = re.search(r'(\w+\s\d{1,2},\s\d{4})',fecha)
    if match:
        fecha_str = match.group(1)
        try:
            fecha_dt = pd.to_datetime(fecha_str)
            return fecha_dt.strftime("%Y-%m-%d")
        except:
            return "Fecha inválida"
    else:
        return "Formato invalido"
        

def sentimientos(review):
    '''
    Recibe un texto y realiza un analisis de sentimiento devolviendo un valor numerico.

    Se va a usar la libreria TextBlob para analisar los sentimientos del texto.

    Parameters:
        review (str): El texto que se desea analizar.
    
    Returns:
        int: Un valor numerico que representa el sentimiento
         
        -0 Negativo
        -1 Neutral o sin Review
        -2 Positivo
    
    
    '''

    if review is None:
        return 1
    polarity =TextBlob(review).sentiment.polarity 
    if polarity < 0:
        return 0
    elif polarity > 0:
        return 2
    else:
        return 1
    

def porcentaje(df, columna):
    count = df[columna].value_counts()
    porcentajes = round(100*count/len(df),2)
    resultado =pd.DataFrame({
        "cantidad":count,
        "Porcentaje":porcentajes
    })
    return resultado


def whisker_max(columna):
    
    q1= columna.describe()[4]
    q3= columna.describe()[6]
    whisker_max = round(q3 + 1.5*(q3 - q1),2)
    print (f"El bigote superir de la variable {columna.name} se ubica en:", whisker_max)
    print(f"Hay {(columna > whisker_max).sum()} valores atipocs en la variable {columna.name}")
    


