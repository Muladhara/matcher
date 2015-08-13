#! -*- coding: utf-8 -*-
import unittest
from glimpse.cleaning.EnterpriseFormFilter import EnterpriseFormFilter

lf = EnterpriseFormFilter()

class TestEnterpriseFormFilterNoUTF8(unittest.TestCase):
    
    def testCleanValue1(self):
        assert(lf.cleanValue("fiatin fallimento")=="fiat")
        
    def testCleanValue2(self):        
        assert(lf.cleanValue("") == "")
        
    def testCleanValue3(self):        
        assert(lf.cleanValue("SOCI età")=="SOCIETA")
        
    def testCleanValue4(self):        
        assert(lf.cleanValue("MARIO IN FORMA ABBREVIATA M")=="MARIO")
        
    def testCleanValue5(self):        
        assert(lf.cleanValue("MARIO in breve M")=="MARIO")
        
    def testCleanValue6(self):        
        assert(lf.cleanValue("MARIO o per breVita M")=="MARIO")
        
    def testCleanValue7(self):        
        assert(lf.cleanValue("D.G.T. S.r.l.")=='DGT SRL')
        
    def testCleanValue8(self):        
        assert(lf.cleanValue("L.K.M.")=="LKM")
        
    def testCleanValue9(self):        
        assert(lf.cleanValue("PATENT DEPT")=='')
        
    def testCleanValue10(self):        
        assert(lf.cleanValue("PATENT DEPT 34")=='')
        
    def testCleanValue11(self):        
        assert(lf.cleanValue("PATENT DEPT 34/B")=='')
        
    def testCleanValue12(self):        
        assert(lf.cleanValue("WHIRLPOOL EUROPE SRL PATENT DEPT")=="WHIRLPOOL EUROPE SRL")
        
    def testCleanValue13(self):        
        assert(lf.cleanValue("FISCHER MARCUS R PATENT DEPT")=="FISCHER MARCUS")
        
    def testCleanValue14(self):        
        assert(lf.cleanValue("Fischer, Marcus R. Patent Dept.")=="Fischer Marcus")
        
    def testCleanValue15(self):        
        assert(lf.cleanValue("Zhang Zheng Patent Dept Whirlpool Europe SRL")=="Zhang Zheng Whirlpool Europe SRL")

    def testCleanValue16(self):
        assert(lf.cleanValue("33")=="")
        
    def testCleanValue17(self):
        assert(lf.cleanValue("REGIONE PERNIGOTTI 24")=="REGIONE PERNIGOTTI")
                
    def testCleanValue18(self):        
        assert(lf.cleanValue(None) is None)
                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()