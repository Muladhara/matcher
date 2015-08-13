import unittest

from glimpse.cleaning.ZipcodeParser import ZipcodeParser
from glimpse.utilities.ConfigurationManager import ConfigurationManager

class TestZipCodeParser(unittest.TestCase):


    def setUp(self):
        cm = ConfigurationManager()
        self.fltr = ZipcodeParser(cm)

    def testCleanValue1(self):
        assert(self.fltr.cleanValue('prova 00195roma')=='00195')
    def testCleanValue2(self):
        assert(self.fltr.cleanValue('prova00195 roma')=='00195')
    def testCleanValue3(self):
        assert(self.fltr.cleanValue('prova00195roma')=='00195')
    def testCleanValue4(self):
        assert(self.fltr.cleanValue('prova 000195roma')=='00195')
    def testCleanValue5(self):
        assert(self.fltr.cleanValue('prova   000195roma')=='00195')
    def testCleanValue6(self):
        assert(self.fltr.cleanValue('prova   0000195roma')=='00195')
    def testCleanValue7(self):
        assert(self.fltr.cleanValue('prova  ') is None)
    def testCleanValue8(self):
        assert(self.fltr.cleanValue(None) is None)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()