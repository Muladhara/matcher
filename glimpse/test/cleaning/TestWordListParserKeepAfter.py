import unittest
from glimpse.cleaning.WordListParserKeepAfter import WordListParserKeepAfter
from glimpse.utilities.ConfigurationManager import ConfigurationManager

class TestWordListParserKeepAfter(unittest.TestCase):

    def setUp(self):
        cm = ConfigurationManager()
        self.fltr = WordListParserKeepAfter(cm, "test_cities.txt")
        
    def testCleanValue1(self):
        assert(self.fltr.cleanValue("a ROMA Centro")==" Centro")
    def testCleanValue2(self):
        assert(not self.fltr.cleanValue("nata a ROMA il")=="ROMA")
    def testCleanValue3(self):
        assert(self.fltr.cleanValue("nata a RoMA il")==" il")
    def testCleanValue4(self):
        assert(self.fltr.cleanValue("SEDIA") =='SEDIA')
    def testCleanValue5(self):
        assert(self.fltr.cleanValue(None) is None)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()