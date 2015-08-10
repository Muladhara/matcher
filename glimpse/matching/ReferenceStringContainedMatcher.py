from SpecificMatcher import SpecificMatcher

class ReferenceStringContainedMatcher(SpecificMatcher):
    '''
    Verifies if a string of db2 is contained in the word set
    of the string in db1
    '''
    
    def scoreStrings(self, par=None):
        string1 = set(self.string1) if self.string1 is not None else set()
        string2 = set(self.string2) if self.string2 is not None else set()
        
        # if db2 is empty, the score is 0
        if len(string2)>0 and len(string2 - string1) == 0:
            return 1
        else:
            return 0
