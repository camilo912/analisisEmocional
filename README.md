# Análisis emocional - Big Data

# Introducción:

Este es un proyecto realizado para el curso tópicos especiales en telemática que trata de poner en practica los conocimiento adquiridos sobre la unidad de big data.La problemática que se busca atacar es la de realizar la técnica de análisis de sentimientos (determinar si un texto es positivo, negativo, o neutro) a los comentarios hechos a diferentes tipos de aerolíneas con respecto a su servicio.

Identificamos la siguiente pregunta de negocio: ¿Existe un correlación entre las estrellas y el análisis de sentimientos  de los comentarios?
A partir de ella realizaremos todo el ciclo de vida de un proyecto de big data.

El conjunto de datos que se utilizará pertenecen al siguiente archivo: airlines.csv

  Integrantes:
  
    - Juan Camilo Henao Salazar.
    
    - Juan Fernando Rincón Cardeño.
    
    - Juan Diego Zuluaga Gallo.

# Adquisición y preparación de datos:

El archivo de datos que se utiliza para realizar el proceso contiene la siguiente información:
id,aerolínea,Fecha,Localización,rating,cabina,valor,recomendaciones,revisión.

Este archivo se carga en el HDFS.


Se asume el csv inicial está en la misma carpeta que getTrain.py y el getTest.py
```
python getTrain.py > traindata.csv
python getTest.py > testdata.csv
```
Todo esto genera los csv que se le van a entregar a Spark.

Luego se cargan estos dos archivos a HDFS.

Luego, para este conjunto de datos se hace un proceso de limpieza o cleaning solo a la revisión o comentario que consiste en:

- Poner todo el texto en minúscula.
- Eliminar todos los signos de puntuación -> "!@#$?/.;:()[]\{\},&%¡¿°|¬^~\"".
- Eliminar todos los Stopwords.
- Stemming -> Diferenciar la raíz de la palabra, se hizo utilizando la librería nltk(natular language tool kit).
- lemmatization -> Juntar palabras diferentes que significan lo mismo, también se hizo utilizando nltk.
- Vectorización.


# Implementación y almacenamiento:

Para realizar todo el proceso de implemenación se utilizará Spark y Mllib. 

Mllib es una biblioteca de machine learning que permitirá utilizar un clasificador de regresión logistica que permita para entrenar el modelo. 

Debido a que la técnica de análisis de sentimientos requiere de un modelo supervisado, el equipo se dividió el trabajo de taggear los 992 comentarios en una distribución de 331,331,330. 

En primera instacia se aprovecho el preprocesamiento que se había realizado en la etapa previa, buscando que el output de este preprocesamiento fuera únicamente los datos importantes para el modelo, asi que se organizo esta data siendo principalmente el vector final de palabras que generaba el modelo previamente, además se tenía el dato final que era la emoción, la cual podía caber en 3 categorías (sad, normal, happy --> 0, 1, 2), buscando que cada id estuviera clasificado y tuviera su respectivo label, para realizar un modelo supervisado. También se separo la data en 2 archivos diferentes, un train.csv y un test.csv, buscando que fuera respectivamente el archivo de entrenamiento y el archivo de test del modelo.

Los archivos necesarios fueron guardados en HDFS, para poder permitir el procesamiento desde el DCA con spark, una vez estaban guardados los archivos en HDFS, se aseguraba el acceso desde el DCA, por lo que se realizo el modelo, el modelo realizado fue un LogisticRegressionWithLBFGS en pyspark, el cual leia el archivo de training para entrenar, separaba la información en su respectivo Label y  features, y se entrenaba el modelo con estos datos, una vez entrenado se accedia al segundo archivo, el de test, con el cual se verificaban los resultados de este y se guardaban en un archivo, con formato de (resultado real, predicción), para poder manejar estos datos, y que se pueda realizar análitica sobre estos en el subsistema de Visualización.

Para continuar con el procedimiento de uso se conecta con el DCA, y se lleva el archivo modelSpark.py para allá.
```
pyspark modelSpark.py
```
Esto creará un nuevo archivo en el HDFS que tendrá el Output del modelo. Este Output se trae localmente a la misma carpeta donde esté cuteOutput.py.

```
python cuteOutput.py > finalOutput.csv
```
Esto genera un nuevo archivo csv que se utilizará para la visualización.

# Visualización:

Para el proceso de visualización se está utilizando neo4j.

Para correr el neo4j se debe hacer:

Instalar el cliente de neo4j:


```
sudo pip install neo4jrestclient
```

Correr el siguiente programa para cargar los datos del csv al neo4j:

```
python display.py
```

Ahora, el usuario puede acceder al servidor de neo4j por medio del localhost:7474.

