from pyspark import SparkConf, SparkContext
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import LogisticRegressionWithLBFGS

from numpy import array
from time import time
import re

conf = SparkConf().setAppName('example_app').setMaster('local[8]')
sc = SparkContext(conf=conf)

data_file = "spark/cleanSparkData.csv"
raw_data = sc.textFile(data_file)

print (raw_data)

test_data_file =  "spark/cleanSparkDataTest.csv"
test_raw_data = sc.textFile(test_data_file)

def new_interaction(line):
    #print (line)
    line_split = line.split(",")
    return LabeledPoint(float(line_split[-1]), array([float(x) for x in line_split[:-1]]))


def get_similarity(preds, stars):
    labels = []
    for i in preds:
        labels.append(i[1])
    cont = 0
    for i in range(len(labels)):
        if((labels[i] == 0 and stars[i] < 4) or (labels[i] == 1 and stars[i] < 8 and stars[i] > 3) or (labels[i] == 2 and stars[i] > 7)):
            cont += 1
    return float(cont/len(labels))

training_data = raw_data.map(new_interaction)
#print (training_data)
test_data = test_raw_data.map(new_interaction)
print(training_data.take(1))

t0 = time()
logit_model = LogisticRegressionWithLBFGS.train(training_data, numClasses=3)
tt = time() - t0

labels_and_preds = test_data.map(lambda p: (p.label, logit_model.predict(p.features)))

labels_and_preds.saveAsTextFile("prueba.txt")

#print(labels_and_preds.take(10), "************ aca ***************")

t0 = time()
test_accuracy = labels_and_preds.filter(lambda v: v[0] == v[1]).count() / float(test_data.count())

#test_accuracy = labels_and_preds.filter(lambda v: 1.0 == v).count() / float(test_data.count())
tt = time() - t0
print("Prediction made in {} seconds. Test accuracy is {}".format(round(tt,3), round(test_accuracy,4)))     
