from SpecificMatcher import SpecificMatcher

class EqualsIgnoreCaseMatcher(SpecificMatcher):
    '''
    Verifies if the two strings are the same (ignoring case).
    '''
    
    def scoreStrings(self, par=None):
        
        try:
            return 1 if self.unsplitString1.lower()==self.unsplitString2.lower() else 0
        except Exception: # any exception, such as a null string, leads to a failed comparison
            return 0
        
        