from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
import pandas as pd
import numpy as np


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

WL = WordNetLemmatizer()

data_frame = pd.read_csv("data/trainAirlines.csv", encoding="iso8859_16")
data = data_frame.values

comments = data[:,-2]
newStuff = []
for comment in comments:
    words = comment.replace("  ", " ").replace(",","").replace(".", "").replace("(", "").replace(")", "").split(" ")
    cleanwords = []
    for word in words:
        if word != "":
            cleanwords += [word]

    taggedwords = nltk.pos_tag(cleanwords)
    newWords = []
    for word, tag in taggedwords:
        tagtype = get_wordnet_pos(tag)
        if (tagtype != ''):
            newWord = WL.lemmatize(word,tagtype)
            newWords += [newWord]
    newStuff += [" ".join(newWords)]
data[:,-2] = newStuff
names = ['id,airline,date,location,rating,cabin,value,recommended,review,feeling']
print (names[0])

for x in data:
    print (','.join(map(str, x[1:])))

#print (comments)
