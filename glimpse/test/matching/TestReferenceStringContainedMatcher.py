import unittest
from glimpse.matching.ReferenceStringContainedMatcher import ReferenceStringContainedMatcher

class TestReferenceStringContainedMatcher(unittest.TestCase):

    def testScoreStrings(self):
        m = ReferenceStringContainedMatcher()
        m.setString1("FIAT AUTO TORINO")
        m.setString2("TORINO")        
        assert(m.scoreStrings()==1)
     
        m.setString2("MARIO")
        assert(m.scoreStrings()==0)
         
        m.setString1("FIAT 00192")
        m.setString2("00192")
        assert(m.scoreStrings()==1)  
        m.setString1("FIAT 00192")
        m.setString2("000192")
        assert(m.scoreStrings()==0)
        
        m.setString1("FIAT 00192")
        m.setString2(None)
        assert(m.scoreStrings()==0)
        
        m.setString1(None)
        m.setString2("FIAT")
        assert(m.scoreStrings()==0)
        
        m.setString1(None)
        m.setString2(None)
        assert(m.scoreStrings()==0)
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()