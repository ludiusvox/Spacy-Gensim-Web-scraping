# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 09:26:10 2021

@author: Travis Martin
"""

#imports
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary


# I put in several print statements so that 
# you can see the behavior of the following items

#print(api.info()) # this will print info about the different corpi you can load
#print(api.info('text8')) #this wil print info about the text 8 
Data = api.load("text8") # this line loads the corpi of text
#print(Data)


# this will create a dictionary based on the loaded data
# it will contain the words in the Data as the value and 
# word ID as the key for the dictionary
Dct = Dictionary(Data)
#print(Dct)
#print(Dct[100])


# this will convert the Data into a bag of words
# where the corpus will contain the id for the word
# and the number of times the word appears in the document
Corpus = [Dct.doc2bow(line) for line in Data]
#print(Corpus)  #id and count


# this will take the created corpus and create a TFIDF model
Model = TfidfModel(Corpus)
#print(Model)


# once you have your corpus, you can also extract a 
# vector for the given corpus, the vector contains
# each words ID followed by its TFIDF score
vector = Model[Corpus[0]]
#print(vector)


# finally, you can print the words in the above corpus
# followed by the tfidf score for that word
# higher score means more unique/interesting for that document
for id, score in vector:
    print(Dct[id], " = ", score)
