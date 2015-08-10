import re

class WordListParserKeepAfter(object):
    '''
    Extracts a substring starting from a given string in a list (excluded from the selection).
    The whole string if not found.
    '''
    def __init__(self, cm, list_file_name):
        self.cm = cm
        data_dir = cm.getProperty("general","data_dir") # the root for the list files
        file_path = data_dir+"/"+list_file_name # the list file path is built
        list_file = open(file_path,'r')
        wordList = list_file.readlines() # the file is read into a list
        self.patternList = [re.compile(r"\b"+w.replace("\n","")+r"\b(.*)", flags=re.I) for w in wordList] # builds regexps for the word list
    
    def cleanValue(self, v):
        # searches for any match
        v2=v
        if v is not None:
            matches = map(lambda x : re.search(x, v), self.patternList)
            matches = filter(lambda x: x is not None, matches)
            # returns a result only if at least one match is found
            if len(matches)>=1:
                v2=matches[0].groups()[0]
        return v2
    
        