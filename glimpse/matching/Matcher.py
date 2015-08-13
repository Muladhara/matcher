from JaccardMatcher import JaccardMatcher
from ReferenceStringContainedMatcher import ReferenceStringContainedMatcher
from ReferenceZipcodeMatcher import ReferenceZipcodeMatcher
from WeightedJaccardMatcher import WeightedJaccardMatcher
from EqualsIgnoreCaseMatcher import EqualsIgnoreCaseMatcher

class Matcher():
    '''
    Handles the matching of record lists
    '''
    
    def loadConfiguration(self):
        '''
        Loads the general configuration
        '''
        self.sx_limit = int(self.cm.getProperty("general","sx_limit"))
        
    def __init__(self, sourceDb1, sourceDb2, 
               matches, outDao, 
               bkTreeIndex, ii, sx_limit, 
               search_discard_words, blocking_column_1, levThreshold, 
               columns_from_to_db1_indices, columns_from_to_db2_indices,
               score_columns, global_score_column,
               keep_only_max_score, 
               cm, logger):
        '''
        Initializes the matcher.
        Arguments:
        sourceDb1: the dao of database to match
        sourceDb2: the dao of reference database
        matches: list of matches [colDb1, colDb2,'criterion',<threshold>]
        outDao: the dao of the output database
        bkTreeIndex: a BK-Tree index of the sourceDb2
        ii: an inverted index of the sourceDb2
        sx_limit: the number of rows in sourceDb1 to consider for the matching
        search_discard_words: words not to consider for the search (exclude from blocking)
        blocking_column_1: the column in sourceDb1 to consider for the blocking
        levThreshold: the distance threshold to use in the blocking
        columns_from_to_db1_indices: [(db1index, targetIndex)] pairs of indices from source db to target
        columns_from_to_db2_indices: [(db2index, targetIndex)] pairs of indices from source db to target
        score_columns : [x, ..., ] indices of the score columms
        global_score_column : index of the global score column        
        keep_only_max_score: if for each set of candidate matchings, only the match with top score must be kept
        cm: the ConfigurationManager
        logger: the logger
        '''
        self.sourceDb1 = sourceDb1
        self.sourceDb2 = sourceDb2
        self.outDao = outDao
        self.bkTreeIndex = bkTreeIndex
        self.ii = ii
        self.search_discard_words = search_discard_words
        self.blocking_column_1 = blocking_column_1
        self.levThreshold = levThreshold
        
        self.columns_from_to_db1_indices = columns_from_to_db1_indices
        self.columns_from_to_db2_indices = columns_from_to_db2_indices
        self.score_columns = score_columns
        self.global_score_column = global_score_column
        
        self.keep_only_max_score = keep_only_max_score
        self.cm = cm
        self.logger = logger
        
        self.loadConfiguration()
        
        # builds a list of [ (col_db1, col_db2), matcher, threshold ]
        self.mList = list()
        # for each Match creates a matcher with the appropriate criterion
        # matches (1,2,'criterion',criterion_threshold)
        for match in matches:
            
            # extracts the threshold (if present) for the matcher
            try:
                th = match[3]
            except IndexError:
                th = None
            
            if match[2]=='weighted_jaccard':
                specMatcher = WeightedJaccardMatcher(ii)
            elif match[2]=='jaccard':
                specMatcher = JaccardMatcher()
            elif match[2]=='reference_string_contained':
                specMatcher=ReferenceStringContainedMatcher()
            elif match[2]=='reference_zipcode_contained':
                specMatcher=ReferenceZipcodeMatcher()
            elif match[2]=='equals_ignorecase':
                specMatcher=EqualsIgnoreCaseMatcher()
             
            self.mList.append( ( (match[0],match[1]), specMatcher, th) )

    def match(self):
        '''
        Performs a matching on the basis of the parameters passed in the constructor
        and returns the outputDao
        '''
        # extracts the tuples from the first db
        patstatDb = self.sourceDb1.getCleanDb()
        # extracts the tuples from the second database
        aidaDb = self.sourceDb2.getCleanDb()
        
        # extracts parameters from the constructor
        ii = self.ii
        bkTreeIndex = self.bkTreeIndex
        logger = self.logger
        sx_limit = self.sx_limit
        search_discard_words = self.search_discard_words
        blocking_column_1 = self.blocking_column_1
        mList = self.mList
        levThreshold = self.levThreshold
        columns_from_to_db1_indices = self.columns_from_to_db1_indices
        columns_from_to_db2_indices = self.columns_from_to_db2_indices
        score_columns = self.score_columns
        global_score_column = self.global_score_column
        
        keep_only_max_score = self.keep_only_max_score
        mDao = self.outDao
        
        # for each row in db1
        matchLen = float((len(patstatDb) if sx_limit==-1 else int(sx_limit) ))
        progr = 0
        percInt = 0
        percIntOld = -1
        for pdb in patstatDb:
            
            # prints a progress indicator
            percInt=int((progr / matchLen*100))
            if percInt % 5 == 0 and percInt!=percIntOld:
                logger.info("Progress " + str(percInt) + " %")
                percIntOld=percInt
            progr += 1
            
            # to match only a limited number of rows
            if(sx_limit!=-1 and progr>sx_limit):
                break
            
            aidaIdSet = set() # set of candidate ids individuated in the blocking
            
            # extracts the value of the blocking column in db1 and tokenizes it
            wordSet = set((pdb[blocking_column_1]).split(" "))
            # for each token
            for word in wordSet:
                # extracts the tokens in db2 with
                # distance <= levThreshold
                if word not in search_discard_words:
                    if levThreshold>0:
                        aidaWords = bkTreeIndex.query(word, levThreshold)
                    # if distance==0, then the word is directly put
                    # among the ones to be looked up in the inverse index
                    else:
                        aidaWords = set()
                        aidaWords.add((0,word))
                else:
                    aidaWords = set()
    
                # for each word in db2, the respective rownum are extracted from the inverse index
                for word in aidaWords:
                    aidas = ii.getObjsByWord(str(word[1]))
                    # the new rownums are collected
                    if aidas is not None:
                        for aid in aidas:
                            aidaIdSet.add(aid)
                    
            # for each tuple of db1, we have all the candidate ids of db2 in aidaIdSet
            # evaluates every candidate
            bestCandidates = self.pickBestNCandidates(pdb, aidaIdSet, aidaDb, ii, mList, keep_only_max_score)
            # returns bestCandidates for the row pdb
            # bestCandidates [(rownum, partialScoreList, score), ... , (rownum, partialScoreList, score)]
            
            for c in bestCandidates:
                rownum = c[0]
                partialScoreList = c[1]
                score = c[2]
                # builds the resulting tuple: columns from db1 + columns from db2 + partialScores + global score
                
                # lists value, position in the target
                values_pos_from_db1 = [(pdb[x],y) for (x,y) in columns_from_to_db1_indices] # inserire in posizione y
                values_pos_from_db2 = [(aidaDb[rownum][x],y) for (x,y) in columns_from_to_db2_indices] # inserire in posizione y
                value_pos_for_score = zip(partialScoreList, score_columns) # ordinatamente inserire in posizione score_columns
                value_pos_for_g_score = [(score,global_score_column)] # inserire in posizione global_score_column
                
                daoList = values_pos_from_db1 + values_pos_from_db2 + value_pos_for_score + value_pos_for_g_score
                # sorts by position
                daoList = sorted(daoList, key = lambda x : x[1])
                # creates the daoTuple to insert
                daoTuple = [x for (x,y) in daoList]
                
                #daoTuple = [pdb[i] for i in columns_from_db1_indices] + [aidaDb[rownum][j] for j in columns_from_db2_indices] + partialScoreList + [score]
                mDao.addRow(daoTuple)
       
        return mDao

    def pickBestNCandidates(self, pdb, aidaIdSet, aidaDb, ii, mList, keep_only_max_score):
        '''
        For a db1 tuple and a set of candidate rownums, returns a list 
        [(rownum, partialScoreList, score), ... , (rownum, partialScoreList, score)]
        of best candidates with scores.
        Arguments:
        pdb: record of db1
        aidaIdSet: set of candidate rownums
        aidaDb: candidate records
        ii: inverted index to have word statistics
        mList: a list of [ (col_db1, col_db2), matcher, threshold ]
        keep_only_max_score: if only the candidate with top score must be kept
        '''
        
        # for each (col_db1 index, col_db2 index, matcher, threshold) in mList
        # sets the fields to check in the Matcher
        for mTuple in mList:
            matcher = mTuple[1]
            mIndexDb1 = mTuple[0][0]
            matcher.setString1(pdb[mIndexDb1])
        
        max_score = 0.0
        
        scoreList=list()
        # for each row of the candidates in the db2
        for rownum in aidaIdSet:
            score=0.0
            partialScoreList=list()
            adb = aidaDb[rownum]
            candidateToAdd = True
            # calculates the score for each match criterion
            for mTuple in mList:
                matcher = mTuple[1]
                mIndexDb2 = mTuple[0][1]
                matcher.setString2(adb[mIndexDb2])
                criterionScore = matcher.scoreStrings(ii)
                partialScoreList.append(criterionScore) # saves the partial score
                

                # threshold for current matching
                matchThreshold = mTuple[2]
                print(criterionScore)
                
                print(matchThreshold)
                if matchThreshold is not None and float(criterionScore) < float(matchThreshold): # if the threshold is violated (if present)
                    candidateToAdd = False
                    break
                
                score += float(criterionScore)
            
            # if for every criterion the threshold is respected then the candidate is added to the list
            # lista [(rownum,partialScoreList,score) , ...)]
            if candidateToAdd:
                scoreList.append((rownum,partialScoreList,score))
                # and the top score is updated
                max_score = max(max_score,score)
        
        # keeps only the top score candidate
        # all candidates, if having the same score
        if keep_only_max_score:
            bestN = filter(lambda x: x[2]==max_score, scoreList)
        
        return bestN
    

    

    
