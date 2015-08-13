import ConfigParser as config
import logging.handlers

class ConfigurationManager():
    '''
    To handle configuration file
    '''
    
    def __init__(self):
        self.config = config.RawConfigParser()
        self.config.read("/Users/Eleonora/Documents/glimpse/config/matcher.cfg")
        self.log = None
    
    def getProperty(self,section,option):
        return self.config.get(section,option)
    
    def getLogger(self):
        
        if self.log is None:            
            logFile = self.getProperty("log", "file")
        
            # create logger
            logger = logging.getLogger('emLogger')
            logger.setLevel(logging.DEBUG)
            
            # create console handler and set level to debug
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            
            chf = logging.handlers.RotatingFileHandler(logFile, mode='a', maxBytes=100000, backupCount=5, encoding=None, delay=0)
            chf.setLevel(logging.DEBUG)
            
            # create formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            
            # add formatter to ch
            ch.setFormatter(formatter)
            chf.setFormatter(formatter)
            
            # add ch to logger
            logger.addHandler(ch)
            logger.addHandler(chf)
            
            self.log = logger
            
        return self.log

        
        
        