import unittest
from glimpse.blocking.InvertedIndex import InvertedIndex

class TestInvertedIndex(unittest.TestCase):

    def testAddWord(self):
     
        ii2 = InvertedIndex()
        ii2.addWord("FIAT", ("1","XY","ROMA","FIAT AUTO"))
        
        ii2.addWord("NINA", ("2","XY","ROMA","NINA COSTRUZIONI TORINO SRL")[0])
        ii2.addWord("COSTRUZIONI", ("2","XY","ROMA","NINA COSTRUZIONI TORINO SRL")[0])
        ii2.addWord("TORINO", ("2","XY","ROMA","NINA COSTRUZIONI TORINO SRL")[0])
        ii2.addWord("SRL", ("2","XY","ROMA","NINA COSTRUZIONI TORINO SRL")[0])
        
        ii2.addWord("COSTRUZIONI", ("3","XY","ROMA","EDIL COSTRUZIONI")[0])
        ii2.addWord("EDIL", ("3","XY","ROMA","EDIL COSTRUZIONI")[0])
        
        ii2.addWord("GLAXO", ("4","XY","ROMA","GLAXO SRL")[0])
        ii2.addWord("SRL", ("4","XY","ROMA","GLAXO SRL")[0])
        
        assert(ii2.getObjsByWord("SRL")==set(['2','4']))
        assert(ii2.getObjsByWord("TORINO")==set(['2']))
        
    def testGetWordFrequency(self):
        ii2 = InvertedIndex()
        
        ii2.addWord("NINA", 2)
        ii2.addWord("NINA", 5)
        ii2.addWord("NINA", 6)
        ii2.addWord("COSTRUZIONI", 2)
        ii2.addWord("COSTRUZIONI", 43)
        ii2.addWord("COSTRUZIONI", 8)
        ii2.addWord("COSTRUZIONI", 16)
        ii2.addWord("TORINO", 8)
        ii2.addWord("TORINO", 16)
        ii2.addWord("TORINO", 2)
        ii2.addWord("SRL", 2)
        
        assert(ii2.getWordFrequency("NINA") == 3.0/11)
        assert(ii2.getWordFrequency("PACO") == 0)
    
    def testGetTopWords(self):
        ii2 = InvertedIndex()
        ii2.addWord("NINA", 2)
        ii2.addWord("NINA", 5)
        ii2.addWord("NINA", 6)
        ii2.addWord("COSTRUZIONI", 2)
        ii2.addWord("COSTRUZIONI", 43)
        ii2.addWord("COSTRUZIONI", 8)
        ii2.addWord("COSTRUZIONI", 16)
        ii2.addWord("TORINO", 8)
        ii2.addWord("TORINO", 16)
        ii2.addWord("TORINO", 2)
        ii2.addWord("SRL", 2)
        assert(ii2.getTopWords(20) == [[4, 'COSTRUZIONI'], [3, 'TORINO'], [3, 'NINA'], [1, 'SRL']]) 
        