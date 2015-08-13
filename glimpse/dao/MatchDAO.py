from glimpse.utilities.DbHandler import DbHandler

class MatchDAO():
    '''
    A DAO to handle a data source
    '''
    
    def __init__(self, dataSource):
        
        self.rows = list()
        self.dbh = DbHandler()
        self.dbh.initDb(dataSource)
        self.dbName = dataSource.db_name
        self.table = dataSource.table
        self.columns = dataSource.get_columns_as_list()
        # empty list of key columns
        self.key_columns=list()
    
    def getColumnsNo(self):
        return len(self.columns)
    
    def getColumnList(self):
        return self.columns
    
    def addKeyColumn(self, key_column):
        self.key_columns.append(key_column)

    def setClericalScore(self, score, key_values):
        ''' 
        Updates a line of the table, inserting the score assigned in the clerical review
        Arguments:
        score: the score assigned by the reviewer
        key_values: a list of values for the keys
        '''
        updateQuery = "UPDATE " + self.table + " SET CLERK_SCORE = " + str(score) + " WHERE "
        i=0
        for key, value in zip(self.key_columns, key_values):
            updateQuery = updateQuery + key + " = '" + str(value) + "'"
            i=i+1
            if i<len(self.key_columns):
                updateQuery=updateQuery + "AND"

        print(updateQuery)
        cur = self.dbh.getCursor()
        cur.execute(updateQuery)
        
    def getKeyColumn(self):
        return self.identifier
        
    def addRow(self,t):
        '''
        Adds a row to the database
        '''
        self.rows.append(t)
        
    def getCleanDb(self, orderedByKey=None):
        '''
        Returns a list of tuples with all the
        rows in the database
        '''
        if len(self.rows)==0: # result caching
            colSel=''
            for c in range(0,len(self.columns)):
                colSel+='`' + self.columns[c] + '`'
                if c<len(self.columns)-1:
                    colSel+=','
                
            getQuery = "SELECT " + colSel + " FROM " + self.table
            # if the result must be ordered by key
            if orderedByKey is not None:
                getQuery = getQuery + " ORDER BY " + orderedByKey
            cur = self.dbh.getCursor()
            cur.execute(getQuery)
            fullDb = cur.fetchall() 
            self.rows = fullDb
        return self.rows
    
    def delete(self):
        '''
        Deletes the table associated with this dao
        '''
        
        deleteQuery = "DELETE FROM " + self.dbName + "." + self.table
        cur = self.dbh.getCursor()
        cur.execute(deleteQuery)        
        self.dbh.handleTransaction(True)
        
    
    def save(self):
        '''
        Saves the current rows 
        into the table associated with this dao
        '''
        
        cur = self.dbh.getCursor()
        
        formalPart = "(" 
        for col in self.columns:
            formalPart += '`' + col + '`,'
        formalPart = formalPart[:-1] + ')'
        
        # total number of columns
        totalFieldsNo = len(self.columns) #+ self.matchNo + 1
        valuePart = "(" + "%s,"*(totalFieldsNo-1)+"%s)"
        
        insertQuery = "INSERT INTO " + self.dbName + "." + self.table + " " + formalPart + "VALUES " + valuePart
        cur.executemany(insertQuery,self.rows)
        
        self.dbh.handleTransaction(True)
                