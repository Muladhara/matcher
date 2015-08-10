#! -*- coding: utf-8 -*-
import unittest
from glimpse.cleaning.GeneralCleaning import GeneralCleaning

lf = GeneralCleaning()

class TestGeneralCleaning(unittest.TestCase):

    def testCleanValue(self):
        assert(lf.cleanValue("")=="")
    def testCleanValue2(self):
        assert(lf.cleanValue('"pippo"')=='pippo')
    def testCleanValue3(self):
        assert(lf.cleanValue("'pippo'")=='pippo')
    def testCleanValue4(self):
        assert(lf.cleanValue('pippo a pippo b')=='pippo a pippo')
    def testCleanValue5(self):
        assert(lf.cleanValue('pippo a pippo bb')=='pippo a pippo bb')
    def testCleanValue6(self):
        assert(lf.cleanValue('pippo  non  lo sa')=='pippo non lo sa')
    def testCleanValue7(self):
        assert(lf.cleanValue(None) is None)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()