desde allí puede realizar los siguientes comando para obtener la visualización de los datos y la información:

  - MATCH (n)-[r]->(m) RETURN n, r, m;  -> Mostrar los datos en un grafo
  
    ![query1](/images/Query1.png)
  
  - MATCH (n)-[r]->(m)-[q]->(f) RETURN n.name, m.name, f.name; Mostrar todos los datos en una tabla
  
    ![query2](/images/Query2.png)
  
  - MATCH (n)-[r]->(m)-[q]->(f) where f.name in ['Existe correlacion'] RETURN n.name, m.name, f.name;-> Mostrar todos los datos en donde existe correlación.
  
    ![query3](/images/Query3)
  
    
    Como se puede observar, en el último query aparecen todos los registros en donde existe una correlación entre el rating y la predicción del modelo. En total hay 126 registros que representa el 63.36% de aciertos. 
  


# Marco teórico: 

El Análisis de Sentimiento es el área del Procesamiento del Lenguaje Natural (PLN) que trata de resolver el problema de que muchos de los datos que generamos los humanos de una manera desestructurada y ambigua, demuestra ciertas emociones gustos que resultan ser complejos de analizar. El objetivo es que una máquina, un programa, sea capaz de distinguir el sentimiento que se esconde tras una opinión vertida en una red social, como por ejemplo Twitter o Facebook; que sea capaz de clasificarlo y resumir todo su proceso mostrando un resultado claro y simple.
Si mezclamos este proceso, con la posibilidad que tenemos de procesar grandes cantidades de datos mediante técnicas de Big Data, nos daremos cuenta que el ámbito de actuación sobre el que podemos movernos es muy amplio.
Por tanto, parece claro que existe una combinación perfecta entre las técnicas de Big Data para extraer cantidades masivas de datos, las técnicas de PLN para analizar y estructurar esos datos y las técnicas de Inteligencia Artificial para clasificar y categorizar dichos datos.

¿Cómo analizar el sentimiento?

Los algoritmos de análisis de sentimiento se componen básicamente de tres fases:

1. Recolección y almacenamiento del conjunto de datos:
    En esta fase podemos utilizar técnicas de Big Data para recolectar cantidades masivas de datos que serán procesadas posteriormente.
    
2. Preprocesado de los datos:

    1. Normalización de los datos mediante la Tokenización:
    se divide todo el texto que va a procesarse en entidades mínimas con significado denominadas tokens. Habitualmente el     texto se divide primero en frases y posteriormente en palabras. De esta forma, la fase posterior (POS Tagging) puede realizar un análisis sintáctico de cada frase.
Al finalizar esta fase se obtiene un conjunto de tokens (frases y palabras).

    1. Etiquetado POS Tagging:
    Partiendo de los tokens (frase) se lleva a cabo el análisis sintáctico, y posteriormente se clasifica cada token (palabra) en función de su categoría gramatical: Nombre, pronombre, verbo, adjetivo, …
De esta fase se obtiene un árbol de etiquetado gramatical.

    1. Extracción de características:
     En esta fase se analizan las negaciones en el lenguaje y se selecciona qué palabras van a utilizarse para la clasificación de sentimientos posterior (sólo los nombres, todas las palabras, los verbos, …)
En base a esto, se asigna sentimiento a cada token individual, para, en la fase posterior, tratar de inferir el sentimiento global de todo el texto.
  
3. Clasificación del sentimiento:

  Una vez que se dispone del texto tokenizado y analizado, la última fase trata de inferir el sentimiento global del texto.
  Para ello se utilizan diferentes técnicas entre las que se encuentran: técnicas automáticas y técnicas manuales.
  Las técnicas automáticas tienen un cierto rango de error en la inferencia del sentimiento, pero tienen la gran ventaja de ser procesos desatendidos que al finalizar nos ofrecerán el resultado que buscábamos (o al menos uno aproximado). Estas técnicas utilizan algoritmos para llevar a cabo su labor. Los algoritmos más utilizados son: Naïve Bayes, Entropía máxima, SVM (Support Vector Machine).
  Las técnicas manuales tienen un rango de precisión mucho mayor, ya que son las propias personas las encargadas de establecer el sentimiento del texto. Tienen la gran pega de que no siempre es posible disponer del tiempo de las personas para llevar a cabo esta tarea y conforme el tamaño de los datos aumente, este proceso se antoja más complicado.



# Webgrafía (Código de Honor):

Codementor.io. (2018). Spark & Python: MLlib Logistic Regression | Codementor. [online] Available at: https://www.codementor.io/jadianes/spark-mllib-logistic-regression-du107neto [Accessed 24 May 2018]. (Fuente principal y de ejemplo para el código)

Bonzanini, M. (2018). Getting started with Neo4j and Python. [online] Marco Bonzanini. Available at: https://marcobonzanini.com/2015/04/06/getting-started-with-neo4j-and-python/ [Accessed 25 May 2018].

BEEVA | Soluciones de tecnología e innovación para empresas. (2018). BigData y el Análisis del Sentimiento - BEEVA | Soluciones de tecnología e innovación para empresas. [online] Available at: https://www.beeva.com/beeva-view/innovacion/bigdata-y-el-analisis-del-sentimiento-2/ [Accessed 25 May 2018].

