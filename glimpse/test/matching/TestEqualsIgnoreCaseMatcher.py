import unittest
from glimpse.matching.EqualsIgnoreCaseMatcher import EqualsIgnoreCaseMatcher

m = EqualsIgnoreCaseMatcher()

class TestEqualsIgnoreCaseMatcher(unittest.TestCase):


    def testScoreStrings1(self):
        m.setString1("casa")
        m.setString2("caso")
        assert(m.scoreStrings()==0)
        
    def testScoreStrings2(self):       
        m.setString1("casa")
        m.setString2(None)
        assert(m.scoreStrings()==0)
        
    def testScoreStrings3(self):    
        m.setString1("casa")
        m.setString2("casa")        
        assert(m.scoreStrings()==1)
        
    def testScoreStrings4(self):
        m.setString1("casa")
        m.setString2("cAsA")    
        assert(m.scoreStrings()==1)
        
    def testScoreStrings5(self):
        m.setString1("Casa")
        m.setString2("cAsA")  
        assert(m.scoreStrings()==1)
        
    def testScoreStrings6(self):
        m.setString1("CasO")
        m.setString2("cAsA")     
        assert(m.scoreStrings()==0)
        
    def testScoreStrings7(self):
        m.setString1("")
        m.setString2("cAsA")  
        assert(m.scoreStrings()==0)
        
    def testScoreStrings8(self):
        m.setString1("")
        m.setString2("")
        assert(m.scoreStrings()==1)
        
    def testScoreStrings9(self):
        m.setString1(None)
        m.setString2("")
        assert(m.scoreStrings()==0)
        
    def testScoreStrings10(self):
        m.setString1("00151")
        m.setString2("00151")      
        assert(m.scoreStrings()==1)
        
    def testScoreStrings11(self):
        m.setString1("00151")
        m.setString2("0151")
        assert(m.scoreStrings()==0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()