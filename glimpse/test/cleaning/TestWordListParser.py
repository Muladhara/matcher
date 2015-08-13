import unittest
from glimpse.cleaning.WordListParser import WordListParser
from glimpse.utilities.ConfigurationManager import ConfigurationManager


class TestWordListParser(unittest.TestCase):

    def setUp(self):
        self.cm = ConfigurationManager()
        self.fltr = WordListParser(self.cm, "test_cities.txt")
        
    def testCleanValue1(self):
        assert(self.fltr.cleanValue("a ROMA luigi")=="ROMA")
    def testCleanValue2(self):
        assert(self.fltr.cleanValue("sergio e' nato a MILANO il 3-4-56")=="MILANO")
    def testCleanValue3(self):
        assert(self.fltr.cleanValue("sergio e' nato a miLanO il 3-4-56")=="miLanO")
    def testCleanValue4(self):
        assert(self.fltr.cleanValue("TORINO")=="TORINO")
    def testCleanValue5(self):
        assert(self.fltr.cleanValue("Reggio nell'emilia")=="Reggio nell'emilia")
    def testCleanValue6(self):
        assert(self.fltr.cleanValue("Reggio nell'emilia")=="Reggio nell'emilia")
    def testCleanValue7(self):
        assert(self.fltr.cleanValue("Reg 1234567890")=="1234567890")
    def testCleanValue8(self):
        assert(self.fltr.cleanValue("SEDIA") is None)
    def testCleanValue9(self):
        assert(self.fltr.cleanValue(None) is None)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()