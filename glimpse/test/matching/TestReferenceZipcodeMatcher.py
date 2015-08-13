import unittest
from glimpse.matching.ReferenceZipcodeMatcher import ReferenceZipcodeMatcher

class TestReferenceZipcodeMatcher(unittest.TestCase):


    def testName(self):
        pass


    def testGetCapFromStrings(self):
        m = ReferenceZipcodeMatcher()
        assert(m.getCapFromStrings("aaa00000 a asdf asd")=='00000')
        assert(m.getCapFromStrings("aaa100000 a asdf asd")=='10000')    
        assert(m.getCapFromStrings("aaa100000 a asdf 12345")=='10000')
    
    def testScoreStrings(self):
        m = ReferenceZipcodeMatcher()
        m.setString1("50330MARIO")
        m.setString2("50330")
        assert(m.scoreStrings()==1)
        
        m.setString1("503300MARIO")
        m.setString2("50330")
        assert(m.scoreStrings()==1)
        
        m.setString1("KZ503300MARIO")
        m.setString2("50330")
        assert(m.scoreStrings()==1)
        
        m.setString1("50300MARIO")
        m.setString2("50330")
        assert(m.scoreStrings()==0)
        
        m.setString1("50330 MARIO")
        m.setString2("50330")
        assert(m.scoreStrings()==1)
        
        m.setString1(None)
        m.setString2("50330")
        assert(m.scoreStrings()==0)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()