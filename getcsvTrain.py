#################### implementación sexta ################ Aprovada, desarrollo
from pyspark import SparkConf, SparkContext
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk

from numpy import array
from time import time

import ETL
import re
import pandas as pd

data_file = "trainAirlines.csv"
file_raw = open(data_file, 'r')
raw_data = file_raw.readlines()[1:]
file_raw.close()

# test_data_file =  "datasets/testAirlines.csv"
test_data_file =  "testAirlines.csv"
test_file_raw = open(test_data_file, 'r')
test_raw_data = test_file_raw.readlines()[1:]
test_file_raw.close()

#raw_data = test_raw_data

twovals = array([ETL.parse_interaction(x) for x in raw_data])

#print (twovals)
mapped_comments = array([ETL.comment_cleaner(x) for x in raw_data])
test_mapped_comments = array([ETL.comment_cleaner(x) for x in test_raw_data])

bag = ETL.bagofwords(mapped_comments,50,300)
#print (bag)

vectors = array([ETL.vectorization(x,bag) for x in mapped_comments])

for i in range(len(vectors)):
    print (",".join(map(str,vectors[i])) + "," + str(twovals[i]))
