#! -*- coding: utf-8 -*-
import unittest
from glimpse.cleaning.EnterpriseFormFilter import EnterpriseFormFilter


class TestEnterpriseFormFilter(unittest.TestCase):

    def testCleanValue1(self):
        lf = EnterpriseFormFilter()
        assert(lf.cleanValue("")=="")
    
    def testCleanValue2(self):        
        lf = EnterpriseFormFilter()
        assert(lf.cleanValue("s.P. a. ")=="SPA")
    
    def testCleanValue3(self):        
        lf = EnterpriseFormFilter()
        assert(lf.cleanValue("s.r.l.")=="SRL")
    
    def testCleanValue4(self):        
        lf = EnterpriseFormFilter()
        assert(lf.cleanValue("societ in liquidazione")=="")
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()