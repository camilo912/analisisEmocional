# Análisis emocional - Big Data


# Introducción:

Este es un proyecto realizado para el curso tópicos especiales en telemática que trata de poner en ejecución los conocimiento adquiridos sobre la unidad de big data.La problemática que se busca atacar es la de realizar la técnica de análisis de sentimientos (determinar si un texto es positivo, negativo, o neutro) a los comentarios hechos a diferentes tipos de aerolíneas con respecto a su servicio.

Identificamos la siguiente pregunta de negocio: ¿Existe un correlación entre las estrellas y el análisis de sentimientos  de los comentarios?
A partir de ella realizaremos todo el ciclo de vida de un proyecto de big data

El conjunto de datos es: airlines.csv

El modelo/ algoritmo de analítica 
992 331 331 330

  Integrantes:
  
    - Juan Camilo Henao Salazar.
    
    - Juan Fernando Rincón Cardeño.
    
    - Juan Diego Zuluaga Gallo.

# Adquisición y preparación de datos:

El archivo de datos que se utiliza para realizar el proceso contiene la siguiente información:
id,aerolínea,Fecha,Localización,rating,cabina,valor,recomendaciones,revisión.

Este archivo se carga en el HDFS. 

Luego, para este conjunto de datos se hace un proceso de limpieza o cleaning solo a la revisión o comentario que consiste en:

- Poner todo el texto en minúscula.
- Eliminar todos los signos de puntuación -> "!@#$?/.;:()[]\{\},&%¡¿°|¬^~\"".
- Eliminar todos los Stopwords.
- Stemming -> Diferenciar la raíz de la palabra, se hizo utilizando la librería ntkl(natular language tool kit).
- lemmatization -> Juntar palabras diferentes que significan lo mismo, también se hizo utilizando ntkl.
- Vectorización.


# Implementación y almacenamiento:

Para realizar todo el proceso de implemen
Se utilizará Spark y Mllib.


# Visualización:

Para el proceso de visualización se está utilizando gephi para python.

# Marco teórico: 

.

# Webgrafía (Código de Honor):

https://www.codementor.io/jadianes/spark-mllib-logistic-regression-du107neto
