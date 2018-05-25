# from pyspark import SparkConf, SparkContext
# from pyspark.mllib.regression import LabeledPoint
# from pyspark.mllib.classification import LogisticRegressionWithLBFGS
# from numpy import array
# from time import time
#
# conf = SparkConf().setAppName('example_app').setMaster('local[8]')
# sc = SparkContext(conf=conf)
# data_file = "datasets/saved.csv"
# raw_data = sc.textFile(data_file)
# header = raw_data.take(1)[0]
# total_data = raw_data.filter(lambda line: line != header)
# total_data_len = total_data.count()
# train_data_len = int(total_data.count()*0.8)
# test_data_len = total_data_len - train_data_len
# train_data = sc.parallelize(raw_data.take(total_data_len + 1)[1:train_data_len+1])
# test_data = sc.parallelize(raw_data.take(total_data_len + 1)[train_data_len + 1:])
#
# def parse_interaction(line):
#     line_split = line.split(",")
#     clean_line_split = line_split[5] + line_split[7]
#     feeling = 0.0
#     if line_split[10]=='normal':
#         feeling = 1.0
#     # elif line_split[10]=='happy':
#     #     feeling = 2.0
#     return LabeledPoint(feeling, array([float(x) for x in clean_line_split]))
#
# training_data = train_data.map(parse_interaction)
# testing_data = test_data.map(parse_interaction)
#
# t0 = time()
# logit_model = LogisticRegressionWithLBFGS.train(training_data)
# tt = time() - t0
#
# print ("Classifier trained in {} seconds".format(round(tt,3)))
#
# # print("Total data + header size is {}".format(raw_data.count()))
# # #print("Total data size is {}".format(total_data.count()))
# # #print(int(total_data.count()*0.8))
# # #print(len(train_data), "aca")
# # #print(type(header), "tipo -1")
# # #print(type(raw_data), "tipo 0")
# # #print(type(total_data), "tipo 1")
# # #print(train_data[1], train_data[2], train_data[3], train_data[4])
# # #print(type(train_data), "tipo 2")
# # print(len(train_data))
# # #print(train_data[792])
# # print("test data: *************")
# # #print(type(test_data), "tipo 3")
# # print(len(test_data))
# # print(total_data_len - train_data_len)
# # print(test_data_len)
# #print(test_data[0])
# #print("Total train data size is {}".format(train_data.count()))

# ############### Segunda implementación #############3
# from pyspark.ml.classification import LogisticRegression
#
# # Load training data
# training = spark \
#     .read \
#     .format("libsvm") \
#     .load("data/mllib/sample_multiclass_classification_data.txt")
#
# lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)
#
# # Fit the model
# lrModel = lr.fit(training)
#
# # Print the coefficients and intercept for multinomial logistic regression
# print("Coefficients: \n" + str(lrModel.coefficientMatrix))
# print("Intercept: " + str(lrModel.interceptVector))

# ################ Tercera implementación ##################
# from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
# from pyspark.mllib.regression import LabeledPoint
#
# # Load and parse the data
# def parsePoint(line):
#     values = [float(x) for x in line.split(' ')]
#     return LabeledPoint(values[0], values[1:])
#
# data = sc.textFile("data/mllib/sample_svm_data.txt")
# parsedData = data.map(parsePoint)
#
# # Build the model
# model = LogisticRegressionWithLBFGS.train(parsedData)
#
# # Evaluating the model on training data
# labelsAndPreds = parsedData.map(lambda p: (p.label, model.predict(p.features)))
# trainErr = labelsAndPreds.filter(lambda (v, p): v != p).count() / float(parsedData.count())
# print("Training Error = " + str(trainErr))
#
# # Save and load model
# model.save(sc, "target/tmp/pythonLogisticRegressionWithLBFGSModel")
# sameModel = LogisticRegressionModel.load(sc,
#                                          "target/tmp/pythonLogisticRegressionWithLBFGSModel")


