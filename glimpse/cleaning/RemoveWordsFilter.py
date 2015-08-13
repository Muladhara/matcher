import re

class RemoveWordsFilter():
    '''
    Cleaning criterion that transforms some words in a field
    according to transform_words configuration parameter.
    '''
    def __init__(self, cm):
        self.cm = cm
        # builds the mapping list for the single words
        filterMappings = eval(cm.getProperty("general","transform_words"))
        
        # loads every replacement mapping
        self.patternMappings = list()
        # cleans trailing comma
        self.patternMappings.append((re.compile(r",$"),''))
        for da,a in filterMappings:
            self.patternMappings.append((re.compile(r"\b"+da+r"\b",flags=re.I),a))
        
        # cleans repeated spaces
        self.patternMappings.append((re.compile(r"\s\s"),' '))
        # cleans leading and trailing spaces  
        self.patternMappings.append((re.compile(r"^\s"),''))
        self.patternMappings.append((re.compile(r"\s$"),''))
        self.patternMappings.append((re.compile(r",$"),''))
                
    # pulisce il singolo valore
    def cleanValue(self, v):
        v2=v
        if v2 is not None:
            for ptrn, repl in self.patternMappings:
                v2=re.sub(ptrn, repl, v2)
        return v2