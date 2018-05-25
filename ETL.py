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
import re

import pandas as pd


data_file = "stopWordsEN.txt"
data_frame = pd.read_csv(data_file)
stop_words = data_frame.values.flatten()

marks = "!@#$?/.;:()[]\{\},&%¡¿°|¬^~_\""

def removeMarks(comment):
    sol = ""
    for i in comment:
        if not i in marks:
            sol += i
    return sol

def stemming(comment):
    ps = PorterStemmer()
    sol = ""
    comment = comment.split(" ")
    for w in comment:
        sol += ps.stem(w) + " "
    return sol[:-1]

def removeStopWords(comment):
    list = comment.split(" ")
    sol = ""
    for i in list:
        if(not i in stop_words):
            sol += i + " "
    return sol[:-1]

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

def lemmatization(comment):
    WL = WordNetLemmatizer()
    maybe = comment.split(" ")
    words = []
    for word in maybe:
        if word != "":
            words+= [word]
    taggedwords = nltk.pos_tag(words)
    newWords = []
    for word, tag in taggedwords:
        tagtype = get_wordnet_pos(tag)
        if (tagtype != ''):
            newWord = WL.lemmatize(word,tagtype)
            newWords += [newWord]
    return " ".join(newWords)

def comment_cleaner(line):
    line_split = line.split(",")
    line_split[9] = line_split[9].lower()
    line_split[9] = removeMarks(line_split[9])#re.sub('[!@#$?/.;:()[]\{\},&%¡¿°|¬^~_]', '', line_split[9])
    line_split[9] = removeStopWords(line_split[9])
    #print(removeStopWords(line_split[9]))
    line_split[9] = stemming(line_split[9])
    line_split[9] = lemmatization(line_split[9])
    return line_split[9]

def parse_interaction(line):
    #print (line)
    line_split = line.split(",")
    if(line_split[8].lower() == "yes"):
        line_split[8] = 1.0
    else:
        line_split[8] = 0.0
    clean_line_split = []

    clean_line_split.append(line_split[8])
    #clean_line_split.append(line_split[7])
    feeling = 0.0
    line_split[10] = line_split[10].strip()
    if line_split[10]=='normal':
        feeling = 1.0
    elif line_split[10]=='happy':
         feeling = 2.0
    clean_line_split.append(feeling)

    #return LabeledPoint(feeling, array([float(x) for x in clean_line_split]))
    return ",".join(map(str,clean_line_split))

def bagofwords(comments,minWords,maxWords):
    dic = {}
    for comment in comments:
        words = comment.split(" ")
        for word in words:
            if word in dic:
                dic[word] = 1 + dic[word]
            else :
                dic[word] = 1
    many = []
    rev = {}
    count = 0
    for key in dic:
        if dic[key] > minWords and dic[key] < maxWords:
            rev[key] = count
            count +=1
            many += [key]
    countfails = 0
    return (rev)

def vectorization(comment,bag):
    words = comment.split(" ")
    vector = [0]*len(bag)
    for word in words:
        if word in bag:
            vector[bag[word]]+=1
    return (vector)

def new_interaction(line):
    #print (line)
    line_split = line.split(",")
    clean_line_split.append(feeling)
    return (line_split)
