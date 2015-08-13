from SpecificMatcher import SpecificMatcher

class JaccardMatcher(SpecificMatcher):
    '''
    Returns a similarity index corresponding to the Jaccard index between two bags
    of strings.
    '''

    def scoreStrings(self, par=None):
        s1=set(self.string1)
        s2=set(self.string2)
        return float(len (s1 & s2)) / float(len (s1 | s2))