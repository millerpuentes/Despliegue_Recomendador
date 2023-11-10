#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Equipo 7 - DSA
"""

# Importaciones aquí
import pandas as pd
import numpy as np
import spacy
from nltk.corpus import stopwords
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.models import CoherenceModel
import nltk
import mlflow
import mlflow.sklearn


#Empieza el desarrollo

# Asegúrate de que estas descargas de nltk se ejecuten una sola vez.
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')

def main():
    # Cargar el modelo de spacy para el español
    nlp = spacy.load("es_core_news_sm")

    # Obtener las stopwords en español
    stopwords_lista = stopwords.words('spanish')

    # Importe el conjunto de datos
    df_clientes = pd.read_csv('../Data/clientes.csv')
    df_clientes_noticias = pd.read_csv('../Data/clientes_noticias.csv')
    df_noticias = pd.read_csv('../Data/noticias.csv')

    # LDA - Stemming
    # Se importa el archivo
    df_bd_stemming = pd.read_csv('../Data/DC_stemming.csv')
    # Se tokeniza el texto
    tokens_stemming = [nltk.word_tokenize(texto) for texto in df_bd_stemming['new_title_content']]
    # Creamos la representación de diccionario del documento
    dictionary_stemming = Dictionary(tokens_stemming)
    # Se remueven las palabras que aparecen en menos de 20 documentos y más del 50% de los documentos
    dictionary_stemming.filter_extremes(no_below=20, no_above=0.5)
    # Se vectoriza el documento para crear el corpus con la matriz de frecuencia
    corpus_stemming = [dictionary_stemming.doc2bow(doc) for doc in tokens_stemming]

    # defina el servidor para llevar el registro de modelos y artefactos
    # mlflow.set_tracking_uri('http://localhost:5000')
    # registre el experimento
    experiment = mlflow.set_experiment("LDA_Clasificador") 

    with mlflow.start_run(experiment_id=experiment.experiment_id):
        # defina los parámetros del modelo
        corpus = corpus_stemming
        id2word = dictionary_stemming
        num_topics = 16
        chunksize = 1000
        passes = 20
        iterations = 400
        alpha = 'auto'
        eta = 'auto'
        random_state = 123
        eval_every = None

        # Cree el modelo con los parámetros definidos y entrénelo
        LDA_stemming = LdaModel(
            corpus=corpus,
            id2word=id2word,
            num_topics=num_topics,
            chunksize=chunksize,
            passes=passes,
            iterations=iterations,
            alpha=alpha,
            eta=eta,
            random_state=random_state,
            eval_every=eval_every
        )
  
        # Registre los parámetros
        mlflow.log_param("num_topics", num_topics)
        mlflow.log_param("chunksize", chunksize)
        mlflow.log_param("passes", passes)
  
        # Registre el modelo
        mlflow.sklearn.log_model(LDA_stemming, "LDA_stemming_1")
  
        # Cree y registre la métrica de interés   
        cm = CoherenceModel(model=LDA_stemming, texts=tokens_stemming, dictionary=dictionary_stemming, coherence='c_v')
        coherence = cm.get_coherence()
        mlflow.log_metric("coherence", coherence)

        perplexity = LDA_stemming.log_perplexity(corpus)
        mlflow.log_metric("perplexity", perplexity)
    
        print(perplexity)
        print(coherence)

# Este bloque se asegura de que main() se ejecute solo cuando este script se corre directamente.
if __name__ == '__main__':
    main()
