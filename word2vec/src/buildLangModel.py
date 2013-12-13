'''
Created on Nov 16, 2013

@author: darshanhegde

@note: creates the language model using word2vec.

If you just want to play around with the model use following commands:
>>from gensim.models import word2vec
>>engModel = word2vec.Word2Vec.load(<path of english model file>)

Call any method you need from http://radimrehurek.com/gensim/models/word2vec.html
'''

from gensim.models import word2vec
from loadBilingualCorpus import LoadBilingualCorpus
from time import time

def main():
    tic = time()
    englishCorpus = LoadBilingualCorpus("../../data/training/", lang="eng", punctRemove=False)
    print "training the english language model"
    modelEng = word2vec.Word2Vec(englishCorpus, size=200, window=10, workers=5)
    modelEng.save_word2vec_format("../models/defEngRand2.model", binary=False)
    toc = time()
    print "english model written. Time taken: ", (toc-tic)/60, "minutes"
#     tic = time()
#     print "training french model"
#     frenchCorpus = LoadBilingualCorpus("../../data/training/", lang="fre", punctRemove=False)
#     modelFre = word2vec.Word2Vec(frenchCorpus, size=200, window=10, workers=5)
#     modelFre.save("../models/defFrePunct.model")
#     toc = time()
#     print "french model written. Time taken: ", (toc-tic)/60, "minutes"
    
    # Now find canonical correlation between english and french 
    
        

if __name__ == '__main__':
    main()