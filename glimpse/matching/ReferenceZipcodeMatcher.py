from SpecificMatcher import SpecificMatcher
import re

class ReferenceZipcodeMatcher(SpecificMatcher):
    '''
    Verifies is a zipcode, wherever contained, in a string of
    db2 is contained in a string of db1
    '''
    def scoreStrings(self, par=None):
        zip2 = self.unsplitString2
        zip1 = self.getCapFromStrings(self.unsplitString1)
        
        return 1 if zip1 == zip2 else 0
        
    
    def getCapFromStrings(self, capField):
        '''
        Exctracts a zipcode from a field.
        Returns None if not found
        '''        
        pattern=re.compile('\d{5}')
        string1Cap = None
        if capField is not None:
            m=re.search(pattern,capField)
            if m is not None:
                string1Cap = m.group(0)

        return string1Cap