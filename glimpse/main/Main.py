import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glimpse_gui.settings")
import sys
from glimpse.utilities.ConfigurationManager import ConfigurationManager
from glimpse.stringUtils.StringMatcher import distance as lev
from glimpse.blocking.BKTreeAndIIFactory import BKTreeAndIIFactory
from glimpse.matching.Matcher import Matcher
from glimpse.dao.MatchDAO import MatchDAO
from glimpse.cleaning.Cleaner import Cleaner
import configurator.models

cm = ConfigurationManager()
logger = cm.getLogger()

class MissingException(Exception):
    def __init__(self, message):
        super(MissingException)

# carica la configurazione 
# di un determinato match
def loadConfigurationForMatching(matchingName):
    conf = dict()
    conf["search_discard_words"] = set(eval(cm.getProperty(matchingName,"search_discard_words")))    
    # estrae la colonna del db2 su cui fare blocking
    conf["blocking_column_2"] = int(cm.getProperty(matchingName,"blocking_column_2"))
    conf["blocking_column_1"] = int(cm.getProperty(matchingName,"blocking_column_1"))
    # estrae il criterio su cui fare blocking
    conf["blocking_criterion"] = cm.getProperty(matchingName,"blocking_criterion")
    conf["blocking_threshold"] = int(cm.getProperty(matchingName, "blocking_threshold"))
    # estrae se deve mantenere solo i candidati con score massimo
    conf["keep_only_max_score"] = cm.getProperty(matchingName,"keep_only_max_score") == 'Y'
    # caricamento della configurazione dei match
    conf["matchNo"] = int(cm.getProperty(matchingName,"match_no"))
    
    conf["matches"] = [ eval(cm.getProperty(matchingName,"match_" + str(i))) for i in range(0,conf["matchNo"])]   
    # estrae le colonne da portare in output dei due db
    conf["columns_from_db1_indices"] = eval(cm.getProperty(matchingName,"columns_from_db1_indices"))
    conf["columns_from_db2_indices"] = eval(cm.getProperty(matchingName,"columns_from_db2_indices"))
    conf["sourceDb_1"] = cm.getProperty(matchingName, "sourceDb_1")
    conf["sourceDb_2"] = cm.getProperty(matchingName, "sourceDb_2")
    conf["output"] = cm.getProperty(matchingName, "outputDb")
    
    return conf

def loadConfigurationForMatchingDb(matchingName):
    conf = dict()
    try:
        m = configurator.models.Matching.objects.get(name=matchingName)
    except Exception:
        raise MissingException("Missing matching")
    conf["search_discard_words"] = set(eval(m.blocking.search_discard_words))
    conf["blocking_column_1"] = int(m.blocking_column_1.get_my_pos())
    conf["blocking_column_2"] = int(m.blocking_column_2.get_my_pos())
    conf["blocking_criterion"] = m.blocking.criterion
    conf["blocking_threshold"] = int(m.blocking.threshold)
    conf["keep_only_max_score"] = cm.getProperty("general","keep_only_max_score") == 'Y'
    conf["matchNo"] = m.match.count()
    conf["matches"] = m.get_list_repr()
    # from-to mappings from db1
    conf["columns_from_to_db1_indices"] = m.get_mapping_list_db1()
    # from-to mappings from db2
    conf["columns_from_to_db2_indices"] = m.get_mapping_list_db2()
    # scores and global score
    conf["score_columns"] = m.get_match_score_column_list()
    conf["global_score_column"] = m.global_score_column.get_my_pos()
    # data sources
    conf["sourceDb_1"] = m.sourceDs1
    conf["sourceDb_2"] = m.sourceDs2
    conf["output"] = m.targetDs
    
    return conf
    
# carica la configurazione 
# per un determinato cleaning
def loadConfigurationForCleaning(cleaningName):
    conf = dict()
    conf["sourceDb"] = cm.getProperty(cleaningName, "sourceDb")
    conf["outputDb"] = cm.getProperty(cleaningName,"outputDb")
    conf["cleaningNo"] = int(cm.getProperty(cleaningName,"cleaning_no"))
    conf["cleanings"] = [eval(cm.getProperty(cleaningName,"cleaning_" + str(i))) for i in range(0,conf["cleaningNo"])]   

    return conf

def loadConfigurationForCleaningDb(cleaningName):
    conf = dict()
    try:
        cleaning = configurator.models.Cleaning.objects.get(name=cleaningName)
    except Exception:
        raise MissingException("Missing cleaning")
    conf["sourceDb"] = cleaning.sourceDs
    conf["outputDb"] = cleaning.targetDs
    conf["cleanings"] = cleaning.get_list_repr()
    return conf

