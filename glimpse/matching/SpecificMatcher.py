class SpecificMatcher(object):
    '''
    A specific Matcher
    '''

    def sameLength(self):
        return len(self.string1)==len(self.string2)
    
    def setString1(self, string1):
        '''
        Sets the string to compare
        '''
        if string1 is not None:
            self.unsplitString1 = string1
            self.string1 = string1.split(" ")
        else:
            self.string1 = None
            self.unsplitString1 = None
    
    def setString2(self, string2):
        '''
        Sets the reference string
        '''
        if string2 is not None:
            self.unsplitString2 = string2
            self.string2 = string2.split(" ")
        else:
            self.string2 = None
            self.unsplitString2
    
    def scoreStrings(self, par=None):
        return NotImplemented