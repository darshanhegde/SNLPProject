'''
Created on Nov 22, 2013

@author: darshanhegde
'''
from gensim.models.word2vec import Word2Vec

class EvalLM:
    
    def __init__(self, testQFilePath, testAFilePath):
        self.testQ = self.loadTest(testQFilePath)
        self.testA = self.loadTest(testAFilePath)
        
    def loadTest(self, testFilePath):
        '''
        returns a list of tuples -- (word1, word2, word3) which are questions of form this-that+this=? when testQFile is passed
        returns a list of tuples -- (pos, word_answer) which are POS and answer_words for testQ's in the same order when testAFile is passed
        '''
        testList = []
        with open(testFilePath, "rU") as testFile:
            for testLine in testFile:
                testTuple = tuple(testLine.strip().split(" "))
                testList.append(testTuple)
                
        testFile.close()
        return testList
    
    def testLM(self, LMFilePath, topK=5, verbose=True):
        LM = Word2Vec.load(LMFilePath)
        corNNCounts, corJJCounts, corVBCounts, corCounts, unkCount = 0.0,0.0,0.0,0.0,0.0
        NNCounts, JJCounts, VBCounts, Counts = 0.0,0.0,0.0,0.0
        if verbose:
            print "Starting the test on syntactic set"
        for testQ, testA in zip(self.testQ, self.testA):
                
            try:    
                topKResults = LM.most_similar(positive=[testQ[0], testQ[2]], negative=[testQ[1]], topn=topK)
            except:
                unkCount += 1
                continue
            
            Counts += 1
            if testA[0].startswith("NN"):
                NNCounts += 1
            if testA[0].startswith("JJ"):
                JJCounts += 1
            if testA[0].startswith("VB"):
                VBCounts += 1
                
            corAns = False
            for result in topKResults:
                if testA[1] == result[0]:
                    corCounts += 1
                    corAns = True
                    
            if testA[0].startswith("NN") and corAns:
                corNNCounts += 1
            if testA[0].startswith("JJ") and corAns:
                corJJCounts += 1
            if testA[0].startswith("VB") and corAns:
                corVBCounts += 1
            
        if verbose:
            print "Percent of correct noun forms: ", corNNCounts/NNCounts
            print "Percent of correct adj forms: ", corJJCounts/JJCounts
            print "Percent of correct verb forms: ", corVBCounts/VBCounts
            print "Percent of correct: ", corCounts/Counts
            
        return corCounts/Counts
                
def main():
    ELM = EvalLM("../eval/word_relationship.questions", "../eval/word_relationship.answers")
    ELM.testLM("../models/defEngPunct.model")

if __name__ == '__main__':
    main()