import unittest
from glimpse.matching.WeightedJaccardMatcher import WeightedJaccardMatcher
from glimpse.blocking.InvertedIndex import InvertedIndex

class TestWeightedJaccardMatcher(unittest.TestCase):

    def testScoreStrings(self):
        ii = InvertedIndex()
        m = WeightedJaccardMatcher(ii)
        m.setString1("ACACIA ROMA")
        m.setString2("LUIGI ROMA")
        
        ii.addWord("ACACIA", 1)
        ii.addWord("ROMA", 1)
        ii.addWord("LUIGI", 2)
        ii.addWord("ROMA", 2)
        
        
        print(m.scoreStrings(ii))
        assert(m.scoreStrings(ii)==0.25)
        
        ii = InvertedIndex()
        m = WeightedJaccardMatcher(ii)
        m.setString1("ACACIA industrie ROMA SPA")
        m.setString2("LUIGI ROMA SRL")
        ii.addWord("ACACIA", 1)
        ii.addWord("industrie", 1)
        ii.addWord("ROMA", 1)
        ii.addWord("SPA", 1)
        ii.addWord("SRL", 2)
        ii.addWord("LUIGI", 2)
        ii.addWord("ROMA", 2)
        print(m.scoreStrings(ii))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()