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
                pyb.stringcard(ranklchar + suitlchar) == j and pyb.stringcard(rankchar+suitlchar) == j:
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

# SHOW-SCORING TESTS ==================================================================================================
# would be nice if there were a way to grade these on all the internal printing, but let's just go by score
# TODO VERIFY THESE AND DO VARIATIONS IN THEIR TODOS
# If I really wanted to grit my teeth over this, I'd have the show-scoring return strings of all its sub-findings
# and key the unit tests on that. The current way still needs visual inspection to verify.

# nothing
class ShowTestNothing(unittest.TestCase):
    def test_shewtest_nothing(self):
        # todo should work in all orderings of hand and starter
        print("no score ---------------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Qh', '0c', '9s', '3d']]
        starter = pyb.stringcard('4d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,0)

# fifteens - two card, have a couple
class ShowTest2CardFifteen(unittest.TestCase):
    def test_shewtest_2card15(self):
        # todo should work in all orderings of hand and starter
        print("2 card fifteens --------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Qh', '0c', '9s', '3d']]
        starter = pyb.stringcard('5d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,4)

# 3 card 15
class ShowTest3CardFifteen(unittest.TestCase):
    def test_shewtest_3card15(self):
        # todo should work in all orderings of hand and starter
        print("3 card fifteens --------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['6h', '3c', '7s', '0d']]
        starter = pyb.stringcard('2d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,4)

# 4 card 15
class ShowTest4CardFifteen(unittest.TestCase):
    def test_shewtest_4card15(self):
        # todo should work in all orderings of hand and starter
        print("4 card fifteen ---------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Ah', '4c', '3s', '7d']]
        starter = pyb.stringcard('6d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,2)
        pass

# 5 card 15
class ShowTest5CardFifteen(unittest.TestCase):
    def test_shewtest_5card15(self):
        # todo should work in all orderings of hand and starter
        print("5 card fifteen (w/run)--------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Ah', '4c', '3s', '5d']]
        starter = pyb.stringcard('2d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,7)
        pass

# pair
class ShowTest1Pair(unittest.TestCase):
    def test_shewtest_1pair(self):
        # todo should work in all orderings of hand and starter
        print("one pair ---------------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Ah', '2c', '6s', '0d']]
        starter = pyb.stringcard('Ad')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,2)

# 2 pair
class ShowTest2Pair(unittest.TestCase):
    def test_shewtest_2pair(self):
        # todo should work in all orderings of hand and starter
        print("two pair ---------------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Ah', '0c', '6s', '0d']]
        starter = pyb.stringcard('Ad')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,4)

# 3 of a kind
class ShowTest3Pair(unittest.TestCase):
    def test_shewtest_2pair(self):
        # todo should work in all orderings of hand and starter
        print("three of a kind --------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Ah', 'Ac', '6s', '0d']]
        starter = pyb.stringcard('Ad')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,6)

# 3 of a kind and pair
class ShowTest3PairAndPair(unittest.TestCase):
    def test_shewtest_2pair(self):
        # todo should work in all orderings of hand and starter
        print("three of a kind and pair -----------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Ah', 'Ac', '4s', '4d']]
        starter = pyb.stringcard('Ad')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,8)

# 4 of a kind
class ShowTest4PairOfAKind(unittest.TestCase):
    def test_shewtest_6pair(self):
        # todo should work in all orderings of hand and starter
        print("four of a kind ---------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['4c', 'Ac', '4s', '4h']]
        starter = pyb.stringcard('4d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,12)

# run of 3
class ShowTestRunOf3(unittest.TestCase):
    def test_shewtest_run3(self):
        # todo should work in all orderings of hand and starter
        print("run of 3 ---------------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['8c', '9c', '0s', 'Qh']]
        starter = pyb.stringcard('Kd')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,3)

# run of 4, bottom (i.e., the odd card out is the highest ranked)
class ShowTestRunOf4Low(unittest.TestCase):
    def test_shewtest_run4low(self):
        # todo should work in all orerings of hand and starter
        print("run of 4 low plus fifteens ---------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['ac', '3c', '4s', 'Qh']]
        starter = pyb.stringcard('2d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,8)

# run of 4, top (i.e., odd card out is lowest ranked)
class ShowTestRunOf4High(unittest.TestCase):
    def test_shewtest_run4hi(self):
        # todo should work in all orderings of hand and starter (watch for nobs)
        print("run of 4 high ----------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['0c', 'jc', 'ks', 'Qh']]
        starter = pyb.stringcard('2d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,4)

# run of 5
class ShowTestRunOf5(unittest.TestCase):
    def test_shewtest_run5(self):
        # todo should work in all orderings of hand and starter (watch for nobs)
        print("run of five ------------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['9c', 'kc', 'js', 'Qh']]
        starter = pyb.stringcard('0d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,5)

# double run (3)
class ShowTestRunOf3Dbl(unittest.TestCase):
    def test_shewtest_run3dbl(self):
        # todo should work in all orderings of hand and starter
        print("double run of 3 --------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['8c', '0c', '9s', 'Qh']]
        starter = pyb.stringcard('0d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,8)

# double run (4)
class ShowTestRunOf4Dbl(unittest.TestCase):
    def test_shewtest_run4dbl(self):
        # todo should work in all orderings of hand and starter
        print("double run of 4 --------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['8c', '0c', '9s', 'jh']]
        starter = pyb.stringcard('0d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,10)

# double double run
class ShowTestRunOf3DblDbl(unittest.TestCase):
    def test_shewtest_run3dbldbl(self):
        # todo should work in all orderings of hand and starter
        print("double double run of 3 -------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['8c', '0c', '9s', '9h']]
        starter = pyb.stringcard('0d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,16)

# triple run
class ShowTestRunOf3Triple(unittest.TestCase):
    def test_shewtest_run3triple(self):
        # todo should work in all orderings of hand and starter
        print("triple run of 3 --------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['6h', '6c', '5s', '6d']]
        starter = pyb.stringcard('7c')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,15)

# 4 card flush
class ShowTest4CardFlush(unittest.TestCase):
    def test_shewtest_4cardflush(self):
        # todo should work in all orderings of hand, keep starter same
        print("4 card flush -----------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['4c', '3c', 'jc', '7c']]
        starter = pyb.stringcard('9h')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,4)

# 5 card flush
class ShowTest5CardFlush(unittest.TestCase):
    def test_shewtest_5cardflush(self):
        # todo should work in all orderings of hand and starter
        print("5 card flush -----------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['4c', '3c', 'qc', '7c']]
        starter = pyb.stringcard('9c')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,5)

# not 4 card flush bc the 4 incl starter
class ShowTestNot4CardFlush(unittest.TestCase):
    def test_shewtest_not4cardflush(self):
        # todo should work in all orderings of hand, keep starter same
        print("Not 4 card flush bc 4 cards incl starter -------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['4c', '3c', 'kc', '7h']]
        starter = pyb.stringcard('9c')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,0)

# nobs
class ShowTestNobs(unittest.TestCase):
    def test_shewtest_nobs(self):
        # todo should work in all orderings of hand, jack must be in hand, starter w suit of j
        print("nobs -------------------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Qh', 'Jd', '9s', '3d']]
        starter = pyb.stringcard('4d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,1)

# 29
class ShowTestZ29(unittest.TestCase):
    def test_shewtest_Z29(self):
        # TODO Should work in all scrambles except that jack must not be starter and starter must have same suit as j
        print("TWENTY-NINE!!! ---------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['5c', '5d', 'jh', '5s']]
        starter = pyb.stringcard('5h')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,29)

# illegal cases - ?
# TODO FIGURE THESE OUT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

if __name__ == '__main__':
    unittest.main()
