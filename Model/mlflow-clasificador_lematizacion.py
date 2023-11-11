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


def main():

    ########################     LDA - Stemming   #############################################

    # Se importa el archivo
    df_bd_lemat = pd.read_csv('../Data/DC_lematizacion.csv')
    # Se tokeniza el texto
    tokens_lematizados = [nltk.word_tokenize(texto) for texto in df_bd_lemat['new_title_content']]
    # Creamos la representación de diccionario del documento
    dictionary_lematizados = Dictionary(tokens_lematizados)
    # Se remueven las palabras que aparecen en menos de 20 documentos y más del 50% de los documentos
    dictionary_lematizados.filter_extremes(no_below=20, no_above=0.5)
    # Se vectoriza el documento para crear el corpus con la matriz de frecuencia
    corpus_lematizados = [dictionary_lematizados.doc2bow(doc) for doc in tokens_lematizados]

    # defina el servidor para llevar el registro de modelos y artefactos
    # mlflow.set_tracking_uri('http://localhost:5000')
    # registre el experimento
    experiment = mlflow.set_experiment("LDA_Clasificador_lematizacion") 

    # Definir valores para iterar
    chunksize_values = [500, 1000, 1500]
    num_topics_values = [15, 19, 25]
    passes_values = [15, 20, 25]

    for chunksize in chunksize_values:
        for num_topics in num_topics_values:
            for passes in passes_values:
                # Configurar parámetros del modelo
                lda_params = {
                    "corpus": corpus_lematizados,
                    "id2word": dictionary_lematizados,
                    "num_topics": num_topics,
                    "chunksize": chunksize,
                    "passes": passes,
                    "iterations": 400,
                    "alpha": 'auto',
                    "eta": 'auto',
                    "random_state": 123,
                    "eval_every": None
                }
                with mlflow.start_run(experiment_id=experiment.experiment_id):
                    # Cree el modelo con los parámetros definidos y entrénelo
                    LDA_lematizacion = LdaModel(**lda_params)

                    # Registre los parámetros
                    mlflow.log_param("num_topics", num_topics)
                    mlflow.log_param("chunksize", chunksize)
                    mlflow.log_param("passes", passes)

                    # Registre el modelo
                    mlflow.sklearn.log_model(LDA_lematizacion, "LDA_Lematizacion")
                    
                    # Cree y registre la métrica de interés

                    # Coherencia   
                    cm = CoherenceModel(model=LDA_lematizacion, texts=tokens_lematizados, dictionary=dictionary_lematizados, coherence='c_v')
                    coherence = cm.get_coherence()
                    mlflow.log_metric("Coherencia", coherence)
                    print(coherence)

                    
                    # Perplejidad
                    perplexity = np.exp2(-LDA_lematizacion.log_perplexity(corpus_lematizados))
                    mlflow.log_metric("Perplejidad", perplexity)        
                    print(perplexity)
        

# Este bloque se asegura de que main() se ejecute solo cuando este script se corre directamente.
if __name__ == '__main__':
    main()