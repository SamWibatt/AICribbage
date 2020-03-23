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
# Numbering by 10s a la BASIC so can keep them in order and have room to add more

# nothing
class ShowTest000_Nothing(unittest.TestCase):
    def test_shewtest_nothing(self):
        # todo should work in all orderings of hand and starter
        print("Show no score ----------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Qh', '0c', '9s', '3d']]
        starter = pyb.stringcard('4d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,0)

# fifteens - two card, have a couple
class ShowTest010_2CardFifteen(unittest.TestCase):
    def test_shewtest_2card15(self):
        # todo should work in all orderings of hand and starter
        print("Show 2 card fifteens ---------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Qh', '0c', '9s', '3d']]
        starter = pyb.stringcard('5d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,4)

# 3 card 15
class ShowTest020_3CardFifteen(unittest.TestCase):
    def test_shewtest_3card15(self):
        # todo should work in all orderings of hand and starter
        print("Show 3 card fifteens ---------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['6h', '3c', '7s', '0d']]
        starter = pyb.stringcard('2d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,4)

# 4 card 15
class ShowTest030_4CardFifteen(unittest.TestCase):
    def test_shewtest_4card15(self):
        # todo should work in all orderings of hand and starter
        print("Show 4 card fifteen ----------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Ah', '4c', '3s', '7d']]
        starter = pyb.stringcard('6d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,2)
        pass

# 5 card 15
class ShowTest040_5CardFifteen(unittest.TestCase):
    def test_shewtest_5card15(self):
        # todo should work in all orderings of hand and starter
        print("Show 5 card fifteen (w/run)---------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Ah', '4c', '3s', '5d']]
        starter = pyb.stringcard('2d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,7)
        pass

# pair
class ShowTest050_1Pair(unittest.TestCase):
    def test_shewtest_1pair(self):
        # todo should work in all orderings of hand and starter
        print("Show one pair ----------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Ah', '2c', '6s', '0d']]
        starter = pyb.stringcard('Ad')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,2)

# 2 pair
class ShowTest060_2Pair(unittest.TestCase):
    def test_shewtest_2pair(self):
        # todo should work in all orderings of hand and starter
        print("Show two pair ----------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Ah', '0c', '6s', '0d']]
        starter = pyb.stringcard('Ad')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,4)

# 3 of a kind
class ShowTest070_3Pair(unittest.TestCase):
    def test_shewtest_2pair(self):
        # todo should work in all orderings of hand and starter
        print("Show three of a kind ---------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Ah', 'Ac', '6s', '0d']]
        starter = pyb.stringcard('Ad')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,6)

# 3 of a kind and pair
class ShowTest080_3PairAndPair(unittest.TestCase):
    def test_shewtest_2pair(self):
        # todo should work in all orderings of hand and starter
        print("Show three of a kind and pair ------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Ah', 'Ac', '4s', '4d']]
        starter = pyb.stringcard('Ad')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,8)

# 4 of a kind
class ShowTest090_4PairOfAKind(unittest.TestCase):
    def test_shewtest_6pair(self):
        # todo should work in all orderings of hand and starter
        print("Show four of a kind ----------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['4c', 'Ac', '4s', '4h']]
        starter = pyb.stringcard('4d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,12)

# run of 3
class ShowTest100_RunOf3(unittest.TestCase):
    def test_shewtest_run3(self):
        # todo should work in all orderings of hand and starter
        print("Show run of 3 ----------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['8c', '9c', '0s', 'Qh']]
        starter = pyb.stringcard('Kd')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,3)

# run of 4, bottom (i.e., the odd card out is the highest ranked)
class ShowTest110_RunOf4Low(unittest.TestCase):
    def test_shewtest_run4low(self):
        # todo should work in all orerings of hand and starter
        print("Show run of 4 low plus fifteens ----------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['ac', '3c', '4s', 'Qh']]
        starter = pyb.stringcard('2d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,8)

# run of 4, top (i.e., odd card out is lowest ranked)
class ShowTest120_RunOf4High(unittest.TestCase):
    def test_shewtest_run4hi(self):
        # todo should work in all orderings of hand and starter (watch for nobs)
        print("Show run of 4 high -----------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['0c', 'jc', 'ks', 'Qh']]
        starter = pyb.stringcard('2d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,4)

# run of 5
class ShowTest130_RunOf5(unittest.TestCase):
    def test_shewtest_run5(self):
        # todo should work in all orderings of hand and starter (watch for nobs)
        print("Show run of five -------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['9c', 'kc', 'js', 'Qh']]
        starter = pyb.stringcard('0d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,5)

# double run (3)
class ShowTest140_RunOf3Dbl(unittest.TestCase):
    def test_shewtest_run3dbl(self):
        # todo should work in all orderings of hand and starter
        print("Show double run of 3 ---------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['8c', '0c', '9s', 'Qh']]
        starter = pyb.stringcard('0d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,8)

# double run (4)
class ShowTest150_RunOf4Dbl(unittest.TestCase):
    def test_shewtest_run4dbl(self):
        # todo should work in all orderings of hand and starter
        print("Show double run of 4 ---------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['8c', '0c', '9s', 'jh']]
        starter = pyb.stringcard('0d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,10)

# double double run
class ShowTest160_RunOf3DblDbl(unittest.TestCase):
    def test_shewtest_run3dbldbl(self):
        # todo should work in all orderings of hand and starter
        print("Show double double run of 3 --------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['8c', '0c', '9s', '9h']]
        starter = pyb.stringcard('0d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,16)

# triple run
class ShowTest170_RunOf3Triple(unittest.TestCase):
    def test_shewtest_run3triple(self):
        # todo should work in all orderings of hand and starter
        print("Show triple run of 3 ---------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['6h', '6c', '5s', '6d']]
        starter = pyb.stringcard('7c')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,15)

# 4 card flush
class ShowTest180_4CardFlush(unittest.TestCase):
    def test_shewtest_4cardflush(self):
        # todo should work in all orderings of hand, keep starter same
        print("Show 4 card flush ------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['4c', '3c', 'jc', '7c']]
        starter = pyb.stringcard('9h')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,4)

# 5 card flush
class ShowTest190_5CardFlush(unittest.TestCase):
    def test_shewtest_5cardflush(self):
        # todo should work in all orderings of hand and starter
        print("Show 5 card flush ------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['4c', '3c', 'qc', '7c']]
        starter = pyb.stringcard('9c')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,5)

# not 4 card flush bc the 4 incl starter
class ShowTest200_Not4CardFlush(unittest.TestCase):
    def test_shewtest_not4cardflush(self):
        # todo should work in all orderings of hand, keep starter same
        print("Show Not 4 card flush bc 4 cards incl starter --------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['4c', '3c', 'kc', '7h']]
        starter = pyb.stringcard('9c')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,0)

# nobs
class ShowTest210_Nobs(unittest.TestCase):
    def test_shewtest_nobs(self):
        # todo should work in all orderings of hand, jack must be in hand, starter w suit of j
        print("Show nobs --------------------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['Qh', 'Jd', '9s', '3d']]
        starter = pyb.stringcard('4d')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,1)

# 29
class ShowTest220_Z29(unittest.TestCase):
    def test_shewtest_Z29(self):
        # TODO Should work in all scrambles except that jack must not be starter and starter must have same suit as j
        print("Show TWENTY-NINE!!! ----------------------------------------------------------------------------------")
        hand = [pyb.stringcard(x) for x in ['5c', '5d', 'jh', '5s']]
        starter = pyb.stringcard('5h')
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter))
        score = pyb.score_shew(hand,starter)
        self.assertEqual(score,29)

# illegal cases - ?
# TODO FIGURE THESE OUT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# PLAY-SCORING TESTS ==================================================================================================
# would be nice if there were a way to grade these on all the internal printing, but let's just go by score
# TODO VERIFY THESE AND DO VARIATIONS IN THEIR TODOS
# If I really wanted to grit my teeth over this, I'd have the show-scoring return strings of all its sub-findings
# and key the unit tests on that. The current way still needs visual inspection to verify.
#
#     curcards = []
#     handcards = ['5h','5c','5d','5s','4h','6d','as','qh']
#     for nc in handcards:
#         newcard = stringcard(nc)
#         print("playing",cardstring(newcard),"on",[cardstring(x) for x in curcards])
#         (resultcards,resscore) = play_card(curcards,newcard)
#         print("Result cards:",[cardstring(x) for x in resultcards],"score",resscore)
# Numbering by 10s a la BASIC so can keep them in order and have room to add more

class PlayTest000_firstcard(unittest.TestCase):
    def test_playtest_1stcard(self):
        print("Play first card --------------------------------------------------------------------------------------")
        curcards = []           # cards already played
        newcard = pyb.stringcard('7h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,[newcard])
        self.assertEqual(curtotal,pyb.val(newcard))
        self.assertEqual(resscore,0)

class PlayTest003_fifteen(unittest.TestCase):
    def test_playtest_fifteen(self):
        print("Play fifteen -----------------------------------------------------------------------------------------")
        curcards = [pyb.stringcard('5d')]           # cards already played
        newcard = pyb.stringcard('jh')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,2)

class PlayTest007_thirtyone(unittest.TestCase):
    def test_playtest_thirtyone(self):
        print("Play thirtyone ---------------------------------------------------------------------------------------")
        curcs = ['5d','jh','ac','5h']           # cards already played
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('qh')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,2)

class PlayTest010_pair(unittest.TestCase):
    def test_playtest_pair(self):
        print("Play pair --------------------------------------------------------------------------------------------")
        curcards = [pyb.stringcard('3d')]           # cards already played
        newcard = pyb.stringcard('3h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,2)

class PlayTest020_notpair(unittest.TestCase):
    def test_playtest_notpair(self):
        print("Play not pair bc intervening card --------------------------------------------------------------------")
        curcs = ['2c','7s']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('2h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,0)

class PlayTest030_3ofakind(unittest.TestCase):
    def test_playtest_3ofakind(self):
        print("Play 3 of a kind -------------------------------------------------------------------------------------")
        curcs = ['4c','4s']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('4h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,6)

class PlayTest040_not3ofakind(unittest.TestCase):
    def test_playtest_not3ofakind(self):
        print("Play 3 of a kind not bc intervening pair instead -----------------------------------------------------")
        curcs = ['4c','Qd','4s']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('4h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,2)

class PlayTest050_4ofakind(unittest.TestCase):
    def test_playtest_4ofakind(self):
        print("Play 4 of a kind -------------------------------------------------------------------------------------")
        curcs = ['6c','6s','6d']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('6h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,12)

class PlayTest060_not4ofakind(unittest.TestCase):
    def test_playtest_not4ofakind(self):
        print("Play 4 of a kind not bc intervening pair instead -----------------------------------------------------")
        curcs = ['2c', '2d', 'Qd','2s']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('2h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,2)

# runs
class PlayTest070_runof3(unittest.TestCase):
    def test_playtest_runof3(self):
        print("Play run of 3 ----------------------------------------------------------------------------------------")
        curcs = ['ac','2s']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('3h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,3)

class PlayTest080_runof3ooo(unittest.TestCase):
    def test_playtest_runof3ooo(self):
        print("Play run of 3 out of order ---------------------------------------------------------------------------")
        curcs = ['8c','6s']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('7h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,3)

class PlayTest090_runof3intervening(unittest.TestCase):
    def test_playtest_runof3int(self):
        print("Play run of 3 broken with intervening card -----------------------------------------------------------")
        curcs = ['5c','6s','Jd']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('7h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,0)

# TODO HEY DO THIS ONE from http://cribbagecorner.com/cribbage-rules-play
#
#scoring sequence in play
#Submitted by Meade (not verified) on Tue, 04/06/2010 - 01:50.
#
#How do you score the following sequence made in play? A 7 was played first followed by a 9 and then a 8 to make a
# sequence of three for 3 points. Here is the questions: My playing partner then played a 7. Is this another sequence
# of three for 3 points and 2 points for 31?
#
#re: scoring sequence
#Submitted by Joan (not verified) on Thu, 06/24/2010 - 17:44.
#
#Yes, your parntner gets 3 points for the run of 7, 8, 9, the last 3 cards played where the sequence was not broken.
# And the 2 points for 31. If 8 or 9 were played first your partner would be out of luck because the first 7 played
# would have interrupted the second sequence.


class PlayTest100_runof4(unittest.TestCase):
    def test_playtest_runof4(self):
        print("Play run of 4 ----------------------------------------------------------------------------------------")
        curcs = ['ac','2s','3s']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('4h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,4)

class PlayTest110_runof4ooo(unittest.TestCase):
    def test_playtest_runof4ooo(self):
        print("Play run of 4 out of order ---------------------------------------------------------------------------")
        curcs = ['8c','6s','5c']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('7h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,4)

class PlayTest120_runof4intervening(unittest.TestCase):
    def test_playtest_runof4int(self):
        print("Play run of 4 broken with intervening card -----------------------------------------------------------")
        curcs = ['ac','2s','Jd','3c']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('4h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,0)

class PlayTest130_runof5(unittest.TestCase):
    def test_playtest_runof5(self):
        print("Play run of 5 ----------------------------------------------------------------------------------------")
        curcs = ['2c','3s','4s','5h']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('6d')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,5)

class PlayTest140_runof5ooo(unittest.TestCase):
    def test_playtest_runof5ooo(self):
        print("Play run of 5 out of order ---------------------------------------------------------------------------")
        curcs = ['8c','6s','5c','4d']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('7h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,5)

class PlayTest150_runof5intervening(unittest.TestCase):
    def test_playtest_runof5int(self):
        print("Play run of 5 broken with intervening card -----------------------------------------------------------")
        curcs = ['ac','2s','4h','Jd','3c']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('5h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,0)

class PlayTest160_runof6(unittest.TestCase):
    def test_playtest_runof6(self):
        print("Play run of 6 ----------------------------------------------------------------------------------------")
        curcs = ['2c','3s','4s','5h','6d']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('7c')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,6)

class PlayTest170_runof6ooo(unittest.TestCase):
    def test_playtest_runof6ooo(self):
        print("Play run of 6 out of order ---------------------------------------------------------------------------")
        curcs = ['3c','6s','5c','4d','2h']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('7h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,6)

class PlayTest180_runof6intervening(unittest.TestCase):
    def test_playtest_runof6int(self):
        print("Play run of 6 broken with intervening card -----------------------------------------------------------")
        curcs = ['ac','2s','4h','3c','9d','5c']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('6h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,0)

class PlayTest190_runof7(unittest.TestCase):
    def test_playtest_runof7(self):
        print("Play run of 7 ----------------------------------------------------------------------------------------")
        curcs = ['ah','2c','3s','4s','5h','6d']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('7d')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,7)

class PlayTest200_runof7ooo(unittest.TestCase):
    def test_playtest_runof7ooo(self):
        print("Play run of 7 out of order ---------------------------------------------------------------------------")
        curcs = ['7c','6s','5c','4d','2c','3h']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('ah')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,7)

class PlayTest210_runof7intervening(unittest.TestCase):
    def test_playtest_runof7int(self):
        print("Play run of 7 broken with intervening card -----------------------------------------------------------")
        curcs = ['3c','2s','ac','4h','5d','6c','ad']
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('7h')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards + [newcard])
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]) + pyb.val(newcard))
        self.assertEqual(resscore,0)

class PlayTest900_overflow(unittest.TestCase):
    def test_playtest_overflow(self):
        print("Play overflow ----------------------------------------------------------------------------------------")
        curcs = ['5d','jh','3c','5h']           # cards already played
        curcards = [pyb.stringcard(x) for x in curcs]           # cards already played
        newcard = pyb.stringcard('qh')
        print("playing", pyb.cardstring(newcard), "on", [pyb.cardstring(x) for x in curcards])
        (resultcards, curtotal, resscore) = pyb.play_card(curcards, newcard)
        print('cards',[pyb.cardstring(x) for x in resultcards],'total',curtotal,'score',resscore)
        self.assertEqual(resultcards,curcards)
        self.assertEqual(curtotal,sum([pyb.val(x) for x in curcards]))
        self.assertEqual(resscore,-1)


if __name__ == '__main__':
    unittest.main()
