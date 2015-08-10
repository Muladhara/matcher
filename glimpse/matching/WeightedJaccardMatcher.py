from SpecificMatcher import SpecificMatcher

class WeightedJaccardMatcher(SpecificMatcher):
    '''
    Returns a score that is the Jaccard Index between two strings
    weighted with respect of the frequency of the words.
    '''
    
    def __init__(self, ii):
        self.ii=ii

    def scoreStrings(self, par=None):
        ii = self.ii
        
        s1=set(self.string1)
        s2=set(self.string2)
        
        wj = sum([(1-ii.getWordFrequency(w)) for w in (s1 & s2)]) / sum([(1-ii.getWordFrequency(w)) for w in (s1 | s2)])
        return wj
    
        