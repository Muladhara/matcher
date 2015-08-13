import unittest
from glimpse.blocking.BKTree import BKTree
from glimpse.stringUtils.StringMatcher import distance

class TestBKTree(unittest.TestCase):
    
    def testQuery1(self):
        t = BKTree(distance, ["paolo","michele","mario","maria","pino","dario","BAKUFU","BALBO","BOLESO","BOLETUS","CARAVELLI&VIRZI","CARBOTRASPORTI","CILLI3SRL","DECOTECH","LAPECORANERA","LAPIDEIIMPIANTISTICA","SLE","SLD","SLC","SLCC","SLIE","SLV","SLPSRL"])
        t.query("michela", 1)
        
    def testQuery2(self):
        t = BKTree(distance, ["paolo","michele","mario","maria","pino","dario","BAKUFU","BALBO","BOLESO","BOLETUS","CARAVELLI&VIRZI","CARBOTRASPORTI","CILLI3SRL","DECOTECH","LAPECORANERA","LAPIDEIIMPIANTISTICA","SLE","SLD","SLC","SLCC","SLIE","SLV","SLPSRL"])
        t.query("mariu",1)
        
    def testQuery3(self):
        t = BKTree(distance, ["paolo","michele","mario","maria","pino","dario","BAKUFU","BALBO","BOLESO","BOLETUS","CARAVELLI&VIRZI","CARBOTRASPORTI","CILLI3SRL","DECOTECH","LAPECORANERA","LAPIDEIIMPIANTISTICA","SLE","SLD","SLC","SLCC","SLIE","SLV","SLPSRL"])
        t.query("d'ario",2)
    
    def testQuery4(self):
        t = BKTree(distance, ["paolo","michele","mario","maria","pino","dario","BAKUFU","BALBO","BOLESO","BOLETUS","CARAVELLI&VIRZI","CARBOTRASPORTI","CILLI3SRL","DECOTECH","LAPECORANERA","LAPIDEIIMPIANTISTICA","SLE","SLD","SLC","SLCC","SLIE","SLV","SLPSRL"])       
        t.query("SLP",1)