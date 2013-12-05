'''
Created on Nov 16, 2013

@author: darshanhegde

@note: it converts the input english / french sentences into normalized list of words and provides iterator method for reading 
in the data as corpus (list of sentences and sentence is a list of words). The normalization process, lower cases all the words
and removes punctuation marks based on the flag passed.  The files are already cleaned and there is almost nothing to do other than
providing few filtering methods like lower casing and punctuation.

FOR NOW ONLY USE IT WITH TRAIN FOLDER -- TEST and VALIDATION SENTENCES CONTAIN SENTENCE INDEX. THE CODE DOESNOT HANDLE IT
'''
from collections import defaultdict
from string import punctuation
import os
import random

PUNCT_LIST = list(punctuation)


class LoadBilingualCorpus:
    
    def __init__(self, inFolderPath, lang="eng", lowerCase=True, punctRemove=True):
        '''
        @param inFolderPath: The path of the directory from which to load the corpus.
        @param lang: eng or fre 
        @param punctRemove: boolean indicating whether to remove punctuation marks. 
        '''
        self.inFolderPath = inFolderPath
        if lang == "eng":
            self.fileExtention = ".e"
        elif lang == "fre":
            self.fileExtention = ".f"
        else:
            raise Exception("please pass a valid language -- eng / fre")
        self.punctRemove = punctRemove
        self.lowerCase = lowerCase
        
    def __iter__(self):
        allFileNames = os.listdir(self.inFolderPath)
        filterFileNames = filter(lambda x: x.endswith(self.fileExtention), allFileNames)
        fullFilePaths = []
        for fileName in filterFileNames:
            fullFilePaths.append(os.path.join(self.inFolderPath, fileName))
            
        for filePath in fullFilePaths:
            with open(filePath, "r") as inFile:
                for inSent in inFile:
                    if self.lowerCase:
                        inSent = inSent.lower()
                    inList = inSent.strip().split(" ") 
                    if self.punctRemove:
                        inList = filter(self.filter_punct, inList)
                        
                    yield inList
                    
            inFile.close()
            
    def filter_punct(self, word):
        return not(word in PUNCT_LIST)
    
def main():
    LBC = LoadBilingualCorpus("../../data/training/")
    counter = 0
    print "first 5000 english sentences"
    engVocab = defaultdict(int)
    for sentence in LBC:
        if counter > 500000:
            break
        for word in sentence:
            engVocab[word] += 1
        counter += 1
        
    freqEngWords = filter(lambda x:x[1]>15,engVocab.items())
    print "Number of words: ", len(freqEngWords)
    sampEngWords = random.sample(freqEngWords, 10000)
    outFile = open("../../data/CCA/engWords.txt", "wb")
    for freqEngWord, count in sampEngWords:
        outFile.write(freqEngWord + "\n")
        
    outFile.close()
        
#     LBC = LoadBilingualCorpus("../../data/training/", lang="fre")    
#     counter = 0
#     print "first 5000 french sentences"
#     for sentence in LBC:
#         if counter > 5000:
#             break
#         print sentence
#         counter += 1

if __name__ == '__main__':
    main()