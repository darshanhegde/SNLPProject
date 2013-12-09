'''
Created on Dec 3, 2013

@author: darshanhegde
'''
import numpy as np
from gensim.models.word2vec import Word2Vec
import chardet
import itertools as iter

def filterLists(engList, freList):
    freModel = Word2Vec.load("../models/defFrePunct.model")
    engRetList = []
    freRetList = []
    for engWord, freWord in zip(engList, freList):
        try:
            freModel[freWord.lower()]
            engRetList.append(engWord)
            freRetList.append(freWord)
        except:
            continue
            
    return engRetList, freRetList

def getDistRep(words,modelPath,dims):
    '''
    Takes a list of words and returns distributed representation of words
    according to the model provided 
    '''
    # Load model 1
    model = Word2Vec.load(modelPath)
    numWords = len(words)
    retMat = np.zeros((numWords,dims))
    
    for idx, word in enumerate(words):
#         print word, chardet.detect(word)
        retMat[idx] = model[word]
        
    return retMat

def getDistRepFromFile(inFilePath):
    '''
    Reads in dist representation as dist as:
    word --> [<list of 200 doubles>]
    '''
    distRep = {}
    with open(inFilePath) as inFile:
        header = inFile.readline()
        for inLine in inFile:
            inList = inLine.split(" ")
            word = inList[0]
            distRepRow = inList[1:]
            distRep[word] = distRepRow
            
    inFile.close()
    return distRep

def writeTrainTestMat(distRepTrain, distRepTest, trainMatPath, testMatPath):
    trainKeys = set(distRepTrain.keys())
    testKeys = set(distRepTest.keys())
    
    interKeys = trainKeys.intersection(testKeys)
    print "Size of intersection vocab: ", len(interKeys)
    trainMat = open(trainMatPath, "w")
    testMat = open(testMatPath, "w")
    for key in interKeys:
        trainMat.write("\t".join(distRepTrain.get(key)) + "\n")
        testMat.write("\t".join(distRepTest.get(key))+ "\n")
        
    trainMat.close()
    testMat.close()
    
def writeMat(mat, outFilePath):   
    outFile =  open(outFilePath, "wb")
    for matRow in mat:
        matRowStr = [str(matEle) for matEle in list(matRow)]
        outFile.write("\t".join(matRowStr))
        
    outFile.close()
    
def readWords(inFilePath):
    words = []
    inFile = open(inFilePath, "rb")
    for inLine in inFile:
        words.append(inLine.strip().lower())
        
    inFile.close()
    return words

def main():
    for year in ['1850', '1870', '1890', '1910', '1930', '1950', '1970', '1990', '2009']:
        print "creating mat for pair: %s"%year
        trainDistRep = getDistRepFromFile("../models/train_models/%s_train.model"%year)
        testDistRep = getDistRepFromFile("../models/test_models/%s_test.model"%year)
        writeTrainTestMat(trainDistRep, testDistRep, "../../data/CCA/pair_%s_train.tsv"%(year) , "../../data/CCA/pair_%s_test.tsv"%(year))

if __name__ == '__main__':
    main()