class InvertedIndex:
    '''
    An inverse index mapping words to records
    '''
    
    def __init__(self):
        self.index = dict()
        self.total_occurrences = 0 # total number of occurrences
    
    def addWord(self, w, s):
        '''
        Adds a word to the inverted index
        Arguments:
        w: the word to be added
        s: the record number w refers to
        '''
        if w in self.index:
            self.index[w].add(s)
        else:
            self.index[w] = set()
            self.index[w].add(s)
        # counts the occurrence
        self.total_occurrences += 1
    
    def getObjsByWord(self, w):
        '''
        Returns the set of records corresponding to
        a given word
        Arguments:
        w: the word to search for
        '''
        if w in self.index:
            return self.index[w]
        else:
            return None
    
    def getWordFrequency(self, w):
        '''
        Retrieves the frequency of a word as
        the number of records it occurs in divided by
        the total number of occurrences of every word
        Arguments:
        w: the word to search for
        '''
        if w not in self.index:
            return 0
        return float(len(self.index[w])) / float(self.total_occurrences)
    
    def getTopWords(self, n):
        '''
        Retrieves the top most frequent words
        '''
        lengths = [ [len(self.index[x]),x] for x in self.index ]
        lengths = sorted(lengths,reverse=True)
        return lengths[:n]