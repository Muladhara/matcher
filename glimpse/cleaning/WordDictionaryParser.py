import re

class WordDictionaryParser(object):
    '''
    Extracts the key words that are contained in a list from a field and returns
    the corresponding value (that can be different from the word), which is separated by a comma.
    '''

    def __init__(self, cm, dictionary_file_name):
        self.cm = cm
        data_dir = cm.getProperty("general","data_dir") # the root for the list files
        file_path = data_dir+"/"+dictionary_file_name # the list file path is built
        list_file = open(file_path,'r')
        wordList = list_file.readlines() # the file is read into a dictionary
        # {key:value}
        wordDict = {w.replace("\n","").split(",")[0] : w.replace("\n","").split(",")[1] for w in wordList}
        # it builds regexp and replacements from the dictionary
        # {pattern: replacement}
        self.patternList = [(re.compile(r"\b("+w+r")\b", flags=re.I),wordDict[w]) for w in wordDict]
    
    def cleanValue(self, v):
        v2=None
        if v is not None:
            # tries to apply every replacement to v
            # returning a list of [(match, new word)]
            replaced_string_list = map(lambda p : (re.search(p[0], v),p[1]), self.patternList)
            # keeps the only elements where a match took place
            replaced_string_list = filter(lambda x: x[0] is not None, replaced_string_list)
            # if exactly a match has been found, returns the corresponding value
            if len(replaced_string_list)==1:
                v2 = replaced_string_list[0][1]  
        return v2