import unittest

from glimpse.cleaning.ShortForCityParser import ShortForCityParser
from glimpse.utilities.ConfigurationManager import ConfigurationManager

class TestShortForCityParser(unittest.TestCase):
    
    def setUp(self):
        cm = ConfigurationManager()
        self.fltr = ShortForCityParser(cm)
    
    def testCleanValue1(self):
        assert(self.fltr.cleanValue("(RM)")=='RM')
    def testCleanValue2(self):
        assert(self.fltr.cleanValue("(1R)") is None)
    def testCleanValue3(self):
        assert(self.fltr.cleanValue("(12)") is None)
    def testCleanValue4(self):
        assert(self.fltr.cleanValue("(RMR)") is None)
    def testCleanValue5(self):
        assert(not self.fltr.cleanValue("(RM-)")=='RM')
    def testCleanValue6(self):
        assert(not self.fltr.cleanValue(" RM-")=='RM')
    def testCleanValue7(self):
        assert(not self.fltr.cleanValue(" -RM-")=='RM')
    def testCleanValue8(self):
        assert(self.fltr.cleanValue("") is None)
    def testCleanValue9(self):
        assert(self.fltr.cleanValue(None) is None)
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
