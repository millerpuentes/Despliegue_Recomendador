![UNIANDES](Imagenes/image_UNIANDES.png)

## CLASIFICADOR Y RECOMENDADOR DE NOTICIAS PARA CLIENTES CORPORATIVOS DEL SECTOR BANCARIO

![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
[![Build Status](https://travis-ci.org/anfederico/clairvoyant.svg?branch=master)](https://travis-ci.org/freddy120/MIAD_no_supervisado_project)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub Issues](https://img.shields.io/github/issues/freddy120/MIAD_no_supervisado_project.svg)](https://github.com/freddy120/MIAD_no_supervisado_project/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Tabla de Contenido

- [Resumen](#resumen)
- [1. Introducción](#1-introducción)
- [2. Descripción de los Datos del proyecto](#2-descripción-de-los-datos-del-proyecto)
- [3. Metodología](#3-metodología)
- [4. Modelamiento](#4-modelamiento)
- [5. Recomendador](#5-recomendador)
- [6. Conclusiones](#6-conclusiones)
- [7. Referecias](#7-referencias)


## Resumen

Como parte de la estrategia comercial y de fidelización de clientes en una entidad bancaria, se desarrolló una herramienta informativa basada en aprendizaje automático para ofrecer a los clientes recomendaciones de noticias relevantes y confiables de acuerdo a su sector. Se analizó una base de datos vinculando información de clientes y noticias mediante algoritmos de PLN, dada su composición textual predominante. La clusterización temática de las noticias se efectuó con el modelo LDA de Gensim, evaluando su eficacia tanto con textos lematizados como con Stemming. Se realizó además una recategorización de clientes para afinar las recomendaciones según la relevancia temática para cada sector. En conclusión, el recomendador logra proporcionar información valiosa, siendo más eficaz con textos lematizados para la clasificación de noticias.


**Palabras clave**: Procesamiento del lenguaje natural, clusterización, aprendizaje no supervisado, LDA. 


## Estructura de Archivos:
* [BD](https://github.com/millerpuentes/Despliegue_Recomendador/tree/main/BD): Script de python para cargar los datos a la Base de Datos.
* [Data](https://github.com/millerpuentes/Despliegue_Recomendador/tree/main/Data): Carpeta donde reposa toda la trazabilidad de los datos trabajados a lo largo del proyecto, se tiene la trazabilidad con ayuda de la herramienta DVC.
* [Dev](https://github.com/millerpuentes/Despliegue_Recomendador/tree/main/Dev): En esta carpeta se tienen los Notebooks de Jupiter en los cuales se realizó el EDA, Modelamiento y se generó la primera versión del recomendador.
* [Front](https://github.com/millerpuentes/Despliegue_Recomendador/tree/main/Front): Esta carpeta contiene el tablero utilizado para disponibilizar el recomendador, programado en Python con la librería Dash.
* [Imagenes](https://github.com/millerpuentes/Despliegue_Recomendador/tree/main/Imagenes): Contiene las imágenes utilizadas a lo largo del proyecto.
* [Model](https://github.com/millerpuentes/Despliegue_Recomendador/tree/main/Model): Esta carpeta contiene los dos modelos utilizados en la herramienta MLflow y sus respectivos experimentos que se utilizaron para obtener los mejores hiperparámetros para definir los temas. 


## 1. Introducción

La transformación de modelos de negocio tradicionales hacia enfoques más digitales e inteligentes es un imperativo en la actual industria financiera, donde los datos son el recurso principal para el desarrollo de nuevas tecnologías. (Bellina & Arellano, 2022).

Este proyecto aborda el desarrollo de un sistema recomendador de noticias para segmentos de clientes corporativos del banco, con el propósito de informar acerca de novedades y sucesos relevantes para sus sectores. El procedimiento incluyó la preparación de datos de texto mediante técnicas de PLN y una revisión detallada de literatura para la implementación de algoritmos de clusterización, donde el modelo LDA de la librería Gensim fue destacado como una herramienta superior para el modelado de temas. (Grisales-Aguirre & Figueroa-Vallejo, 2022, 282). Otros métodos explorados, como los modelos de K-medias y la paquetería Transformers, no superaron al LDA en eficacia.

En conclusión, el sistema recomendador, basado en LDA con texto lematizado, logra asignar prioridades de noticias efectivamente según los segmentos de clientes y los temas de interés sugeridos, como macroeconomía y sostenibilidad, entre otros. La solución diseñada permitiría su integración en plataformas de banca en línea, facilitando la comunicación de información de manera periódica.


## 2. Descripción de los Datos del proyecto

**Modelo Relacional de los datos**
![Diagrama Relacional](../Imagenes/Diagrama_relacional.png)

Se utilizaron los set de datos porporcionados por el Centro de Analítica de Bancolombia, disponible en Kaggle, compuesto por tres archivos CSV interconectados por dos claves principales. El archivo “clientes.csv” detalla información de los clientes del banco, “noticias.csv” lista títulos, identificadores, URLs, fechas y contenidos de noticias, y “clientes_noticias.csv” vincula clientes con noticias mediante identificadores.

Para facilitar el manejo de la información, se consolidó un dataframe que incluye identificadores de clientes y noticias, nombres, subsectores, títulos, URLs y contenidos. Durante la limpieza del dataframe, se descubrieron y gestionaron varias inconsistencias y duplicidades, resultando en 960 clientes únicos con al menos una noticia asociada.


## 3. Metodología

El contenido de las noticias fue procesado mediante algoritmos de PLN para eliminar números, acentos, caracteres especiales, letras mayúsculas, así como palabras referentes a días y meses, dado que las fechas no fueron consideradas. El objetivo era mitigar el impacto que dichos elementos temporales podrían tener en la agregación por temas. Se empleó NLTK para eliminar Stopwords en español y palabras de menos de dos caracteres.

Para extraer las características esenciales de cada noticia, se implementaron en paralelo dos métodos de reducción de palabras a su raíz: Stemming y Lematización. El primero, eliminando prefijos y sufijos tras la tokenización de las noticias usando Snowball Stemmer de NLTK; y el segundo, reduciendo palabras a su lema base con WordNetLemmatizer de NLTK.

## 4. Modelamiento

Para realizar el modelamiento de los temas en las noticias, se tomaron los datos a los que se les aplicó Stemming y Lematización, se separó cada palabra individualmente buscando sus tokens por medio de word_tokenize de NLTK. Se filtraron las palabras que aparecían en más del 50% de las noticias o en menos de 20 de ellas con filter_extremes de Gensim. Finalmente, se generaron bolsas de palabras únicas con sus respectivas frecuencias (corpus) mediante doc2bow de Gensim. 

Con el propósito de evaluar el desempeño de la agrupación de textos bajo estos dos contextos (Stemming y Lematización), se desarrollaron dos modelos LDA para la estimación de los clústeres. Para definir el número de temas asociados a las noticias que se deben incluir en los modelos, se aplicó la medida de coherencia (en su punto más alto) y perplejidad (en su punto más bajo).

Para ello se diseñó un experimento en python, guardando su trazabilidad con ayuda de la herramienta mlflow. Dicho experimento consistía en iterar sobre 3 de los hiperparámetros más relevantes que son: 

**chunksize:** determina la cantidad de documentos procesados a la vez durante el entrenamiento. Un valor más alto puede acelerar el entrenamiento, pero también puede requerir más memoria. Específicamente, afecta la eficiencia del procesamiento del corpus durante cada iteración.

**num_topics:** establece la cantidad de tópicos que el modelo intentará identificar en el corpus. Es crucial elegir un número apropiado de tópicos que refleje la complejidad y diversidad del conjunto de datos. Valores más altos pueden capturar más detalles, pero también pueden llevar a tópicos superpuestos o poco distintos.

**passes:** representa la cantidad de veces que el modelo recorre todo el corpus durante el entrenamiento. Un valor más alto puede mejorar la calidad del modelo al permitirle ajustarse mejor a los datos, pero también puede aumentar el tiempo de entrenamiento. Es una especie de medida de la paciencia del modelo para aprender de los datos.

![Resultados](../Imagenes/resultados_modelos.png)



Posteriormentes de crea una función en python para evaluar las diferentes configuraciones con respecto a los temas con las que se identificó que la cantidad de temas ideal en estas dos métricas fue 16 acorde a los rangos evaluados para el modelo con Stemming.Al realizar el proceso al corpus con Lematización, la máxima coherencia entre los temas y baja perplejidad se alcanza cuando los temas son 19 para el rango evaluado.

La representación gráfica de los temas encontrados para las palabras trabajadas por Stemming se pueden visualizar con pyLDAvis en un plano de dos componentes principales:

![Temas Stemming](../Imagenes/topicos_stemming.png)

En el que la mayoría de los temas aparecen claramente diferenciados. Los traslapes observados en los temas 2 y 5 probablemente no ocurren en una vista tridimensional, confirmado durante el análisis para la asignación de categorías.

Para el modelo LDA - lematizado se asignaron palabras clave a cada clúster de noticias, se visualizaron los resultados al igual que con los datos trabajados por Stemming con la librería pyLDAvis (19 temas):

![Temas Lematizados](../Imagenes/topicos_lematizados.png)

Aquí, aunque la mayoría de los temas están bien definidos, los temas 2, 4, 8, y 10 presentan traslapes y requieren verificación manual durante la asignación de categorías. Las Figuras 6 y 7 revelan similitudes en las agrupaciones entre ambos métodos, como el tema 1 en Stemming correlacionado con el tema 9 en Lematización, esta similitud se identificó mediante inspección manual.

Luego de la identificación de los temas se procedió a asignar de manera manual la correspondencia de acuerdo a las categorías de las noticias como lo muestra la siguiente tabla:

<p align="center">
  <img width="480" height="300" src="../Imagenes/categoria_temas.png" alt="Categorías por temas">
</p>


Con la asignación por temas se le asignó una relevancia a las noticias de acuerdo al sector en que se encontraba el cliente (Salud o Industrial):

<p align="center">
  <img width="480" height="300" src="../Imagenes/relevancia_sector.png" alt="Relevancia de noticia por Sector">
</p>


### 5. Recomendador

Finalmente se desarrolló un recomendador basado en el NIT del cliente para identificar el sector al que pertenece y asignar la relevancia de las noticias correspondientes. Se seleccionan de forma aleatoria las noticias de la fecha que el cliente selecciona, exceptuando las categorizadas como ‘Otra’ por su irrelevancia para el negocio, y por ende, no se sugieren al cliente. 

Este procedimiento se realizó sólo con el set de datos de Stemming, ya que presentó mejor desempeño.

Para ilustrar la salida de las recomendaciones obtenidas por cada método se selecciona un cliente que pertenece al sector industrial y otro al sector salud, a los dos se le recomienda las 5 noticias conforme a sus preferencias:

Sector salud:

![Noticias Sector Salud - Stemming](../Imagenes/clientes_sector_salud.png)

Sector Industrial:

![Noticias Sector Industrial - Stemming](../Imagenes/clientes_sector_industrial.png)

El recomendador está seleccionando de manera adecuada la priorización de noticias para el cliente en cuestión, mostrando la calidad de las noticias clasificadas con respecto al tema etiquetado, logrando clasificaciones coherentes y precisas.

### 6. Conclusiones

Este proyecto resalta la importancia crítica de los datos en la transformación de la industria financiera hacia modelos más digitales e inteligentes, aplicando técnicas avanzadas de procesamiento del lenguaje natural para desarrollar un recomendador de noticias efectivo y preciso. La elección del modelo LDA, validada tras una revisión exhaustiva de diferentes técnicas, se comprobó adecuada, especialmente cuando se aplicaba a textos lematizados, proporcionando clasificaciones en temáticas coherentes y precisas. Dado que los modelos LDA reciben como parámetro el número de tópicos, es fundamental seleccionar un criterio de evaluación que permita estimar la cantidad correcta, en este caso,  las medidas de coherencia y perplejidad.

La posible integración del sistema en plataformas de banca en línea promete ser un avance significativo en la comunicación periódica de información pertinente a clientes corporativos, alineando las recomendaciones con los segmentos de clientes y la relevancia temática para cada sector. Este método optimiza la pertinencia de la información compartida y refuerza las estrategias de fidelización mediante el enfoque en necesidades informativas específicas de los clientes.

En cuanto a la evaluación, debido al enfoque de aprendizaje no supervisado del proyecto, se propone llevar a cabo encuestas de NPS para obtener insights claros sobre la satisfacción y precisión en las recomendaciones del modelo. Se sugiere implementar pruebas con cuatro grupos de control estratificados según el sector. Cada grupo recibe recomendaciones del modelo entrenados, permitiendo así una evaluación comparativa integral, respaldada por métricas de NPS y feedback de los usuarios. Este método detallado de evaluación busca no solo medir la efectividad del modelo, sino también afinar continuamente el sistema basándose en las respuestas y preferencias del usuario.


## 7. Referencias

- Bellina, J. C., & Arellano, N. (2022, Septiembre 22). Los retos que traen las nuevas tecnologías en el sector financiero. EY. Retrieved Agosto 25, 2023, from https://www.ey.com/es_pe/banking-capital-markets/retos-nuevas-tecnologias-sector-financiero

- Beregovskaya, I., & Koroteev, M. (2021, 09 27). Review of Clustering-Based Recommender Systems. arxiv, 2109(Computer Science), 22. https://arxiv.org/abs/2109.12839. https://arxiv.org/abs/2109.12839

- Carrera-Trejo, J. V., & Cadena-Martínez, R. (2022). Identificacion de tópicos en un corpus utilizando Transformers. Computación y Sistemas, 26(3), 1093 - 1105. 10.13053/CyS-26-3-4187
 
- Grisales-Aguirre, A. M., & Figueroa-Vallejo, C. J. (2022). Modelado de tópicos aplicado al análisis del papel del aprendizaje automático en revisiones sistemáticas. Revista de Investigación, Desarrollo e Innovación, 12(2), 279 - 292. https://doi.org/10.19053/20278306.v12.n2.2022.15271

- Miranda, L., Viterbo, J., & Bernardini, F. (2020, 08 10). Towards the Use of Clustering Algorithms in Recommender Systems. AIS Electronic Library, 2020(Americas Conference on Information Systems), 11. https://core.ac.uk/download/pdf/326836383.pdf


### Desarrolladores: 
<p align="center">
  <img width="200" src="Imagenes/image_Joan.png" alt="Joan Esteban Chacón">
</p>
<p align="center">
  <b>Joan Esteban Chacón</b>
</p>
<p align="center">
  <img width="200" src="Imagenes/image_Grace.png" alt="Grace Gonzalez">
</p>
<p align="center">
  <b>Grace Gonzalez</b>
</p>

<p align="center">
  <img width="200" src="Imagenes/image_Catalina.png" alt="Catalina Cárdenas">
</p>
<p align="center">
  <b>Catalina Cárdenas</b>
</p>

<p align="center">
  <img width="200" src="Imagenes/image_MP.png" alt="Miller Puentes">
</p>
<p align="center">
  <b>Miller Puentes</b>
</p>

<p align="center">
  <img width="450" height="150" src="Imagenes/image_MIAD.png" alt="MIAD">
</p>
