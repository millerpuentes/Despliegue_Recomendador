#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Equipo 7 - DSA
"""

# Importe de librerías para ejecutar los modelos
import pandas as pd
import numpy as np
import pyLDAvis
import seaborn as sns
import matplotlib.pyplot as plt
import re
import spacy
from spacy.lang.es.examples import sentences
from unidecode import unidecode
import zipfile
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import nltk
import pyLDAvis.gensim_models
from gensim.corpora import Dictionary
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.decomposition import PCA
from sklearn.decomposition import LatentDirichletAllocation
from wordcloud import WordCloud
from gensim.models import CoherenceModel
from gensim.models.ldamulticore import LdaMulticore
from pprint import pprint
from gensim.models import LdaModel

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')

# Cargar el modelo de spacy para el español
nlp = spacy.load("es_core_news_sm")

# Obtener las stopwords en español
stopwords_lista = stopwords.words('spanish')


# Creamos un stemmer en español
stemmer = SnowballStemmer('spanish')

#Importe MLFlow para registrar los experimentos
import mlflow
import mlflow.sklearn



# Creación de funciones a utilizar 
def eliminar_stopwords(texto):
    # Tokenizar el texto en palabras
    palabras = nltk.word_tokenize(texto)

    # Filtrar las palabras que no son stopwords y que tienen más de 2 caracteres
    palabras_filtradas = [palabra for palabra in palabras if palabra.lower() not in stopwords_lista and len(palabra) >= 2]

    # Unir las palabras filtradas en un nuevo texto
    texto_filtrado = ' '.join(palabras_filtradas)

    return 

# Creamos un stemmer en español
def realizar_stemming(texto):
    # Tokenizar el texto en palabras
    palabras = nltk.word_tokenize(texto)

    # Aplicar stemming a cada palabra
    palabras_stemmed = [stemmer.stem(palabra) for palabra in palabras]

    # Unir las palabras stemmeadas en un nuevo texto
    texto_stemmed = ' '.join(palabras_stemmed)

    return 


# Creamos un lematizador
def lematizar(noticia):
    # Lematizamos las palabras
    lemmatizer = WordNetLemmatizer()
    # Tokenizamos el texto en palabras
    word_tokens = word_tokenize(str(noticia))
    # Lematizamos las palabras que no están en las stopwords, ni tienen más de 3 caracteres (previendo textos en inglés)
    tokens = [lemmatizer.lemmatize(w) for w in word_tokens if w not in stopwords_lista and len(w) > 3]
    # Unimos las palabras lematizadas en una cadena de texto
    texto_lematizado = " ".join(tokens)

    return texto_lematizado


# Importe el conjunto de datos
df_clientes = pd.read_csv('../Data/clientes.csv')
df_clientes_noticias = pd.read_csv('../Data/clientes_noticias.csv')
df_noticias = pd.read_csv('../Data/noticias.csv')



# Tratamiento previo
# Se eliminan la fechas
df_bd = df_clientes_noticias.drop(columns=['news_init_date','news_final_date'])
# Se une el set de datos de Clientes_Noticias con el de Clientes
df_bd = pd.merge(df_bd, df_clientes[['nit','subsec','nombre']], on='nit')
# El nuevo DF se une con el set de datos de las noticias
df_bd= pd.merge(df_bd, df_noticias[['news_id', 'news_title', 'news_text_content']], on='news_id').sort_values(by=['nit']).reset_index(drop=True)
# Creamos una nueva columna con valores únicos del título + el contenido de la noticia para luego proceder a eliminar noticias repetidas
df_bd['new_title_content'] = df_bd['news_title'] + ' ' + df_bd['news_text_content']
# Eliminamos filas con valores duplicados en la nueva columna creada 'new_title_content'
df_bd.drop_duplicates(subset='new_title_content', inplace=True)
# Para las noticias mantenemos unicamente la columna concatenada
df_bd = df_bd.drop(columns=['news_title','news_text_content'])

# Iniciamos a partir de la 3er columna para aplicar estos cambios en ('subsec', 'nombre', 'new_title_content')
for col in df_bd.columns[2:]:
  # Convertimos en minúsculas
  df_bd[col] = df_bd[col].str.lower()
  # Para todas las columnas excepto la url, eliminamos caracteres especiales, y nombres de meses y dias
  if col != 'news_url_absolute':
    # Se retiran las tildes
    df_bd[col] = df_bd[col].astype(str).apply(unidecode)
    # Se eliminan carácteres especiales y signos de puntuación
    df_bd[col] = df_bd[col].replace(r"[^A-Za-z\s]","", regex=True)
    df_bd[col] = df_bd[col].replace(r"\d+","", regex=True) # Se reemplazan números por espacios vacíos
    # Como no se tienen en cuenta las fechas se eliminan meses y dias de la semana
    df_bd[col] = df_bd[col].replace(r"enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre|lunes|martes|miercoles|jueves|viernes|sabado|domingo", "", regex=True)
    # Se eliminan espacios vacíos dobles en el texto con las transformaciones anteriores
    df_bd[col] = df_bd[col].str.split().str.join(' ')
    # Se eliminena las palabras con menos de dos caracteres
    df_bd[col] = df_bd[col].apply(lambda x: ' '.join([word for word in x.split() if len(word) >= 2]))


# Se implementa la función eliminar Stopwords
df_bd['new_title_content'] = df_bd['new_title_content'].apply(lambda x: eliminar_stopwords(x))

# Se realiza el stemming
df_bd_stemming = df_bd.copy()
df_bd_stemming['new_title_content'] = df_bd_stemming['new_title_content'].apply(lambda x: realizar_stemming(x))


# Se realiza la lematización
df_bd_lemat = df_bd.copy()
df_bd_lemat['new_title_content'] = df_bd_lemat['new_title_content'].apply(lematizar)


# defina el servidor para llevar el registro de modelos y artefactos
# mlflow.set_tracking_uri('http://localhost:5000')
# registre el experimento
experiment = mlflow.set_experiment("LDA_Clasificador")

# Aquí se ejecuta MLflow sin especificar un nombre o id del experimento. MLflow los crea un experimento para este cuaderno por defecto y guarda las características del experimento y las métricas definidas. 
# Para ver el resultado de las corridas haga click en Experimentos en el menú izquierdo. 
with mlflow.start_run(experiment_id=experiment.experiment_id):
    # defina los parámetros del modelo
    n_estimators = 200 
    max_depth = 6
    max_features = 4
    # Cree el modelo con los parámetros definidos y entrénelo
    rf = RandomForestRegressor(n_estimators = n_estimators, max_depth = max_depth, max_features = max_features)
    rf.fit(X_train, y_train)
    # Realice predicciones de prueba
    predictions = rf.predict(X_test)
  
    # Registre los parámetros
    mlflow.log_param("num_trees", n_estimators)
    mlflow.log_param("maxdepth", max_depth)
    mlflow.log_param("max_feat", max_features)
  
    # Registre el modelo
    mlflow.sklearn.log_model(rf, "random-forest-model")
  
    # Cree y registre la métrica de interés
    mse = mean_squared_error(y_test, predictions)
    mlflow.log_metric("mse", mse)
    print(mse)