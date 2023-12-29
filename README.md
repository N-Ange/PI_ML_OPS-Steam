## Introcucción
Este proyecto se trabaja sobre la plataforma de juegos Steam, desde un rol de Data Engineer para obtener un MVP (Minimum Viable Product). Para el desarrolo del mismo se reciben 3 datasets.
Se va a dessarrolar la Extraccion, Transformacion y carga (ETL) y el Analisis Exploratorio de Datos(EDA), para luego hacer un analisis de sentimineto y un sistema de recomendacion.


## Datos
 australian_user_reviews.json: Este dataset conitene la informacion sobre los comentarios que hicieron los usuarios sobre los juegos que consumen, ademas si recomendian o no el juego.

 australian_user_items.json: Este dataset contiene informacion sobre los juegos adquiridos por cada usuario, como tambien el tiempo acumulado de juego apra cada uno.

 output_steam_games.json= Este dataset contiene la informacion sobre los juegos de steam, como titulo, desarrollador, precio,genero, entre otros.

 ## Tareas

 # Transformacion
 Se realizo el proceso de ETL de los 3 datasets.
 Dos de los dataset estaban anidados, es decir habia columnas con diccionarios o listas de diccionarios, por lo que se hizo un proceso de desanidad para transformar esos datos en columnas.
 Luego se borraron varias columnas y datos que no aportaban informacion util para el proyecto, ya que habia una limitacion por el rendimiento de la API.
 [01_ELT australian_user_reviews](https://github.com/N-Ange/PI_ML_OPS-Steam/blob/main/01_ETL%20australian_user_reviews.ipynb)
 [01_ETL australian_users_items](https://github.com/N-Ange/PI_ML_OPS-Steam/blob/main/01_ETL%20australian_users_items.ipynb)
 [01_ETL output_steam_games](https://github.com/N-Ange/PI_ML_OPS-Steam/blob/main/01_ETL%20output_steam_games.ipynb)
 [EDA]https://github.com/N-Ange/PI_ML_OPS-Steam/blob/main/EDA.ipynb



# Analisis de sentimientos

Uno de los pedidos del proyecto es un analisis de sentimientos, para lo cual se creo una nueva columna que remplazaba la columna que contenia los comentarios de los jugadores, y clasificando dichos comentarios segun sentimientos de la siguiente manera:

* 0 Si es malo.
* 1 si es neutral o no tiene comentario.
* 2 si es positivo.

Ya que solo se buscaba un MVP se realizo un analisis de sentimiento basico utilizando la libreria TextBlob que es libreria de procesamiento natural de lenguaje (NLP). El metodo que utilizado es asignar un valor numerico a un texto, por ejemplo los comentarios de los usuarios, para asi representar el sentimiento expresado en el texto.

[Enginer](https://github.com/N-Ange/PI_ML_OPS-Steam/blob/main/enginer.ipynb)

## Analisis exoloratorio de datos
Se realizo un EDA de los 3 datasets ya sometidos a ETL con la finalidad de identificar las variables que se pueden llegar a utilizar en la creacion del modelo de recomendacion. Se utilizo la libreria Pandas para el manejo de datos y las librerias Matplotlib y seaborn para la visualizacion.

[EDA](https://github.com/N-Ange/PI_ML_OPS-Steam/blob/main/EDA.ipynb)

Al finalizar se decidio construir un dataframe especifico con la informacion nesesaria, id del usuario, nombres de los juegos, y el raiting que se creo con la combinacion dell analisis de sentimiento y la recomendacion.

# Modelo de aprendizaje

Se crearon dos modelos de recomendacion, uno recibe el nombre de un juego y otro recibe id de un usuario, ambos devuelven una lista de 5 juegos recomendados.

El primero tiene una relacion item - item, se toma un juego y basandose en la similitud con otros juegos devuelve los recomendados. El segundo es una relacion usuario-itemm es decir recibe un usuario, y encuentra usuarios similares y recomiedan jugos que a esos usuarios les gustaron.

Para generar estos modelos se uso la similitud de coseno que es una medida que se utiliza comunmente para evaluar la similitd entre dos vectores en un espacio multidimensional.
[Modelo de Recomendacion](https://github.com/N-Ange/PI_ML_OPS-Steam/blob/main/Modelo%20de%20recomendacion.ipynb)

# Desarrolo de Api
Para la Api se uso la libreria FastApi y se generaron las sigueintes funciones.

* PlayTimeGenre: Esta funcion recibe el genero de un juego y devuelve el año con mas horas jugadas segun el año de lanzamiento de cada juego para dicho genero.
* UserForGenre: Recibe un genero y devuelve el usuario que mas horas jugo dicho genero, y cuantas horas jugo cada año.
* UsersRecommend: Recibe un año y devuelve los 3 juegos mas recomendados para dicho año.
* UserNotRecommend: Recibe un año y devuelve los 3 juegos menos recomendados para dicho año.
* sentiment_analysis:Recibe un año y devuelve una lsita con la cantidad y tipo de comnetarios se hicieron ese año.
* recomendacion de juego: Recibe el nombre de un jeugo y devuelve una lista con 5 juegos similares.
[API](https://github.com/N-Ange/PI_ML_OPS-Steam/blob/main/main.py)
# Deploy
Para el deploy de la API se eligio la plataforma Render la cual nos permite crear y ejecutar aplicaciones, sitios web, permitiendo el despliegue autoatico desde GitHub.
[Render](https://pi-ml-ops-steam-z21p.onrender.com/)

Segenero un servicio nuevo en render, se conecto el repositorio para luego iniciar el servicio.



## Mejoras
Para este proyecto se presento un MVP se realizaron analisis basicos que se podrian mejorar:

* Analsis de sentimiento: Se puede realizar un mejor analisis de sentimiento revisando los comentarios, ya que hay en diferentes idiomas y emoticonos. Tambien se podria ajustar mas el modelo probando con diferentes tipos de clasificacion.

* Modelo de Recomendacion: Se puede crear un rating que revise la cantidad de horas jugadas por cada usuario, el si fueron utiles los comentarios, el precio.

* EDA: Se puede hacer un analisis exploratorio de datos mas exhaustivo, buscando relaciones entre juegos y usuarios para generar un puntaje mas preciso en el momento de hacer las recomendaciones.

* ETL: Se puede hacer una transformaciones mas exhaustivas, como por ejemplo al faltar algunos datos se los elimina sin intentar averiguar por que no estaban ni donde se podian obtener.

* Otro servico de Nube: Se puede intentar usar otro servicio para cargar la API, ya que la version gratuita de render limita la memoria que se puede utilizar, por ejemplo se dejo afuera la segunda funcion de recomendacion ya que al utilizar sobre pasaba dicho limite.
