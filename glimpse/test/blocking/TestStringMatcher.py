import unittest
from glimpse.stringUtils.StringMatcher import StringMatcher

class Test(unittest.TestCase):

    def setUp(self):
        self.sm = StringMatcher()
    
    def testDistance(self):
        self.sm.set_seq1("marco")
        self.sm.set_seq2("pippo")
        d = self.sm.distance()
        self.assertEqual(d, 4)
        self.sm.set_seq2("marco")
        d2 = self.sm.distance()
        self.assertEqual(d2, 0)