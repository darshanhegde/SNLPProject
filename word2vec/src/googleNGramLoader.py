'''
Created on Nov 26, 2013

@author: darshanhegde

@note: The class takes the N Gram Folder Path and start year(4-digit int) and stop year (4-digit int) 
and gives a iterator over the N-grams and counts for the year range (end points inclusive)
Some NGrams contained POS appended to them. Added a flag to choose between stripping and not stripping them off.
Make sure you have unzipped Google N Gram files in the folder or use 
>>gunzip *.gz
to unzip all the files in a single shot
'''

import os

class GoogleNGramLoader:
    
    def __init__(self, nGramFolderPath, startYear, stopYear, stripPOSTags=True):
        self.startYear = startYear
        self.stopYear = stopYear
        self.stripPOSTags = stripPOSTags
        NGFileNames = os.listdir(nGramFolderPath)
        self.NGFilePaths = []
        for NGFileName in NGFileNames:
            self.NGFilePaths.append(os.path.join(nGramFolderPath, NGFileName))
            
    def __iter__(self):
        for NGFilePath in self.NGFilePaths:
            with open(NGFilePath, "rU") as NGFile:
                for NGramLine in NGFile:
                    NGramList = NGramLine.strip().split("\t")
                    NGram = NGramList[0]
                    NGramYear = int(NGramList[1])
                    NGramCount = int(NGramList[2])
                    
                    if self.stripPOSTags:
                        NGrams = NGram.split(" ")
                        NGramOut = []
                        for NG in NGrams:
                            if NG != "_END_":
                                NGramOut.append(NG.split("_")[0])
                        NGram = " ".join(NGramOut)
                    
                    if NGramYear>=self.startYear and NGramYear<=self.stopYear:
                        yield (NGram, NGramCount)
                        
            NGFile.close()
                    

def main():
    '''
    This shows simple test case for using the loader
    '''
    GN = GoogleNGramLoader("../../data/GNGram/", 1990, 1995, True)
    for NG in GN:
        print NG

if __name__ == '__main__':
    main()