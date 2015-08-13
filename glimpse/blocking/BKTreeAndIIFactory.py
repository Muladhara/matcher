from InvertedIndex import InvertedIndex
from BKTree import BKTree

class BKTreeAndIIFactory():
    '''
    A factory for BKTree and InverseIndex
    '''

    def getIIndexAndBkTree(self, db2Dao, blocking_column, search_discard_words, dist_function):
        '''
        Returns an instance of (BKTree, InverseIndex)
        Arguments:
        db2Dao: the input MatchDao 
        blocking_column: the blocking column to index
        search_discard_words: a list of words that must not be used in blocking
        dist_function: the distance function (it must be a metric function)
        '''
        
        db2 = db2Dao.getCleanDb()  
        
        # for each string, it splits it and saves the words in a set
        wordSet = set()
        ii = InvertedIndex()
        rownum = 0
        
        for adb in db2:
            # builds the inverse index and the tree
            tupleSet = set((adb[blocking_column]).split(" "))
            # for each token
            for w in tupleSet:
                # if the word is not in the stop lost, it is added to the 
                # index and to the bag of words for the tree
                if w not in search_discard_words:
                    wordSet.add(w)
                    ii.addWord(str(w),rownum)
            rownum+=1
        
        bkTreeIndex = BKTree(dist_function, wordSet)
        return (ii,bkTreeIndex)