# #################### implementación quinta ################ Aprovada, checked
# from pyspark import SparkConf, SparkContext
# from pyspark.mllib.regression import LabeledPoint
# from pyspark.mllib.classification import LogisticRegressionWithLBFGS
# from numpy import array
# from time import time
#
# conf = SparkConf().setAppName('example_app').setMaster('local[8]')
# sc = SparkContext(conf=conf)
#
# data_file = "datasets/trainAirlines.csv"
# raw_data = sc.textFile(data_file)
# header = raw_data.first()
# raw_data = raw_data.filter(lambda x:x != header)
#
# test_data_file =  "datasets/testAirlines.csv"
# test_raw_data = sc.textFile(test_data_file)
# test_header = test_raw_data.first()
# test_raw_data = test_raw_data.filter(lambda x:x != test_header)
#
# def parse_interaction(line):
#     line_split = line.split(",")
#     clean_line_split = []
#     clean_line_split.append(line_split[5])
#     clean_line_split.append(line_split[7])
#     feeling = 0.0
#     if line_split[10]=='normal':
#         feeling = 1.0
#     elif line_split[10]=='happy':
#          feeling = 2.0
#     return LabeledPoint(feeling, array([float(x) for x in clean_line_split]))
#
# training_data = raw_data.map(parse_interaction)
# test_data = test_raw_data.map(parse_interaction)
# print(training_data.take(1))
#
# t0 = time()
# logit_model = LogisticRegressionWithLBFGS.train(training_data, numClasses=3)
# tt = time() - t0
#
# labels_and_preds = test_data.map(lambda p: (p.label, logit_model.predict(p.features)))
#
# t0 = time()
# test_accuracy = labels_and_preds.filter(lambda v: v[0] == v[1]).count() / float(test_data.count())
# #test_accuracy = labels_and_preds.filter(lambda v: 1.0 == v).count() / float(test_data.count())
# tt = time() - t0
#
# print("Prediction made in {} seconds. Test accuracy is {}".format(round(tt,3), round(test_accuracy,4)))
#
# # ################ implementación sexta ##############
# # from pyspark.ml.classification import LogisticRegression
# # from pyspark import SparkConf, SparkContext
# #
# # conf = SparkConf().setAppName('example_app').setMaster('local[8]')
# # sc = SparkContext(conf=conf)
# #
# # # Load training data
# # training = sc \
# #     .read \
# #     .format("libsvm") \
# #     .load("datasets/trainAirlines.csv")
# #
# # lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)
# #
# # # Fit the model
# # lrModel = lr.fit(training)
# #
# # # Print the coefficients and intercept for multinomial logistic regression
# # print("Coefficients: \n" + str(lrModel.coefficientMatrix))
# # print("Intercept: " + str(lrModel.interceptVector))

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

conf = SparkConf().setAppName('example_app').setMaster('local[8]')
sc = SparkContext(conf=conf)

# data_file = "datasets/trainAirlines.csv"
data_file = "trainAirlines.csv"
raw_data = sc.textFile(data_file)
header = raw_data.first()
raw_data = raw_data.filter(lambda x:x != header)

# test_data_file =  "datasets/testAirlines.csv"
test_data_file =  "testAirlines.csv"
test_raw_data = sc.textFile(test_data_file)
test_header = test_raw_data.first()
test_raw_data = test_raw_data.filter(lambda x:x != test_header)

# stop_words = sc.textFile("datasets/stopWordsEN.txt").take(994)
stop_words = sc.textFile("stopWordsEN.txt").take(994)
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
    words = comment.split(" ")
    taggedwords = nltk.pos_tag(words)
    newWords = []
    for word, tag in taggedwords:
        tagtype = get_wordnet_pos(tag)
        if (tagtype != ''):
            newWord = WL.lemmatize(word,tagtype)
            newWords += [newWord]
    return " ".join(newWords)

def parse_interaction(line):
    line_split = line.split(",")
    if(line_split[8].lower() == "yes"):
        line_split[8] = 1.0
    else:
        line_split[8] = 0.0
    line_split[9] = line_split[9].lower()
    line_split[9] = removeMarks(line_split[9])#re.sub('[!@#$?/.;:()[]\{\},&%¡¿°|¬^~_]', '', line_split[9])
    line_split[9] = removeStopWords(line_split[9])
    #print(removeStopWords(line_split[9]))
    line_split[9] = stemming(line_split[9])
    line_split[9] = lemmatization(line_split[9])
    print(line_split[9])
    clean_line_split = []
    clean_line_split.append(line_split[5])
    #clean_line_split.append(line_split[7])
    feeling = 0.0
    if line_split[10]=='normal':
        feeling = 1.0
    elif line_split[10]=='happy':
         feeling = 2.0
    return LabeledPoint(feeling, array([float(x) for x in clean_line_split]))

training_data = raw_data.map(parse_interaction)
test_data = test_raw_data.map(parse_interaction)
#print(training_data.take(1))

t0 = time()
logit_model = LogisticRegressionWithLBFGS.train(training_data, numClasses=3)
tt = time() - t0

labels_and_preds = test_data.map(lambda p: (p.label, logit_model.predict(p.features)))

t0 = time()
test_accuracy = labels_and_preds.filter(lambda v: v[0] == v[1]).count() / float(test_data.count())
#test_accuracy = labels_and_preds.filter(lambda v: 1.0 == v).count() / float(test_data.count())
tt = time() - t0

print("Prediction made in {} seconds. Test accuracy is {}".format(round(tt,3), round(test_accuracy,4)))

# ################ implementación septima ##############
# from pyspark.ml.classification import LogisticRegression
# from pyspark import SparkConf, SparkContext
#
# conf = SparkConf().setAppName('example_app').setMaster('local[8]')
# sc = SparkContext(conf=conf)
#
# # Load training data
# training = sc \
#     .read \
#     .format("libsvm") \
#     .load("datasets/trainAirlines.csv")
#
# lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)
#
# # Fit the model
# lrModel = lr.fit(training)
#
# # Print the coefficients and intercept for multinomial logistic regression
# print("Coefficients: \n" + str(lrModel.coefficientMatrix))
# print("Intercept: " + str(lrModel.interceptVector))
