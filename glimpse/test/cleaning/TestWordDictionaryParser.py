import unittest
from glimpse.cleaning.WordDictionaryParser import WordDictionaryParser
from glimpse.utilities.ConfigurationManager import ConfigurationManager

class TestWordDictionaryParser(unittest.TestCase):

    def setUp(self):
        cm = ConfigurationManager()
        self.fltr = WordDictionaryParser(cm, "test_cities_dict.txt")

    def testCleanValue1(self):
        assert(self.fltr.cleanValue(None) is None)
    def testCleanValue2(self):
        assert(self.fltr.cleanValue("") is None)
    def testCleanValue3(self):
        assert(self.fltr.cleanValue("RM") == "ROMA")
    def testCleanValue4(self):
        assert(self.fltr.cleanValue("RM") != "TORINO")
    def testCleanValue5(self):
        assert(self.fltr.cleanValue("sono nato a to il 23-05.2013") == "TORINO")
    def testCleanValue6(self):
        assert(self.fltr.cleanValue("sono di rM e di mi") is None)
    def testCleanValue7(self):
        assert(self.fltr.cleanValue("sono di mI")=='MILANO')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()