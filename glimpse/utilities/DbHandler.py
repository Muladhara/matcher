import MySQLdb as mysql

class DbHandler():
    '''
    To handle connections to MySql
    '''
    
    def __init__(self):
        self.db = None
    
    def initDb(self, dataSource):
       
        self.db = None 
        
        DATABASE_HOST = dataSource.host
        DATABASE_USER = dataSource.user
        DATABASE_NAME = dataSource.db_name
        DATABASE_PASSWD = dataSource.password
        DATABASE_PORT = dataSource.port
        
        if self.db is None:
            self.db=mysql.connect(host=DATABASE_HOST,user=DATABASE_USER,passwd=DATABASE_PASSWD, db=DATABASE_NAME, port=int(DATABASE_PORT))
    
    def stopDb(self):
        if self.db is not None:
            self.db.close()
    
    def handleTransaction(self, commit):
        if self.db is not None:
            if commit:
                self.db.commit()
            else:
                self.db.rollback()
    
    def getCursor(self):
        if self.db is None:
            self.initDb()
        return self.db.cursor()
    
        