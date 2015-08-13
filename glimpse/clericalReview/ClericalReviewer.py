from __future__ import print_function

class ClericalReviewer():
    '''
    Allows to perform a clerical review
    '''

    def __init__(self, cDao, key_column1, key_column2):
        '''
        Builds a reviewer given the dao and the two key columns
        '''
        self.cDao = cDao
        self.key_column1 = key_column1
        self.key_column2 = key_column2
        self.cDao.addKeyColumn(key_column1)
        self.cDao.addKeyColumn(key_column2)
        
    def review(self):
        '''
        Implements the clerical review
        '''
        tuples = self.cDao.getCleanDb(orderedByKey=self.self.key_column1)
        selectionBlock = list()
        previousKey = None
        currentKey = None
        
        cols = self.cDao.getColumnList()
        
        for t in tuples:
            currentKey = t[0]
            # if there is a change of key, an option must be chosen
            if previousKey is not None and currentKey != previousKey:
                print("======================================")
                print("Option to be chosen for: " + previousKey + ":")
                for j in range(0,len(selectionBlock)):
                    print("\n" + str(j) + " > ")
                    for (field,value) in zip(cols,selectionBlock[j]):
                        print(field + ": " + value if value is not None else "None", end=" ")
                      
                # asks for an option
                ch = None
                # keeps asking, while a correct number has not been given
                while ch is None:
                    print("\nChoice: ", end="")
                    try:
                        ch = input()
                        ch = int(ch)
                    except Exception:
                        ch = None
                # saves the choice
                self.cDao.setClericalScore(1,selectionBlock[ch][0],selectionBlock[ch][0])
                # resets the selection block
                selectionBlock = list()
            else:
                selectionBlock.append(t)
                
            previousKey = currentKey