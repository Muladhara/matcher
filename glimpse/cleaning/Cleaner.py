from RemoveWordsFilter import RemoveWordsFilter
from CopyWordsFilter import CopyWordsFilter
from EnterpriseFormFilter import EnterpriseFormFilter
from ZipcodeParser import ZipcodeParser
from ShortForCityParser import ShortForCityParser
from WordListParser import WordListParser
from WordDictionaryParser import WordDictionaryParser
from GeneralCleaning import GeneralCleaning
from Capitalizer import Capitalizer
from WordListParserKeepAfter import WordListParserKeepAfter
from WordListParserKeepBefore import WordListParserKeepBefore

class Cleaner(object):
    '''
    Handles the cleaning of a data source combining a variety
    of enterprise legal form 
    '''
    def __init__(self, daoIn, daoOut, cleanings, cm):
        self.daoIn = daoIn # intput dao
        self.daoOut = daoOut # output dao
        self.cleaners = dict() # {targetColumnIndex : (inputColumnIndex, [cleaners, ...])}
        
        # builds the cleanings. If they have more complex
        # constructors, then the parameters are appropriately passed
        for cl in cleanings:
            inputColumnIndex = cl[0]
            targetColumnIndex = cl[1]
            
            if cl[2]=='transform_words':
                    self.setCleaningMethod(RemoveWordsFilter(cm), inputColumnIndex, targetColumnIndex)
            elif cl[2]=='clean_enterprise':
                self.setCleaningMethod(EnterpriseFormFilter(), inputColumnIndex, targetColumnIndex)
            elif cl[2]=='zipcode_parser':
                self.setCleaningMethod(ZipcodeParser(cm), inputColumnIndex, targetColumnIndex)
            elif cl[2]=='short_city_parser':
                self.setCleaningMethod(ShortForCityParser(cm), inputColumnIndex, targetColumnIndex)
            elif cl[2]=='wordlist_parser':
                self.setCleaningMethod(WordListParser(cm,cl[3]), inputColumnIndex, targetColumnIndex)
            elif cl[2]=='wordlist_parser_keepafter':
                self.setCleaningMethod(WordListParserKeepAfter(cm,cl[3]), inputColumnIndex, targetColumnIndex)
            elif cl[2]=='wordlist_parser_keepbefore':
                self.setCleaningMethod(WordListParserKeepBefore(cm,cl[3]), inputColumnIndex, targetColumnIndex)
            elif cl[2]=='worddictionary_parser':
                self.setCleaningMethod(WordDictionaryParser(cm,cl[3]), inputColumnIndex, targetColumnIndex)
            elif cl[2]=='capitalizer':
                self.setCleaningMethod(Capitalizer(cm), inputColumnIndex, targetColumnIndex)
            elif cl[2]=='general_cleaning':
                self.setCleaningMethod(GeneralCleaning(), inputColumnIndex, targetColumnIndex)
            
            else: # otherwise copies the field
                self.setCleaningMethod(CopyWordsFilter(), cl[0], cl[1])
    
    def setCleaningMethod(self, cleaner, inputColumnIndex, targetColumnIndex):
        '''
        Sets a cleaner for the pair inputColumnIndex, targetColumnIntex.
        Arguments:
        cleaner: the cleaner to be set
        inputColumnIndex: the index of the column to clean from
        targetColumnIndex: the index of the target, clean column
        '''
        
        # each cleaner calculates a destination column
        # from an input column, applying in the order
        # a number of cleaners
        
        # if a cleaner does not exist for the target column
        if targetColumnIndex not in self.cleaners:
            self.cleaners[targetColumnIndex] = (inputColumnIndex, [cleaner])
        # if a clener already exists and another one has to be added
        else:
            self.cleaners[targetColumnIndex][1].append(cleaner)
    
    
    def getCleanDB(self):
        '''
        Cleans each column of the given input dao with its cleaner. Adds the results
        to the output dao.
        '''
        cdb = self.daoIn.getCleanDb()
        nCol = self.daoOut.getColumnsNo()
        
        # for each row of the input dao
        # for each column of the output dao
        # gets the input column
        # gets the cleaners
        # extracts the current value
        # each cleaner is applied, updating the current value
        # the clean row is added to the output dao
          
        for cdb_row in cdb:
            out_row = []
            for i in range(0,nCol):
                input_col = self.cleaners[i][0]                
                cleaner_objects = self.cleaners[i][1]                
                v = cdb_row[input_col]                
                for co in cleaner_objects:
                    v = co.cleanValue(v)
                out_row.append(v)
            self.daoOut.addRow(out_row)
        
        return self.daoOut