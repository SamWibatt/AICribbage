import unittest
from pyb import pybbage as pyb

class StrcardCardstrTestAllLegit(unittest.TestCase):
    def test_cardstr_back(self):
        # test that all values from 0..51 translate back and forth correctly
        nummatch = 0
        for j in range(0,52):
            if pyb.stringcard(pyb.cardstring(j)) == j:
                nummatch += 1
        self.assertEqual(nummatch,52)

class StrcardTestAllLegit(unittest.TestCase):
    def test_strcard_legit(self):
        # test that all upper and lowercase variations of rank and suit match the expected card 0..51
        ranks = 'A234567890JQK'
        suits = 'HDCS'
        suits2 = '♥♦♣♠'
        numgood = 0
        for j in range(0,52):
            rankchar = ranks[j//4]
            ranklchar = str.lower(rankchar)
            suitchar = suits[j%4]
            suitlchar = str.lower(suitchar)
            suit2char = suits2[j%4]
            if pyb.stringcard(rankchar+suitchar) == j and pyb.stringcard(rankchar+suit2char) == j and \
                pyb.stringcard(ranklchar+suitchar) == j and pyb.stringcard(ranklchar+suit2char) == j and \
                pyb.stringcard(ranklchar + suitlchar) == j and pyb.stringcard(ranklchar+suitchar) == j:
                numgood += 1
        self.assertEqual(numgood,52)

class CardstrTestAllLegit(unittest.TestCase):
    def test_cardstr_legit(self):
        # test that all values for card 0..51 get back the correct rank and suit
        ranks = 'A234567890JQK'
        suits2 = '♥♦♣♠'
        numgood = 0
        for j in range(0,52):
            if pyb.cardstring(j) == ranks[pyb.rank(j)] + suits2[pyb.suit(j)]:
                numgood += 1
        self.assertEqual(numgood,52)


if __name__ == '__main__':
    unittest.main()
