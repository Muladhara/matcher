import unittest
from glimpse.cleaning.WordListParserKeepBefore import WordListParserKeepBefore
from glimpse.utilities.ConfigurationManager import ConfigurationManager

class TestWordListParserKeepBefore(unittest.TestCase):

    def setUp(self):
        cm = ConfigurationManager()
        self.fltr = WordListParserKeepBefore(cm, "test_cities.txt")

    def testCleanValue2(self):
        assert(self.fltr.cleanValue("a ROMA Centro")=="a")
    def testCleanValue3(self):
        assert(self.fltr.cleanValue("l'azienda si trova a ROMA Centro")=="l'azienda si trova a")
    def testCleanValue4(self):
        assert(self.fltr.cleanValue("l'azienda si trova c/o Milano")=="l'azienda si trova c/o")
    def testCleanValue5(self):
        assert(self.fltr.cleanValue("SEDIA") == 'SEDIA')
    def testCleanValue6(self):
        assert(self.fltr.cleanValue("Abito in Corso Francia") =='Abito in')        
    def testCleanValue7(self):
        assert(self.fltr.cleanValue(None) is None)

        cm = ConfigurationManager()
        self.fltr = WordListParserKeepBefore(cm, "streets_prefix.txt")
        
        #print(self.fltr.cleanValue("c/o Fiat group automobiles S.p.A. Corso Settembrini, 40"))
        #print(self.fltr.cleanValue("c/o Fiat group automobiles S.p.A. 40,       strada Settembrini"))
        #print(self.fltr.cleanValue("per Azioni Strada Torino"))
        #print(self.fltr.cleanValue("Via Paris Bordone, 82  Frazione Biancade"))
        #print(self.fltr.cleanValue("Via XXV Aprile 60"))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()