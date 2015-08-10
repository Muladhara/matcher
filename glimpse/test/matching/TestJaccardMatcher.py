import unittest
from glimpse.matching.JaccardMatcher import JaccardMatcher

class TestJaccardMatcher(unittest.TestCase):


    def testScoreStrings(self):
        
        m = JaccardMatcher()
         
        m.setString1('MARIO CIPPI ALMA')
        m.setString2('LUCA MARIO PIETRO')
        assert(m.scoreStrings() == 0.2)
         
        m.setString1('LUCA')
        m.setString2('AMIL LUCA ELETTRO')
        assert(m.scoreStrings() == float(1/3.0))
         
        m.setString1('AP LUCA PUNK')
        m.setString2('LUCA ELETTRO POST PINK')
         
        assert(m.scoreStrings() == float(1/6.0))
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()