def loadConfigurationForClericalReview(clerical_review_name):
    conf = dict()
    conf["sourceDb"] = cm.getProperty(clerical_review_name, "sourceDb")
    conf["key_column1"] = cm.getProperty(clerical_review_name, "key_column1")
    conf["key_column2"] = cm.getProperty(clerical_review_name, "key_column2")
    
    return conf

# carica la configurazione
def loadGeneralConfiguration():
    conf = dict()    
    # estrae le colonne da portare in output dei due db
    conf["sx_limit"] = int(cm.getProperty("general","sx_limit"))
    return conf

def clean(cleaningName):
    logger.info("BEGIN")
    cleaningConf = loadConfigurationForCleaningDb(cleaningName)
    sourceDb = cleaningConf["sourceDb"]
    outputDb = cleaningConf["outputDb"]
    cleanings = cleaningConf["cleanings"]
    daoIn = MatchDAO(sourceDb)
    daoOut = MatchDAO(outputDb)
    clnr = Cleaner(daoIn, daoOut, cleanings, cm)
    
    # esegue i clean
    logger.info("Cleaning started")
    daoOut = clnr.getCleanDB()
    logger.info("Cleaning ended")
    # e salva
    logger.info("BEGIN saving")
    daoOut.delete()
    daoOut.save()
    logger.info("END saving")
    

def compareAndClassify(matchingName):
    logger.info("BEGIN")
    
    # carica le configurazioni
    logger.info("Retrieving configuration")
    conf = loadGeneralConfiguration() # TODO: eliminare dalla configurazione generale variabili passate come parametri
    matchConf = loadConfigurationForMatchingDb(matchingName)
    
    sx_limit = conf["sx_limit"]
    
    db1 = matchConf["sourceDb_1"]
    db2 = matchConf["sourceDb_2"]
    dbOut = matchConf["output"]
    
    levThreshold = matchConf["blocking_threshold"]
    search_discard_words = matchConf["search_discard_words"]
    # estrae le colonne su cui fare blocking
    blocking_column_2 = matchConf["blocking_column_2"]
    blocking_column_1 = matchConf["blocking_column_1"]
    
    # estrae se deve mantenere solo i candidati con score massimo
    keep_only_max_score = matchConf["keep_only_max_score"]
    
    # estrae le colonne da portare in output
                                        
    columns_from_to_db1_indices = matchConf["columns_from_to_db1_indices"]
    # from-to mappings from db2
    columns_from_to_db2_indices = matchConf["columns_from_to_db2_indices"]
    # scores and global score
    score_columns = matchConf["score_columns"]
    global_score_column = matchConf["global_score_column"]
    
    # caricamento della configurazione dei match
    matchNo = matchConf["matchNo"]
    matches = matchConf["matches"]
    
    logger.info("Lodaded blocking threshold="+str(levThreshold))
    logger.info("Discarded words for search:" + str(search_discard_words))
    logger.info("Sx_limit="+str(sx_limit))
    logger.info(str(matchNo) + " matches loaded")
    logger.info("Matches: " + str(matches))
    
    db2Dao = MatchDAO(db2) # riferimento
    db1Dao = MatchDAO(db1) # da ricercare
    mDao = MatchDAO(dbOut) # risultato
        
    logger.info("BEGIN BKTree and InvertedIndex creation")
    bkif = BKTreeAndIIFactory()
    ii, bkTreeIndex = bkif.getIIndexAndBkTree(db2Dao,blocking_column_2,search_discard_words,lev)
    #print(ii.getTopWords(20))
    
    logger.info("END BKTree, DirectIndex and InvertedIndex creation")    
    
    logger.info("BEGIN matching")
    m = Matcher(db1Dao, db2Dao, matches, mDao, bkTreeIndex, ii, sx_limit, 
                search_discard_words, blocking_column_1, levThreshold, 
                columns_from_to_db1_indices, columns_from_to_db2_indices,
                score_columns, global_score_column,
                keep_only_max_score, cm, logger)
    
    mDao = m.match()

    logger.info("END matching")
    logger.info("BEGIN SAVING")
    mDao.delete()
    mDao.save()
    logger.info("END SAVING")

if __name__ == '__main__':
    
    if len(sys.argv)!=3 or sys.argv[1] not in ('-match','-clean'):
        print("usage:\n glimpse.main.Main -clean <cleaning name>\n glimpse.main.Main -match <matching name>")
    elif sys.argv[1]=="-clean":
        try:
            clean(sys.argv[2])
        except MissingException:
            print("The cleaning does not exist.")
            exit(-1)
    elif sys.argv[1]=="-match":
        try:
            compareAndClassify(sys.argv[2])
        except MissingException:
            print("The matching does not exist.")
            exit(-2)
    exit(0)