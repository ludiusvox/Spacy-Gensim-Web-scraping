# AIA POSExtract.py
# @copyright: Collin Lynch
#
# This code provides a basic walkthrough of POS tagging methods
# that are built into NLTK.  These methods are to be used on
# arbitrary text and support extraction of keywords such as
# nouns and verbs which we can use to compose keywords for our
# matrices.

# Imports
# -----------------------------------
import nltk



# Working Code
# -----------------------------------
# First we will load a basic document from an existing nltk dataset.
# In this case we will use Jane Austen's Emma as a basic text.
#print(nltk.corpus.gutenberg.fileids())
EmmaWords = nltk.corpus.gutenberg.words(fileids="austen-emma.txt")
#print(EmmaWords)



# Having loaded that and taking advantage of the existing tokenizer
# we will go ahead and apply POS tagging to the words.  In this case
# we are just using the built-in tokenizer that works with the NLTK.
# more complex POS tagging can be done by other methods.
#
# NOTE: This process can be slow depending on the time.
EmmaTags = nltk.pos_tag(EmmaWords)



# Having done that we can then extract all of the nouns so we have a
# simplified topic model.  In this case we can iterate over the tagged
# words with a simple loop to pull the NN (singular noun), NNS (plural
# noun), NNP (proper noun singular), and NNPS (proper noun plural).
# Other types (e.g. verbs) can be pulled by looking up the type or using
# the first letter.
def getNouns(Tagged_Text):
    """
    Iterate over the tagged text pulling the nouns.
    """

    # Generate an empty set for storage.
    NounSet = set()

    # Iterate over the pairs collecting the items.
    for (Word, Tag) in Tagged_Text:

        print("Checking Word/Tag Pair: {} {}".format(Word, Tag))
        
        if (Tag[0] == "N"):
            NounSet.add(Word)

    return(NounSet)



# Extracting the nouns, and perhaps additional words like verbs, will
# proide us with a very crude topic model that we can use for lookup
# and comparison via tf-idf or some other document.  We will return to
# that in a later case.
EmmaNouns = getNouns(EmmaTags)
#print(EmmaNouns)


# In the meantime look at ways to apply this to your existing page code.
# Among other things we can feed these collected words into our document
# vector code to produce a noun-only positioning for the document.



# To do that we borrow from the prior code but now assume we are feeding
# it a list version of the words.  
NounTokens = list(EmmaNouns)


import numpy
import scipy.spatial
import gensim
import gensim.downloader


#print(gensim.downloader.info()['models'].keys())
GloveModel = gensim.downloader.load('glove-twitter-50')


# To make a document vector suitable for this task we first
# convert it to a lower case sequence and then use that to
# get the individual values.  Then we sum the total up.
def makeDocVec(DocTokens):

    DocSum = 0
    for Token in DocTokens:
        try:
            WordVectors = GloveModel[Token.lower()]
            DocSum += numpy.array(WordVectors)
        except:
            print(Token, " not in database")
            
    return(DocSum)


# Now if you do the above for two documents you can just compare
# them using the basic cosine similarity function.
Doc1Sum = makeDocVec(NounTokens)
print(Doc1Sum)
Doc2Sum = makeDocVec(NounTokens)
print(Doc2Sum)


print(scipy.spatial.distance.cosine(Doc1Sum, Doc2Sum))
    


