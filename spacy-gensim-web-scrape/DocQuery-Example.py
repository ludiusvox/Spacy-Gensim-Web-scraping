# DocQuery-example.py
# Collin Lynch and Travis Martin
# 9/8/2021

# The DocQuery code is taked with taking a query and a set of
# saved documents and then returning the document that is closest
# to the query using either TF/IDF scoring or the sum vector.
# When called this code will load the docs into memory and deal
# with the distance one at a time.  

# Imports
# ---------------------------------------------
import spacy
import os
import scipy.spatial
import nltk
from gensim.models import TfidfModel
from gensim.corpora import Dictionary


# Core Code.
# ---------------------------------------------

"""
input: document directory
1. load the pacy vocab
2. look in the document directory and load all files in it
3. do not load the url file
4. put all the loaded files into a list
output: all the doc names that need to be loaded 
"""
def load_docs(DocDir):
    BaseVocab = spacy.vocab.Vocab()
    Loaded_Docs = {}
    for file in os.listdir(Directory):
        if file != 'infile.txt':
            LoadedDoc = spacy.tokens.Doc(BaseVocab).from_disk(Directory + file)
            Loaded_Docs[file] = LoadedDoc
            
    return Loaded_Docs



"""
input: spacy model, docs as a dict, query string, compfunction
1. set the closest document as the first in the list
2. decide to do a vector or tfidf comparison
3. if doing a vec comparison
    a. sum the vectors for the words in the query
    b. set closest distance to be 1 - farthest two sets can be apart
    c. take in a single document and find the sum of all the word vectors in the doc
    d. check to see if computed distance is smaller than current distance
    e. set closest document and name
4. if doing a tfidf comparison
    a. create a tfidf model for documents in the corpus
    b. set closest distance to -1 = nonsensical value
    c. take the query and sum up the words that appear in each document to geta score
    d. check to see if new score higher than the rest - highest score is better
    e. set closest doc and name
5. return the closest document and name
output: closest document and closest name
"""
def get_closest(SpacyModel, Docs, Query, CompFunc):      
    # Store the first doc in the list as the closest.
    ClosestName = list(Docs.keys())[0]
    ClosestDoc = Docs[ClosestName]

    # Now we iterate over the remainder simply checking
    # their distance and updating if they are closer.
    if CompFunc == "VEC":
        query_vec = 0
        for word in Query:
            query_vec += word.vector
            
        ClosestDist = 1
        for key in Docs.keys():    
            tempdist = get_vec_dist(SpacyModel, Docs[key], query_vec)
            if tempdist < ClosestDist:
                ClosestDist = tempdist
                ClosestName = key
                ClosestDoc = Docs[key]            
                
    elif CompFunc == "TFIDF":
            TFIDFModel, Dct, Corpus = compute_tfidf_value(Docs)
            
            ClosestDist = -1
            for n in range(len(Corpus)):
                tempdist = get_tfidf_dist(Query.text, TFIDFModel[Corpus[n]], Dct)
                if tempdist > ClosestDist:
                    ClosestDist = tempdist
                    ClosestName = list(Docs.keys())[n]
                    ClosestDoc = Docs[ClosestName]
    
    # Now return the best as a pair.
    return ClosestName, ClosestDoc
   
  
   
"""
input: all the documents in the corpus
1. create an empty list
2. go through all the documents in the set
3. tokenize the document and add it to the list
4. create a dictionary with a unique key for each word in the corpus
5. cycle through all the text and count the frequency of each word
6. create a tfidf model based on the text above
output: the model, dictionary, and corpus of text
"""
def compute_tfidf_value(Docs):
    
    all_doc_words = []
    for key in Docs.keys():
        word_tokens = nltk.word_tokenize(Docs[key].text)
        all_doc_words.append(word_tokens)
        
    Dct = Dictionary(all_doc_words)
    Corpus = [Dct.doc2bow(line) for line in all_doc_words]
    Model = TfidfModel(Corpus)
    
    return Model, Dct, Corpus
    
    
    


"""
input: query as a string, tfidf models individual corpus, dictionary
1. set total score to 0 = lowest value possible
2. go through the entire vaector passed in and look to see if the words in the query string are present
3. if they are present add the score values
4. return the total score
output: total score
"""
def get_tfidf_dist(Query, Vector, Dct):
    total_score = 0
    for id, score in Vector:
        if Dct[id] in Query:    
            #print(Dct[id], " = ", score)
            total_score += score
    return total_score



"""
input: spacy model, doc, query asa vector
1. set total vec to 0 = nonsensical value
2. iterate through the document and find the vector for each word in the doc
3. sum all the vectors together
4. compute cosine distance for the query and doc
output: the cosine distance computed
"""
def get_vec_dist(SpacyModel, Doc, Query):
    total_vec = 0
    for word in Doc:
        total_vec += word.vector
    
    tempdist = scipy.spatial.distance.cosine(Query, total_vec)
    
    return tempdist




if __name__ == "__main__":


    #initial declarations
    URL_File = 'infile.txt'
    
    #Type = "VEC"
    Type = "TFIDF"
    Directory = '/home/aaronl/PycharmProjects/pythonProject/start/'
    Query_String = 'The happiest place on Earth'

    
    #open the url file and store the webpage names for later
    webpage_names = []
    with open(URL_File, 'r') as InFile:
        website = InFile.readline()[:-1]
        while website:
            webpage_names.append(website)
            website = InFile.readline()[:-1]
        InFile.close()
    
    
    #load the spacy model
    Model = spacy.load("en_core_web_sm")
    
    
    #load the documents created in the doc downloader program
    Loaded_Docs = load_docs(Directory)
    
    #create a spacy model for the query string
    Query_Model = Model(Query_String)
    
    #find the lcosest document and name for the query
    ClosestName, ClosestDoc = get_closest(Model, Loaded_Docs, Query_Model, Type)
    
    #print the results
    print("The closest website to the query string is: " +  str(ClosestName))

        
   
