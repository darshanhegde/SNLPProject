'''
Created on Dec 3, 2013

@author: darshanhegde
'''
import numpy as np
from gensim.models.word2vec import Word2Vec
import chardet
import itertools as iter
import commands
import re

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
    Reads in dist representation as dict as:
    word --> [<list of 200 doubles>]
    '''
    distRep = {}
    with open(inFilePath) as inFile:
        header = inFile.readline()
        for inLine in inFile:
            inList = inLine.strip().split(" ")
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

def getCCA(modelFileOnePath, ModelFileTwoPath):
    trainDistRep = getDistRepFromFile(modelFileOnePath)
    testDistRep = getDistRepFromFile(ModelFileTwoPath)
    writeTrainTestMat(trainDistRep, testDistRep, "CCAFileOne.tsv", "CCAFileTwo.tsv")
    commands.getstatusoutput("R CMD BATCH CCAScore.r")
    RScriptOut = open("CCAScore.r.Rout", "rU").read().replace("\n", " ")
    CCAScore = re.findall(".*?Avg CCA Score: (.*?) ||.*?", RScriptOut)[0]
    print CCAScore
    return float(CCAScore)
    

def main():  
    print getCCA("../models/1850_2.txt", "../models/1850_3.txt")
    print getCCA("../models/1850_3.txt", "../models/1870_1.txt")
    print getCCA("../models/1870_2.txt", "../models/1870_3.txt")
    print getCCA("../models/1850_3.txt", "../models/1870_3.txt")
#         trainDistRep = getDistRepFromFile("../models/defEngRand1.model")
#         testDistRep = getDistRepFromFile("../models/defEngRand1.model")
#         writeTrainTestMat(trainDistRep, testDistRep, "../../data/CCA/randPair1.tsv" , "../../data/CCA/randPair2.tsv")
#     trainDistRep = getDistRepFromFile("../models/1850_1_shuffle.model")
#     testDistRep = getDistRepFromFile("../models/1850_2_shuffle.model")
#     writeTrainTestMat(trainDistRep, testDistRep, "../../data/CCA/dep_pair_shuff_1850_1_2_1.tsv" , "../../data/CCA/dep_pair_shuff_1850_1_2_2.tsv")
#     years = ['1850', '1870', '1890', '1910', '1930', '1950','1970', '1990', '2009']
#     for yearIdx in range(len(years)-1):
#         print "creating mat for pair: %s and %s"%(years[yearIdx], years[yearIdx+1])
#         trainDistRep = getDistRepFromFile("../models/%s_w2v.model"%years[yearIdx])
#         testDistRep = getDistRepFromFile("../models/%s_w2v.model"%years[yearIdx+1])
#         writeTrainTestMat(trainDistRep, testDistRep, "../../data/CCA/dep_pair_%s_%s_%s.tsv"%(years[yearIdx], years[yearIdx+1], years[yearIdx]) , "../../data/CCA/dep_pair_%s_%s_%s.tsv"%(years[yearIdx], years[yearIdx+1], years[yearIdx+1]))

if __name__ == '__main__':
    main()