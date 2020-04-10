import sys

#print("I am pybbage!")

# lesser classes ----------------------------------------------------------------------------------------

# So I expect in arduino I can use a struct for this stuff. As of this writing (3/14/20) I'm out of it on
# codeine cough syrup - yay coronavirus panic and me being sick sick sick - so this may need a lot of ripping
# out and redux. Still, one's soul requires programming.
# Accordingly I've forgotten everything I knew about python classes so am consulting
# https://www.w3schools.com/python/python_classes.asp
# class Person:
#   def __init__(self, name, age):
#     self.name = name
#     self.age = age
#
# p1 = Person("John", 36)
#
# print(p1.name)
# print(p1.age)

# how about an object to represent a hand.
# it can have up to six cards in it
# I don't think it needs to know if it's a crib
# so: cards and parallel list of used flag
# flag might also have discarded for cards given to the crib
# so that they don't get restored e.g. between the play/countl and the scoring
# any reason not to just use a list and numcards kind of arrangement?
# fixed memory is helpful on tiny machines, just not pythonic
# This cards and flags thing seems super clumsy
# may resurrect for doing hypothetical hands, but currently just overthinking
# let's just try without it
# class Hand:
#     # constants for card flags
#     # Held means it is currently in hand and playable
#     # Discarded means given to crib (should it even still be in the hand?)
#     # in_play means it's not discarded but has been played in the play/count
#     HELD = 0
#     DISCARDED = 1
#     IN_PLAY = 2
#
#
#     # ctor
#     def __init__(self, cards = None, flags = None):
#         # I can imagine that we may need to spin up "hypothetical" hands directly without calling add_card
#         self.cards = cards
#         self.flags = flags
#         pass
#
#     # add_card assumes the card is legit (0..51, non-duplicate) and it's not in play or otherwise
#     # unusual (flag=0) though you can override the flag.
#     # returns the index of the new card
#     def add_card(self,card,flag=HELD):
#         if self.cards is None:
#             self.cards = []
#             self.flags = []
#         self.cards.append(card)
#         self.flags.append(flag)
#         return len(cards)-1
#
#     def get_card(self,i):
#         if self.cards is None or len(self.cards) <=i:
#             return None
#         return self.cards[i]
#
#     def get_flag(self,i):
#         if self.flags is None or len(self.flags) <=i:
#             return None
#         return self.flags[i]

# Default computer player --------------------------------------------------------------------------------------------
# K so I have a player object. What do we know about players?
# - what cards they hold and which are "used"
# - whether they're the dealer
# - their score
# parent pybbage
class Player:
    def __init__(self, parent, cards = [], used_cards = [], crib = [], dealer = False, score = 0, name = "Player"):
        self.parent = parent
        self.cards = cards
        self.used_cards = used_cards
        self.crib = crib
        self.dealer = dealer
        self.score = score
        self.name = name

    def set_score(self,points):
        self.score = points

    # add_score is a pegging - if the score goes past 120, force it to 121 (game hole) and return True.
    # otherwise return False.
    def add_score(self,points):
        self.score += points
        if self.score > 120:
            self.score = 121
            return True
        return False

    def get_score(self):
        return self.score

    def set_dealer(self,isdealer):
        self.dealer = isdealer;

    def is_dealer(self):
        return self.dealer

    def get_cards(self):
        return self.cards

    def set_cards(self,cards):
        self.cards = cards

    def add_card(self,card):
        self.cards.append(card)

    def add_crib(self,card):
        self.crib.append(card)

    def get_used_cards(self):
        return self.used_cards

    def set_used_cards(self,used_cards):
        self.used_cards = used_cards

    def get_crib(self):
        return self.crib

    def set_crib(self,crib):
        self.crib = crib

    def get_name(self):
        return self.name

    def set_name(self,name):
        self.name = name

    # =================================================================================================================
    # HERE ARE OVERRIDEABLE STRATEGY METHODS like playing a card in the play or shew
    # easy ones are using human input and choosing cards at random
    # might also have one for initial cut or subsequent cuts
    def cut(self,deck):
        # default: assume computer, and that deck is big enough to do this. Should be called right after a shuffle
        cutspot = self.parent.get_computer_input(4,len(deck)-4)
        print("*** cutting.... at",cutspot)
        return self.parent.cut(deck,cutspot)

    def discard(self,otherplayer):
        # here, choose two cards from self.hand and into the dealer's crib, either own if self.is_dealer
        # or otherplayer if not.
        # default implementation, just choose two at random. Can use deal to pull a card off.
        # or, just yank the card out.
        for j in range(0,2):
            cardind = self.parent.random_at_most(len(self.cards)-1)
            card = self.cards[cardind]              # split out the card
            self.cards = self.cards[:cardind] + self.cards[cardind + 1:]  # remove card from hand
            if self.is_dealer():
                self.add_crib(card)
            else:
                otherplayer.add_crib(card)

    # in the play, we get the stack of cards to date
    # choose a card and play it, if one is legal, returning the new stack of cards and the score for this round
    # (which also gets added on here.) can be 0. If -1, no legal play was available, and card stack unchanged,
    # which means "go"
    # card that gets played, if any, is appended to used_cards so hand can be restored for show.
    # THIS VERSION SHOULD STAY AS THE DEFAULT, OR AT LEAST BE AVAILABLE THROUGH A PlayFirstLegalPlayer
    # SUBCLASS, BC THAT WILL MAKE FOR EASY UNIT TESTING!!!!!!!
    def play(self,curcards):
        # choose a card for the play, if there is one that works
        # let's just go with the first one
        # def play_card(curcards, newcard):
        # return (newcards, curtotal, curscore)
        for i in range(0,len(self.cards)):
            card = self.cards[i]
            (newcards,curtotal,curscore) = self.parent.play_card(curcards,card)
            if curscore != -1:
                # play this one!
                print("playing",self.parent.cardstring(card),"on",[self.parent.cardstring(x) for x in curcards])
                self.cards = self.cards[:i] + self.cards[i + 1:]  # remove card from hand
                self.used_cards.append(card)        # memorize it so can be restored
                #self.score += curscore;
                return (newcards,curtotal,curscore)
                pass
        # if we get here, it's a go, I guess
        print("Go!")
        return (curcards,sum([self.parent.val(x) for x in curcards]),-1)

    # =================================================================================================================

    def print_hand(self):
        print("Hand:",[self.parent.cardstring(x) for x in self.cards],"used",
              [self.parent.cardstring(x) for x in self.used_cards])

    def print_crib(self):
        if self.is_dealer():
            print("Crib:", [self.parent.cardstring(x) for x in self.crib])
        else:
            print("Crib: (not dealer)")

    def print(self):
        print("Name:",self.name,"Dealer:",self.is_dealer(),"score:",self.score)
        self.print_hand()
        if self.is_dealer():
            self.print_crib()


# Default human player ------------------------------------------------------------------------------------------------
class HumanPlayer(Player):

    def __init__(self, parent, cards = [], used_cards = [], crib = [], dealer = False, score = 0, name = "Player"):
        super().__init__(parent, cards, used_cards, crib, dealer, score, name)

    # TEMP just do random cut like computer
    # TODO restore this later but cuts are annoying
    # def cut(self,deck):
    #     # humqn version!
    #     print("*** enter cut!")
    #     return cut(deck,get_input(4,len(deck)-4))


    def discard(self, otherplayer):
        # here, choose two cards from self.hand and into the dealer's crib, either own if self.is_dealer
        # or otherplayer if not.
        # default implementation, let user input
        # or, just yank the card out.
        for j in range(0, 2):
            print("Cards:")
            for k in range(0,len(self.cards)):
                print("{}) {}".format(k,self.parent.cardstring(self.cards[k])))
            print("Enter a card to discard")
            cardind = self.parent.get_input(0,len(self.cards) - 1)
            card = self.cards[cardind]  # split out the card
            self.cards = self.cards[:cardind] + self.cards[cardind + 1:]  # remove card from hand
            if self.is_dealer():
                self.add_crib(card)
            else:
                otherplayer.add_crib(card)

    # in the play, we get the stack of cards to date
    # choose a card and play it, if one is legal, returning the new stack of cards and the score for this round
    # (which also gets added on here.) can be 0. If -1, no legal play was available, and card stack unchanged,
    # which means "go"
    # card that gets played, if any, is appended to used_cards so hand can be restored for show.
    # THIS VERSION SHOULD STAY AS THE DEFAULT, OR AT LEAST BE AVAILABLE THROUGH A PlayFirstLegalPlayer
    # SUBCLASS, BC THAT WILL MAKE FOR EASY UNIT TESTING!!!!!!!
    def play(self,curcards):
        # choose a card for the play, if there is one that works
        # so scan through and make sure there is a legal play. If not,
        legalcards = []
        for i in range(0,len(self.cards)):
            card = self.cards[i]
            (newcards,curtotal,curscore) = self.parent.play_card(curcards,card)
            if curscore != -1:
                legalcards.append(card)
        if legalcards == []:
            print("No legal card to play! you say go")
            return (curcards,sum([self.parent.val(x) for x in curcards]),-1)

        # limit choices to legal cards
        print("Legal Cards:")
        for k in range(0, len(legalcards)):
            print("{}) {}".format(k, self.parent.cardstring(legalcards[k])))
        print("Enter a card to play:")
        cardind = self.parent.get_input(0,len(legalcards) - 1)
        card = legalcards[cardind]  # split out the card
        self.cards = self.cards[:cardind] + self.cards[cardind + 1:]  # remove card from hand
        self.used_cards.append(card)  # memorize it so can be restored
        (newcards, curtotal, curscore) = self.parent.play_card(curcards, card)
        return (newcards,curtotal,curscore)

# Player for Unit Testing that plays the first card in their hand that is legal.
class PlayFirstLegalCardPlayer(Player):
    def __init__(self, parent, cards = [], used_cards = [], crib = [], dealer = False, score = 0, name = "Player"):
        super().__init__(parent, cards, used_cards, crib, dealer, score, name)

    def play(self,curcards):
        # choose a card for the play, if there is one that works
        # let's just go with the first one
        # def play_card(curcards, newcard):
        # return (newcards, curtotal, curscore)
        for i in range(0,len(self.cards)):
            card = self.cards[i]
            (newcards,curtotal,curscore) = self.parent.play_card(curcards,card)
            if curscore != -1:
                # play this one!
                print("playing",self.parent.cardstring(card),"on",[self.parent.cardstring(x) for x in curcards])
                self.cards = self.cards[:i] + self.cards[i + 1:]  # remove card from hand
                self.used_cards.append(card)        # memorize it so can be restored
                self.score += curscore;
                return (newcards,curtotal,curscore)
                pass
        # if we get here, it's a go, I guess
        print("Go!")
        return (curcards,sum([self.parent.val(x) for x in curcards]),-1)


# random number generator a la arduino -----------------------------------------------------------

# so for random, let's reproduce arduino's, which is taken from avrlibc's, as shewn here
# https://arduino.stackexchange.com/questions/1481/formula-calculation-of-the-function-random-randomseed

# see random.c for the original code - including license here bc that seems appropriate

# /*-
#  * Copyright (c) 1990, 1993
#  *	The Regents of the University of California.  All rights reserved.
#  *
#  * Redistribution and use in source and binary forms, with or without
#  * modification, are permitted provided that the following conditions
#  * are met:
#  * 1. Redistributions of source code must retain the above copyright
#  *    notice, this list of conditions and the following disclaimer.
#  * 2. Redistributions in binary form must reproduce the above copyright
#  *    notice, this list of conditions and the following disclaimer in the
#  *    documentation and/or other materials provided with the distribution.
#  * 3. Neither the name of the University nor the names of its contributors
#  *    may be used to endorse or promote products derived from this software
#  *    without specific prior written permission.
#  *
#  * THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
#  * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  * ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
#  * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
#  * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#  * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
#  * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#  * SUCH DAMAGE.
#  *
#  * Posix rand_r function added May 1999 by Wes Peters <wes@softweyr.com>.
#  *
#  * $Id: random.c 1944 2009-04-01 23:12:20Z arcanum $
#  */
#
# /*
#  * From:
# static char sccsid[] = "@(#)rand.c	8.1 (Berkeley) 6/14/93";
# */

# icky global "next" for random
from typing import List, Any

class Pybbage:

    def __init__(self):
        self.rand_next = 1
        self.random_max = 0x7FFFFFFF

        # global score list
        self.SCORE_NOBS = 0          #  0. nobs - 1
        self.SCORE_GO = 1            #  1. go - 1
        self.SCORE_FIFTEEN = 2       #  2. fifteen - 2
        self.SCORE_THIRTYONE = 3     #  3. thirty-one - 2
        self.SCORE_PAIR = 4          #  4. pair - 2
        self.SCORE_HEELS = 5         #  5. heels - 2
        self.SCORE_RUN3 = 6          #  6. run of 3 - 3
        self.SCORE_RUN4 = 7          #  7. run of 4 - 4
        self.SCORE_TWOPAIR = 8       #  8. two pair - 4
        self.SCORE_FLUSH = 9         #  9. flush - 4
        self.SCORE_RUN5 = 10         # 10. run of 5 - 5
        self.SCORE_FLUSH5 = 11       # 11. 5 card flush - 5
        self.SCORE_RUN6 = 12         # 12. run of 6 - 6
        self.SCORE_PAIRROYAL = 13    # 13. pair royal - 6
        self.SCORE_RUN7 = 14         # 14. run of 7 - 7
        self.SCORE_DBLRUN3 = 15      # 15. double run of 3 - 8
        self.SCORE_DBLRUN4 = 16      # 16. double run of 4 - 10
        self.SCORE_4KIND = 17        # 17. 4 of a kind
        self.SCORE_TRIPLERUN = 18    # 17. triple run - 15
        self.SCORE_DBLDBLRUN = 19    # 18. double double run - 16

        # name and score for each of these
        self.scoreStringsNPoints = [
            ("nobs",1),                 # SCORE_NOBS = 0
            ("go",1),                   # SCORE_GO = 1
            ("fifteen",2),              # SCORE_FIFTEEN = 2
            ("thirty-one",2),           # SCORE_THIRTYONE = 3
            ("pair",2),                 # SCORE_PAIR = 4
            ("heels",2),                # SCORE_HEELS = 5
            ("run of 3",3),             # SCORE_RUN3 = 6
            ("run of 4",4),             # SCORE_RUN4 = 7
            ("two pair",4),             # SCORE_TWOPAIR = 8
            ("flush",4),                # SCORE_FLUSH = 9
            ("run of 5",5),             # SCORE_RUN5 = 10
            ("5 card flush",5),         # SCORE_FLUSH5 = 11
            ("run of 6",6),             # SCORE_RUN6 = 12
            ("pair royal",6),           # SCORE_PAIRROYAL = 13
            ("run of 7",7),             # SCORE_RUN7 = 14
            ("double run of 3",8),      # SCORE_DBLRUN3 = 15
            ("double run of 4",10),     # SCORE_DBLRUN4 = 16
            ("4 of a kind",12),         # SCORE_4KIND = 17
            ("triple run",15),          # SCORE_TRIPLERUN = 18
            ("double double run",16)    # SCORE_DBLDBLRUN = 19
        ]


    def do_random(self,ctx):
        x = ctx
        # Can't be initialized with 0, so use another value.
        if (x == 0):
            x = 123459876
        hi = x // 127773       # // should be integer divide
        lo = x % 127773
        x = 16807 * lo - 2836 * hi
        if (x < 0):
            x += 0x7fffffff
        self.rand_next = x
        return x % (self.random_max + 1)


    def random(self):
        return self.do_random(self.rand_next)

    def srandom(self,seed):
        self.rand_next = seed;


    # card handling routines -------------------------------------------------------------------------

    def rank(self,card):
        return card // 4

    def val(self,card):
        '''value, s.t. ace = 1, 2 = 2, ... 10 and face cards = 10'''
        return self.rank(card)+1 if self.rank(card) < 10 else 10

    def suit(self,card):
        return card % 4


    def cardstring(self,card):
        '''card is a number from 0-51; card %4 is rank, where 0 = hearts, 1 = diamonds, 2 = clubs, 3 = spades.
        card // 4 is rank, 0 = ace .. 12 = king
        '''
        if card not in range(0,52):
            print("Illegal card value",card)
            return None
        return 'A234567890JQK'[self.rank(card)] + '♥♦♣♠'[self.suit(card)]

    # this is mostly for debugging and unit testing
    def stringcard(self,strc):
        '''strc is a 2 character code for a card. first character = rank, A234567890JQK, 2nd = suit, hdcs for heart diamond
        club spade, case-insensitive, can also be ♥♦♣♠ '''
        if strc is None:
            return None
        ranks = 'A234567890JQK'
        suits = 'HDCS'
        suits2 = '♥♦♣♠'
        if len(strc) != 2:
            print("ERROR: stringcard input must be 2 characters")
            return None

        stru = str.upper(strc)
        if stru[0] not in ranks:
            print("ERROR: rank",stru[0],"is not a legal rank from",ranks)
            return None
        if stru[1] not in suits and stru[1] not in suits2:
            print("ERROR: suit",stru[1],"is not a legal suit from",suits,"or",suits2)
            return None

        return (ranks.index(stru[0]) * 4) + (suits.index(stru[1]) if stru[1] in suits else suits2.index(stru[1]))



    # shuffle returns a data structure containing parallel lists of card value (rank/suit combo 0..51) and flag
    # for whether it's been dealt.
    # this representation lets you walk through the deck sequentially (deal) but also fish cards out random-access (cut).
    # only... that's not really what cut is, is it? it takes a position in the deck and swaps the 'halves' of the deck!
    # that being the case, do we need the dealt-flag? the cribbage cut and turn is just swap halves, then deal a card.
    # shuffle implemented by generating 52 32-bit random numbers and scanning it to determine their order.
    # the LOL here is that this takes 208 bytes and I couldn't use it for vpok bc that's more RAM than a PIC 16F628 has.
    # on ardy it can be discarded once the ordering is redone.
    # Uno R3 / atmega328 has 2K ram, yes? Some taken by the arduino core but not lots
    def shuffle(self):
        newdeck = {'order':[self.random() for i in range(0,52)],
                'value':[-1 for i in range(0,52)]}
        curmin = min(newdeck['order'])
        # the arduino version will look quite different, searching instead of listbuilding
        for val in range(0,52):
            card = newdeck['order'].index(curmin)
            newdeck['value'][card] = val
            gtmin = list(filter(lambda x:x>curmin,newdeck['order']))
            if len(gtmin) > 0:
                curmin = min(gtmin)
        return newdeck['value']

    # COULD ALSO TRY THE SHUFFLE WAY WHERE YOU JUST PICK TWO CARDS TO SWAP AND DO THAT A BUNCH OF TIMES.
    # THAT'S MORE THE TINY861 VERSION - how many times is enough, etc.
    # worry re later

    # deck is just an array now
    # let's just have the deck be an array and pull cards off of its front
    def deal_card(self,deck):
        if deck is not None and len(deck) > 0:
            card = deck[0]
            deck = deck[1:]
            return (deck,card)
        return (None,None)

    # Cut will take an index into a deck which is assumed not to have any cards removed from it, plus an index.
    # then it swaps the halves. returns the cut deck.
    # weirdness is that cut (deck,0) returns deck unchanged. so, disallow 0?
    # ektully from sec 3.1 of the rules,
    # When cutting for the first deal of a game, the
    # first player shall remove no less than four cards
    # and not more than half the pack. The second
    # player shall remove no less than four cards and
    # shall leave at least four cards.
    # c. When cutting before each deal and for the starter
    # card, no less than four cards shall be taken from
    # the top and no less than four left on the bottom.
    # This will be enforced by the calls to the random number gettors below.
    def cut(self,deck,index):
        if index >= 1 and index < len(deck):
            return deck[index:] + deck[:index]
        print("Illegal cut index",index,"- not doing cut")
        return deck;


    # SCORING -------------------------------------------------------------------------------------------------------------

    # let's just try scoring a show, damn the data structures for now
    # where hand is a list of 0..51, starter is the up-card 0..51
    # assumed to be correct i.e. no duplicates or illegal values
    # returns (total score for hand, [scoring subsets])
    # where a scoring subset is [[indices of participating cards],score constant]
    # where indices of participating cards are 0..3 for cards in hand, 4 = starter
    # and score constant is from the global score list above, e.g. SCORE_NOBS
    # through SCORE_DBLDBLRUN - which is an index into scoreStringsNPoints that
    # stores the name of the scoring subset e.g. "nobs" and the number of points it's worth.

    def score_shew(self,hand,starter):
        curscore = 0
        score_subsets = []

        # for convenience
        cards = hand + [starter]

        # look for fifteens ===============================================================================================
        # what is the power set of cards? I suppose we need to check
        # all two-card sums (of which there are 5 choose 2 = 10)
        for i in range(0,4):
            for j in range(i+1,5):
                if self.val(cards[i]) + self.val(cards[j]) == 15:
                    curscore += 2
                    score_subsets.append([[i,j],self.SCORE_FIFTEEN])
                    #print(cardstring(cards[i]),cardstring(cards[j]),"... 15 -",curscore)
        # all three-card sums (of which there are 5 choose 3 = 10, which = inverse of 5 choose 2, I guess)
        for i in range(0,3):
            for j in range(i+1,4):
                for k in range(j+1,5):
                    if self.val(cards[i]) + self.val(cards[j]) + self.val(cards[k]) == 15:
                        curscore += 2
                        score_subsets.append([[i, j, k], self.SCORE_FIFTEEN])
                        #print(cardstring(cards[i]), cardstring(cards[j]), cardstring(cards[k]), "... 15 -", curscore)
        # all four-card sums (of which there are 5 choose 4 = 5)
        for i in range(0,5):
            subcards = [x for x in cards]           # need to make a new copy...??? yup
            #print("About to remove",cards[i],"from",subcards)
            subcards.remove(cards[i])
            if sum([self.val(x) for x in subcards]) == 15:
                curscore += 2
                #for cs in [cardstring(x) for x in subcards]:
                #    print(cs,end=' ')
                #print("... 15 -",curscore)
                partcards = list(range(5))
                partcards.remove(i)
                score_subsets.append([partcards, self.SCORE_FIFTEEN])

        # all 5 cards' sum (1 sum)
        if sum([self.val(x) for x in cards]) == 15:
            curscore += 2
            #for cs in [cardstring(x) for x in cards]:
            #    print(cs, end=' ')
            #print("... 15 -", curscore)
            score_subsets.append([list(range(5)), self.SCORE_FIFTEEN])

        # look for big stuff like double double runs ======================================================================

        # runs ============================================================================================================
        # rules do not explicitly forbid ace-high straight but do not ever show one, so let's say there is none
        # most popular answer at https://boardgames.stackexchange.com/questions/8060/is-ace-high-or-low-or-both
        # says the same.
        # so if we sort cards...
        # we need to do this a) on arduino b) in the play/count
        # so, a set of n cards whose ranks span n-1 and which have no pairs is a run, yes?
        # this needs a fizzbuzz thing, I suppose, that you check for 5 card run, and if there is one,
        # disqualify any cards in it from participating in any smaller runs?
        # maybe some examples
        # I like the idea of pattern-rec the kinds of runs
        # though for pure scoring purps there's no real reason... unless maybe it's an unrolled loop that's faster
        #
        # so from the rules:
        # straight (or run), single
        #
        # Sequence of three or more consecutive cards in any order during the play of the cards; for example, 3-5-6-7-4
        # (counts three when the 7 is played and counts five when the 4 is played).
        #
        # straight, multiple (used only in counting hands and crib):
        #
        # • Double run: two three-card or four-card straights, including one pair; for example, A-2-3-3 or A-2-3-3-4.
        # • Double-double run: four three-card straights, including two pairs; for example, 8-8-9-9-10.
        # • Triple run: three three-card straights, including three of a kind; for example, J-Q-Q-Q-K.
        #
        # what are all the patterns, assuming cards sorted? Going from 5-card on down, fizzbuzz style
        #
        # 6 pairs disqualifies any runs.
        #
        # run of 5, sorted then normalized ranks, 0 pairs
        # 0 1 2 3 4
        #
        # triple run: sorted then normalized ranks, 3 pairs
        # 0 0 0 1 2
        # 0 1 1 1 2
        # 0 1 2 2 2
        #
        # double double run: sorted then normalized ranks, 2 pairs
        # 0 0 1 1 2
        # 0 0 1 2 2
        # 0 1 1 2 2
        #
        # double run of 4, sorted then normalized ranks, 1 pair
        # 0 0 1 2 3
        # 0 1 1 2 3
        # 0 1 2 2 3
        # 0 1 2 3 3
        #
        # That's it for 5-card cases; if any match, don't look for pairs or runs separately?
        # OR IS IT BETTER TO TRY TO COMPOSE THIS FROM ELEMENTS?
        # ---
        # then the smaller stuff:
        # double run of 3, where c-a = 2 and x is outlier, 1 pair
        # A A B C X
        # A B B C X
        # A B C C X
        # X A A B C
        # X A B B C
        # X A B C C
        # how to express this in sortnorm? 0 0 1 2 X is easy enough, just say anything > 2 = x
        # consider it 2 sets of cases yielding sortnorm2: first, do the >2 is x, use 4 for x, and look for
        # 0 0 1 2 4
        # 0 1 1 2 4
        # 0 1 2 2 4
        # then other sortnorm2 where you normalize against the second highest value in the bunch? then <0 = x, say x= 4
        # 4 0 0 1 2
        # 4 0 1 1 2
        # 4 0 1 2 2
        # not super happy with this but ... hm.
        # ok, so for the first cases, if the first 4 are 0 0 1 2 / 0 1 1 2 / 0 1 2 2 and haven't matched as a double run
        # of 4 or any of the earlier stuff, call a double run of 3
        # That works, but what about the other cases? there I guess try the subbing off 2nd-min thing, hm.
        #
        # once all the double-run cases are accounted for, can score in terms of single runs and pairs and stuff?
        # is there anything else that isn't scored purely as pairs/runs? I think we'd be ok after that.
        # runs of 3 can spot by checking all sets of 3 cards for spread of 2, no pairs,
        # runs of 4 similar. Need to make sure runs of 3 don't participate in a run of 4.
        # if there is a run of 4, can there be runs of 3? I don't think so. Only 1 card doesn't participate

        # start with sorting the cards, so as to preserve order all throughout
        # to reckon participating cards, we need to build a parallel list of the
        # original indices of the cards. That is sortinds.
        # this is all slow and gross, arduino rewrite will need to be more elegant
        sortcards = sorted(cards)
        sortinds = [cards.index(x) for x in sortcards]
        sortranks = [self.rank(x) for x in sortcards]
        normsranks = [x - min(sortranks) for x in sortranks]
        #print("sortcards =",[cardstring(x) for x in sortcards],"sortranks =",sortranks,"normsranks =",normsranks)

        # 5-card scores: sequence, name, points. VERIFY SCORING
        # 5-carders preclude any other scores for runs or pairs. 15s, flushes, nobs still ok.
        fivecarders = [
            [[0, 1, 2, 3, 4], self.SCORE_RUN5], #"run of 5", 5],           #  5 = 5*1 per card
            [[0, 0, 0, 1, 2], self.SCORE_TRIPLERUN], #"triple run", 15],        # 15 = 3*3 runs + 3*2 pairs
            [[0, 1, 1, 1, 2], self.SCORE_TRIPLERUN], #"triple run", 15],
            [[0, 1, 2, 2, 2], self.SCORE_TRIPLERUN], #"triple run", 15],
            [[0, 0, 1, 1, 2], self.SCORE_DBLDBLRUN], #"double double run", 16], # 16 = 4*3 runs + 2*2 pairs
            [[0, 0, 1, 2, 2], self.SCORE_DBLDBLRUN], #"double double run", 16],
            [[0, 1, 1, 2, 2], self.SCORE_DBLDBLRUN], #"double double run", 16],
            [[0, 0, 1, 2, 3], self.SCORE_DBLRUN4], #"double run of 4", 10],   # 10 = 2*4 runs + 1*2 pairs
            [[0, 1, 1, 2, 3], self.SCORE_DBLRUN4], #"double run of 4", 10],
            [[0, 1, 2, 2, 3], self.SCORE_DBLRUN4], #"double run of 4", 10],
            [[0, 1, 2, 3, 3], self.SCORE_DBLRUN4]] #"double run of 4", 10]]

        found_fivecarder = 0            # flag: if any five-carders found, don't use pairs
        found_fourcarders = 0
        for fivey in fivecarders:
            if normsranks == fivey[0]:
                found_fivecarder = 1
                curscore += self.scoreStringsNPoints[fivey[1]][1]
                #for cs in [cardstring(x) for x in cards]:
                #    print(cs,end=' ')
                #print("...", fivey[1],"-",curscore)
                score_subsets.append([list(range(5)), fivey[1]])
                break


        if found_fivecarder == 0:
            # runs! first look for 4s - if there are any, can't be any 3s, yes?
            # so try the first 4 and last 4 among the normsranks, yes?
            if normsranks[:4] == [0,1,2,3]:
                found_fourcarders = 1
                curscore += 4
                #for i in range(0,4):
                #    print(cardstring(sortcards[i]),end=' ')
                #print("... run of 4 -",curscore)
                # so, sortinds[:4] should be the participating cards, yes?
                score_subsets.append([sortinds[:4],self.SCORE_RUN4])
            elif normsranks[:4] == [0,0,1,2] or normsranks[:4] == [0,1,1,2] or normsranks[:4] == [0,1,2,2]:
                found_fourcarders = 1
                curscore += 8           # 2*3 + pr
                #for i in range(0,4):
                #    print(cardstring(sortcards[i]),end=' ')
                #print("... double run -",curscore)
                score_subsets.append([sortinds[:4],self.SCORE_DBLRUN3])
            else:
                nranks2 = [x - min(normsranks[1:]) for x in normsranks[1:]]
                #print("normsranks =",normsranks,"nranks2 =",nranks2)
                if nranks2 == [0,1,2,3]:
                    found_fourcarders = 2
                    curscore += 4
                    #for i in range(1, 5):
                    #    print(cardstring(sortcards[i]), end=' ')
                    #print("... run of 4 -", curscore)
                    # so, sortinds[1:] should be the participating cards, yes?
                    score_subsets.append([sortinds[1:], self.SCORE_RUN4])
                elif nranks2 == [0, 0, 1, 2] or nranks2 == [0, 1, 1, 2] or nranks2 == [0, 1, 2, 2]:
                    found_fourcarders = 2
                    curscore += 8  # 2*3 + pr
                    #for i in range(1, 5):
                    #    print(cardstring(sortcards[i]), end=' ')
                    #print("... double run -", curscore)
                    score_subsets.append([sortinds[1:], self.SCORE_DBLRUN3])

        # Count pairs if no higher-order hand precludes
        if found_fivecarder == 0 and found_fourcarders == 0:
            pairranks = []
            numpairs = 0
            for i in range(0,4):
                for j in range(i+1,5):
                    if self.rank(cards[i]) == self.rank(cards[j]):
                        numpairs +=1
                        if self.rank(cards[i]) not in pairranks:
                            pairranks.append(self.rank(cards[i]))
            curscore += 2 * numpairs
            # if there were pairs, emit participating cards
            # prpartcards will be a list of lists
            # each inner list i is the card indices whose rank is pairranks[i]
            prpartcards = []
            for ranky in pairranks:
                partcards = []
                for i in range(0,5):
                    if self.rank(cards[i]) == ranky:
                        partcards.append(i)
                        #print(self.cardstring(cards[i]),end=' ')
                prpartcards.append(partcards)

            # then for every case except 2 and 4, there is only one pair rank so just
            # use prpartcards[0] as the participating card list.
            if numpairs > 0:
                if numpairs == 1:
                    #print("... pair",end=' ')
                    score_subsets.append([prpartcards[0], self.SCORE_PAIR])
                elif numpairs == 2:
                    #print("... two pair",end=' ')
                    # really just two pairs. Is score_twopair a thing?
                    # yeah, let's do this:
                    score_subsets.append([prpartcards[0]+prpartcards[1], self.SCORE_TWOPAIR])
                elif numpairs == 3:
                    #print("... 3 of a kind",end=' ')
                    score_subsets.append([prpartcards[0], self.SCORE_PAIRROYAL])
                elif numpairs == 4:
                    # this is kind of gross but w/e
                    # just add two entries to the score list a 3 of a kind and a pair
                    #print("... 3 of a kind and pair",end=' ')
                    if(len(prpartcards[0])==2):
                        score_subsets.append([prpartcards[0], self.SCORE_PAIR])
                        score_subsets.append([prpartcards[1], self.SCORE_PAIRROYAL])
                    else:
                        score_subsets.append([prpartcards[1], self.SCORE_PAIR])
                        score_subsets.append([prpartcards[0], self.SCORE_PAIRROYAL])
                elif numpairs == 6:
                    #print("... 4 of a kind",end=' ')
                    score_subsets.append([prpartcards[0], self.SCORE_4KIND])
                #print("-",curscore)
                #print("Found",numpairs,"pairs")  # debug do we need?

            # so if found_fourcarders = 1, the first 4 were a run, so the last card can be in other scores?
            # if it's 2, the last 4 were, so first card can be in other scores? Does it matter?
            # TODO VERIFY THAT
            if found_fourcarders == 0:
                # nicked from the fifteens:
                for i in range(0, 3):
                    for j in range(i + 1, 4):
                        for k in range(j + 1, 5):
                            # how do we look for a run? get the sorted of the 3 cards' ranks.
                            nsrnks = sorted([self.rank(cards[i]),self.rank(cards[j]),self.rank(cards[k])])
                            nsrnks = [x-min(nsrnks) for x in nsrnks]
                            if nsrnks == [0,1,2]:
                                curscore += 3
                                #print(cardstring(cards[i]),cardstring(cards[j]),cardstring(cards[k]),"... run of 3 -",
                                #      curscore)
                                score_subsets.append([[i,j,k], self.SCORE_RUN3])

        # flushes =========================================================================================================
        # not quite clear on this - from the rules
        # Four cards of the same suit held in the
        # hand count four points; five cards of the
        # same suit (including the starter card)
        # count five points in the hand or crib.
        # I think that means if the non-starters are all the same suit, it's 4, and the starter only counts
        # as the 5th
        if self.suit(hand[0]) == self.suit(hand[1]) and self.suit(hand[1]) == self.suit(hand[2]) and \
                self.suit(hand[2]) == self.suit(hand[3]):
            if self.suit(hand[3]) == self.suit(starter):
                curscore += 5
                #for cs in [cardstring(x) for x in cards]:
                #    print(cs,end=' ')
                #print("... 5 card flush -",curscore)
                score_subsets.append([list(range(5)),self.SCORE_FLUSH5])
            else:
                curscore += 4
                #for cs in [cardstring(x) for x in hand]:
                #    print(cs,end=' ')
                #print("... 4 card flush -",curscore)
                score_subsets.append([list(range(4)),self.SCORE_FLUSH])

        # and finally, nobs ===============================================================================================
        for i in range(0,4):
           if self.rank(hand[i]) == 10 and self.suit(hand[i]) == self.suit(starter):
                curscore += 1
                #print(cardstring(hand[i]), cardstring(starter),"... nobs -", curscore)
                score_subsets.append([[i],self.SCORE_NOBS])
                break

        # finally, at long last, return score - but if it's 0, say nineteen bc that's all clever
        #if curscore == 0:
        #    for cs in [cardstring(x) for x in cards]:
        #        print(cs,end=' ')
        #    print("... NINETEEN!")

        return (curscore,score_subsets)

    # render_score_subsets prints a list of score subsets produced by score_shew
    # from the same hand and starter. Purely cosmetic, and in graphical versions
    # will instead highlight the cards and do some song and dance with the values
    # or some such.
    def render_score_subsets(self,hand,starter,subsets):
        # card indices in a score subset are 0..3 for those in hand, 4 for starter
        cards = hand + [starter]

        curscore = 0
        for subset in subsets:
            (partcards,scoreindex) = subset
            # accumulate points
            curscore += self.scoreStringsNPoints[scoreindex][1]
            for i in partcards:
                print(self.cardstring(cards[i]),end=' ')
            print("...",self.scoreStringsNPoints[scoreindex][0],"-",curscore)



    # SCORING THE PLAY / COUNT ============================================================================================
    # given: the cards that have been played so far, list of 0..51
    # and card to be played
    # return: (cards now played = cards so far + played, running total, score for playing the given card or -1 for error)
    # not a serious error, I expect this to be a "lookahead" function for deciding what card to play for the computer
    def play_card(self,curcards, newcard):
        newcards = curcards if curcards is not None else []
        curscore = 0

        newcards = newcards + [newcard]
        curtotal = sum([self.val(x) for x in newcards])

        # figure out if newcard CAN be played on newcards, yes?
        # - can't go over 31 - is that the only limitation? I suppose so
        if curtotal > 31:
            return(curcards,curtotal-self.val(newcard),-1)         # error

        #print("-- running total",curtotal)

        # otherwise we should be ok.
        # if total is now 15, 2 points!
        if curtotal == 15:
            curscore += 2
            print("... fifteen -",curscore)
        # if total is now 31, 2 points
        elif curtotal == 31:
            curscore += 2
            print("... thirty-one -", curscore)

        # what else? Pair, if same rank as the last card - and can be 3, 4 of a kind?
        # and runs
        # "go" for 1 point will have to be handled outside this, I guess, player must recognize they can't play
        # and allow the other player to.
        # - weird case there, they can keep playing until they can't place any more cards

        # I'm going to say pairs and runs can't be interrupted, though runs don't have to be in order.
        # that is, playing a 5, then a 7, then a 5, the second 5 doesn't make a pair.
        # so - start noodling.
        # pairs:
        numrankmatch = 0
        currank = self.rank(newcard)
        # pairs are easy bc you can only go up to 4 of a kind. loopify this when I see a pattern
        # or leave it like it is if I want to
        # ifs are nested bc if there is a discontinuity, the chain breaks.
        if len(curcards) >=1 and self.rank(curcards[-1]) == currank:
            numrankmatch += 1
            if len(curcards) >=2 and self.rank(curcards[-2]) == currank:
                numrankmatch += 1
                if len(curcards) >=3 and self.rank(curcards[-3]) == currank:
                    numrankmatch += 1
        # so, numrankmatch + 1 is the number of matching cards, not including the played card.
        if numrankmatch == 1:
            curscore += 2
            print("... pair -",curscore)
        elif numrankmatch == 2:
            curscore += 6
            print("... three of a kind -",curscore)
        elif numrankmatch == 3:
            curscore += 12
            print("... four of a kind -",curscore)

        # FIGURE OUT RUNS
        # this works:
        # >>> h = [5, 3, 7, 4, 6]
        # >>> for i in range(-1, -(len(h)+1), -1):
        # ...     print([x-min(h[i:]) for x in sorted(h[i:])])
        # ...
        # [0]
        # [0, 2]
        # [0, 2, 3]
        # [0, 1, 3, 4]
        # [0, 1, 2, 3, 4]
        # that looks like a way to spot runs
        # like pairs, go until you find a run...? an intervening non-run does not disqualify.
        # what is the longest possible? The whole length of newcards, I suppose.
        # look at them all, and pick the highest run, if any.
        # >>> for i in range(-1, -(len(h)+1), -1):
        # ...     ns = [x-min(h[i:]) for x in sorted(h[i:])]
        # ...     if ns == list(range(0,-i)):
        # ...         print(ns," = RUN!!!!!!!!! of",-i)
        # ...     else:
        # ...         print(ns," = not run :(")
        # ...
        # [0]  = RUN!!!!!!!!! of 1
        # [0, 2]  = not run :(
        # [0, 2, 3]  = not run :(
        # [0, 1, 3, 4]  = not run :(
        # [0, 1, 2, 3, 4]  = RUN!!!!!!!!! of 5
        # so there you have it. just start at -3 bc no shorter run matters
        # ALSO: need to get rank of card, not just card
        longestrun = 0
        for i in range(-3, -(len(newcards)+1), -1):
            sorty = [self.rank(x) for x in sorted(newcards[i:])]
            ns = [x-min(sorty) for x in sorty]
            if ns == list(range(0,-i)):
                longestrun = -i

        if longestrun != 0:
            curscore += longestrun
            print(" ... run of",longestrun,"-",curscore)


        return(newcards,curtotal,curscore)


    # input ===============================================================================================================

    # get_input gets numeric input from min (inclusive) to max (inclusive)
    # for choosing cut, discard, play6

    def get_input(self,inmin,inmax,inexclude=None):
        got_legit = False
        while not got_legit:
            try:
                if inexclude is None:
                    prompt = "input a number from {} to {} --> ".format(inmin,inmax)
                    num = int(input(prompt))
                    if num >= inmin and num <= inmax:
                        got_legit = True
                    else:
                        print("out of range!")
                else:
                    prompt = "input a number from {} to {} except {} --> ".format(inmin,inmax,sorted(inexclude))
                    num = int(input(prompt))
                    if num >= inmin and num <= inmax and num not in inexclude:
                        got_legit = True
                    else:
                        print("out of range or one of the exceptions!")
            except ValueError as e:
                print("Please enter a number.")
        return num


    # support routine for the computer version of get_input - need to get this right
    # ok, so random() gets us a 32 bit number
    # how to spread that out evenly over the possibilities?
    # modulo isn't - what do we get if we do num // ((inmax-inmin) + 1)
    # then add inmin, should be a number from inmin...inmax, yes?
    # this might be it. from @Ryan Reich:
    # https://stackoverflow.com/questions/2509679/how-to-generate-a-random-integer-number-from-within-a-range
    # which has this commentary and C code:
    # All the answers so far are mathematically wrong. Returning rand() % N does not uniformly give a number in the
    # range [0, N) unless N divides the length of the interval into which rand() returns (i.e. is a power of 2).
    # Furthermore, one has no idea whether the moduli of rand() are independent: it's possible that they go
    # 0, 1, 2, ..., which is uniform but not very random. The only assumption it seems reasonable to make is that
    # rand() puts out a Poisson distribution: any two nonoverlapping subintervals of the same size are equally likely
    # and independent. For a finite set of values, this implies a uniform distribution and also ensures that the values
    # of rand() are nicely scattered.
    #
    # This means that the only correct way of changing the range of rand() is to divide it into boxes; for example, if
    # RAND_MAX == 11 and you want a range of 1..6, you should assign {0,1} to 1, {2,3} to 2, and so on. These are
    # disjoint, equally-sized intervals and thus are uniformly and independently distributed.
    #
    # The suggestion to use floating-point division is mathematically plausible but suffers from rounding issues in
    # principle. Perhaps double is high-enough precision to make it work; perhaps not. I don't know and I don't want
    # to have to figure it out; in any case, the answer is system-dependent.
    #
    # The correct way is to use integer arithmetic. That is, you want something like the following:
    # ---
    # #include <stdlib.h> // For random(), RAND_MAX
    #
    # // Assumes 0 <= max <= RAND_MAX
    # // Returns in the closed interval [0, max]
    # long random_at_most(long max) {
    #   unsigned long
    #     // max <= RAND_MAX < ULONG_MAX, so this is okay.
    #     num_bins = (unsigned long) max + 1,
    #     num_rand = (unsigned long) RAND_MAX + 1,
    #     bin_size = num_rand / num_bins,
    #     defect   = num_rand % num_bins;
    #
    #   long x;
    #   do {
    #    x = random();
    #   }
    #   // This is carefully written not to overflow
    #   while (num_rand - defect <= (unsigned long)x);
    #
    #   // Truncated division is intentional
    #   return x/bin_size;
    # }
    # ---
    # The loop is necessary to get a perfectly uniform distribution. For example, if you are given random numbers from
    # 0 to 2 and you want only ones from 0 to 1, you just keep pulling until you don't get a 2; it's not hard to check
    # that this gives 0 or 1 with equal probability. This method is also described in the link that nos gave in their
    # answer, though coded differently. I'm using random() rather than rand() as it has a better distribution (as
    # noted by the man page for rand()).
    #
    # THERE ARE OTHER VERSIONS TOO BUT THIS ONE IS HIGHEST VOTED
    # I wonder if my old vpok 0..51 thing was similar


    # Assumes 0 <= max <= random_max
    # Returns in the closed interval [0, max]
    # OK, going to need a comparison test for this.
    # and done, c and python agreed on a million random_at_most(52) then a million random_at_most(6).
    # TODO maybe make the c version used by the python script - learn how to write py libs in c
    # might be more trouble than it's worth - https://docs.python.org/3.7/extending/extending.html
    # though not if I end up having to do a bunch of iteration for learning models &c.
    def random_at_most(self,max):
    #   unsigned long
    #     // max <= RAND_MAX < ULONG_MAX, so this is okay.
        num_bins = max + 1
        num_rand = self.random_max + 1
        bin_size = num_rand // num_bins
        defect   = num_rand % num_bins

        #   long x;
        #   do {
        #    x = random();
        #   }
        #   // This is carefully written not to overflow
        #   while (num_rand - defect <= (unsigned long)x);
        # no "do" loop in python
        firstloop = True
        while (firstloop or (num_rand - defect <= x)):
            firstloop = False
            x = self.random()

        # Truncated division is intentional
        return x//bin_size;



    # computer version of get_input - inmin and inmax are both inclusive
    # can loop forever if inexclude excludes all possible values, TODO fix that
    # in arduino version we can assume caller gets it right bc that is the spirit of C
    def get_computer_input(self,inmin, inmax, inexclude=None):
        while True:
            num = inmin + self.random_at_most((inmax-inmin)+1)
            if inexclude is None:
                return num
            if num not in inexclude:
                return num

    # THE PLAY -----------------------------------------------------------------------------------------------------------

    # the play: pone and dealer are players, after discard, but with full hand
    # this can now play the following correctly from http://cribbagecorner.com/cribbage-rules-go
    # An example sequence of play showing the rules for pegging points by both players:
    #
    # Alice (pone) plays a 4, for a total of 4, and says 'Four.'
    # Bob plays a 7, for a total of 11, and says 'Eleven'.
    # Alice plays another 4, for a total of 15, and says 'Fifteen for two.' [and pegs 2 points]
    # Bob plays a Jack, for a total of 25, and says 'Twenty-five'.
    # Alice cannot go, as any of her remaining cards would take the total over 31. She says 'go'.
    # Bob plays a 5, for a total of 30, and says 'Thirty, and one for the go' [and pegs 1 point]
    #
    # The count now goes back to zero, and the play continues. Since Bob played the last card, Alice goes
    # first now.
    #
    # Alice plays a 7, for a total of 7, and says 'Seven'.
    # Bob plays an 8, for a total of 15, and says 'Fifteen for two.' [and pegs 2 points]
    # Alice plays a 9, for a total of 24, and says 'Twenty-four for three'. [and pegs 3 points for her run
    # of 7-8-9]
    # Bob cannot go, as he has run out of cards. He therefore says 'Go', and Alice pegs a point for the go.
    # She also has run out of cards and so the game proceeds to the next phase.
    #
    # Another example:
    #
    # Bob (pone) plays a 4, for a total of 4, and says 'Four.'
    # Alice plays another 4, for a total of 8, and says 'Eight for two.' [and pegs 2 points for the pair]
    # Bob plays a third 4, for a total of 12, and says 'Twelve for six.' [and pegs 6 points for the pair
    # royal ]
    # Alice plays a 3, for a total of 15, and says 'Fifteen for two.' [and pegs 2 points]
    # Bob plays a 2 for a total of 17 and says 'Seventeen for three.' [and pegs 3 points for the run 4-3-2]
    # Alice plays a 5, for a total of 22, and says 'Twenty-two for four.' [and pegs 4 points for the run
    # 5-4-3-2]]
    # Bob cannot go without going over 31, and so says 'Go'.
    # Alice plays a 9, for a total of 31, and says 'Thirty-one for two.' [and pegs 2 points. 'One for the
    # go' is only scored when the scoring player does not make 31. ]
    #
    # The count is now reset, and Bob plays first, as Alice played last.
    #
    # Bob plays a Queen, for a total of 10, and says 'Ten.'
    # Alice cannot go, as she has run out of cards, and so says 'Go'. [ Bob pegs 1 point for the go. ]
    #
    # For tips on how to make the most of the go, see the cribbage strategy section.
    #
    # If you say 'Go' when you had a card you could legally play, this is a breach of the rules called a
    # renege. (I will disallow this, have the machine yell)
    # TODO: come up with test cases and how to make this work as unit tests with visibility into what happens
    # inside the play; perhaps play function should return an ordering of how the cards were played, one list
    # of cards per count, also noting who played them, and final scores?

    # return True if somebody won
    def do_play(self,dealer,pone):
        play_is_done = False
        # k so play consists of some number of counts. Whoever did not go last in the previous count gets to go
        # first in a new count.
        dealer_played_last = True  # bc for first count, pone goes first
        while not play_is_done:
            print("New count -----------------------------------------------------------")
            print("Pone" if dealer_played_last == True else "Dealer","plays first")
            curcards = []
            player_called_go = -1  # 0 means dealer, 1 means pone, -1 means nobody yet
            count_is_done = False

            while not count_is_done:
                # print("play not done infinite loop spotter")
                # who goes first? for the first coune: The pone shall play the first card face up on the
                # table, announcing its value.
                # Subsequent, the player who didn't play last.
                if dealer_played_last == True:          # dealer played last, so pone plays
                    print("Dealer played last so pone goes")
                    dealer_played_last = False          # let's try setting this in every case?
                    if player_called_go != 1:
                        print(pone.get_name(),"the pone play:")
                        (curcards, curtotal, newscore) = pone.play(curcards)
                        print("curcards now", [self.cardstring(x) for x in curcards], "curtotal", curtotal)
                        if newscore == -1:
                            # so: this means "go." if player_called_go is -1, mark that pone has said "go"
                            if player_called_go == -1:
                                print("Pone calls go!")
                                player_called_go = 1
                            elif player_called_go == 0:
                                # other player called go and so now we're done with this count
                                print("Pone played out after dealer said go")
                                count_is_done = True
                                # at this point, if pone played any cards and total is not 31, that means pone
                                # gets the one-for last, yes?
                                # how do we know pone played any cards? This happens bc they *couldn't*,
                                # so it would have had to have been last time through, then skip dealer.
                                # or is it that pone has to have played to get here?
                                if curtotal != 31:
                                    print(pone.get_name()," the pone pegs 1 for last")
                                    if pone.add_score(1) == True:
                                        # pone wins!
                                        return True
                                else:
                                    print("########### Total is 31, nobody gets 1")
                                # let's force dealer played last = false here so next count starts with dealer
                                dealer_played_last = False
                        else:
                            # actually played a card, so dealer played last is False
                            # ok this doesn't stop infinite loops
                            # dealer_played_last = False
                            if newscore != 0:
                                print("Adding score for pone:", newscore)
                                if pone.add_score(newscore) == True:
                                    # pone wins
                                    return True
                else:       # dealer_played_last == False, so dealer plays
                    print("Pone played last so dealer goes")
                    dealer_played_last = True          # let's try setting this in every case?
                    if player_called_go != 0:
                        print(dealer.get_name(),"the dealer play:")
                        (curcards, curtotal, newscore) = dealer.play(curcards)
                        print("curcards now", [self.cardstring(x) for x in curcards], "curtotal", curtotal)
                        if newscore == -1:
                            if player_called_go == -1:
                                print("Dealer calls go!")
                                player_called_go = 0  # dealer said go
                            elif player_called_go == 1:
                                # other player called go and so now we're done with this count
                                print("Dealer played out after pone said go")
                                count_is_done = True
                                # SEE ABOVE re: how pone handles one-for-last n stuff
                                if curtotal != 31:
                                    print(dealer.get_name()," the dealer pegs 1 for last")
                                    if dealer.add_score(1) == True:
                                        # dealer wins!
                                        return True
                                else:
                                    print("########### Total is 31, nobody gets 1")
                                # let's force dealer played last = true here so next count starts with pone
                                dealer_played_last = True
                        else:
                            # actually played a card, so dealer played last is True
                            # doesn't stop infinite loops
                            #dealer_played_last = True
                            if newscore != 0:
                                print("Adding score for dealer:", newscore)
                                if dealer.add_score(newscore) == True:
                                    # dealer wins
                                    return True

            # ok, hand is done, if nobody has any cards left, play is done
            if len(pone.get_cards()) == 0 and len(dealer.get_cards()) == 0:
                play_is_done = True

# HEREAFTER UNCHANGED *************************************************************************************************

    def do_game(self):
        # quick random_at_most test paralleling the one in random.c
        # do a million of 52, then a million of 6 - matched!
        # for j in range(0,1000000):
        #    print(random_at_most(52))
        # for j in range(0,1000000):
        #    print(random_at_most(6))
        # sys.exit(0)

        # end quick random_at_most test

        # quick play tests that could turn into unit tests
        do_play_tests = False
        if do_play_tests:
            print("TEMP PLAY TESTS ===================================================================")

            # let's enact this, with players that play the first legal card in their hand.
            # Alice (pone) plays a 4, for a total of 4, and says 'Four.'
            # Bob plays a 7, for a total of 11, and says 'Eleven'.
            # Alice plays another 4, for a total of 15, and says 'Fifteen for two.' [and pegs 2 points]
            # Bob plays a Jack, for a total of 25, and says 'Twenty-five'.
            # Alice cannot go, as any of her remaining cards would take the total over 31. She says 'go'.
            # Bob plays a 5, for a total of 30, and says 'Thirty, and one for the go' [and pegs 1 point]

            # The count now goes back to zero, and the play continues. Since Bob played the last card, Alice goes first now.

            # Alice plays a 7, for a total of 7, and says 'Seven'.
            # Bob plays an 8, for a total of 15, and says 'Fifteen for two.' [and pegs 2 points]
            # Alice plays a 9, for a total of 24, and says 'Twenty-four for three'. [and pegs 3 points for her run of 7-8-9]
            # Bob cannot go, as he has run out of cards. He therefore says 'Go', and Alice pegs a point for the go. She also
            # has run out of cards and so the game proceeds to the next phase.
            # players don't need a crib for this, I reckon
            # + I do know how to spell "scenario" but I've seen it wrong online so much that the right spelling looks weird
            print(
                "SENERIO 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            # Alice the Pone
            pone = PlayFirstLegalCardPlayer(cards=[self.stringcard(x) for x in ['4c', '4d', '7h', '9d']],
                                            dealer=False, score=0, name="Alice")
            # Bob the Dealer
            dealer = PlayFirstLegalCardPlayer(cards=[self.stringcard(x) for x in ['7c', 'Jd', '5h', '8c']],
                                              dealer=True, score=0, name="Bob")
            self.do_play(dealer, pone)
            # YAY that seems to have worked

            print(
                "SENERIO 2 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            # then try a variant where Bob's got a 2 and a 4, so he can play 2 cards after Alice says go, and gets 31
            # Alice the Pone
            pone = PlayFirstLegalCardPlayer(cards=[self.stringcard(x) for x in ['4c', '4d', 'Jh', 'Qd']],
                                            dealer=False, score=0, name="Alice")
            # Bob the Dealer
            dealer = PlayFirstLegalCardPlayer(cards=[self.stringcard(x) for x in ['7c', 'Jd', '2h', '4h']],
                                              dealer=True, score=0, name="Bob")
            self.do_play(dealer, pone)
            # WORKY!!!!!!!!!!!!!!!!

            print(
                "SENERIO 3 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            # then try a variant where Bob's got a 2 and a A, so he can play 2 cards after Alice says go, and gets 1 for last
            # Alice the Pone
            pone = PlayFirstLegalCardPlayer(cards=[self.stringcard(x) for x in ['4c', '4d', 'Jh', 'Qd']],
                                            dealer=False, score=0, name="Alice")
            # Bob the Dealer
            dealer = PlayFirstLegalCardPlayer(cards=[self.stringcard(x) for x in ['7c', 'Jd', '2h', 'Ah']],
                                              dealer=True, score=0, name="Bob")
            self.do_play(dealer, pone)
            # WORKY!!!!!!!!!!!!!!!!

            print(
                "SENERIO 4 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            # Bob (pone) plays a 4, for a total of 4, and says 'Four.'
            # Alice plays another 4, for a total of 8, and says 'Eight for two.' [and pegs 2 points for the pair]
            # Bob plays a third 4, for a total of 12, and says 'Twelve for six.' [and pegs 6 points for the pair
            # royal ]
            # Alice plays a 3, for a total of 15, and says 'Fifteen for two.' [and pegs 2 points]
            # Bob plays a 2 for a total of 17 and says 'Seventeen for three.' [and pegs 3 points for the run 4-3-2]
            # Alice plays a 5, for a total of 22, and says 'Twenty-two for four.' [and pegs 4 points for the run
            # 5-4-3-2]]
            # Bob cannot go without going over 31, and so says 'Go'.
            # Alice plays a 9, for a total of 31, and says 'Thirty-one for two.' [and pegs 2 points. 'One for the
            # go' is only scored when the scoring player does not make 31. ]
            #
            # The count is now reset, and Bob plays first, as Alice played last.
            #
            # Bob plays a Queen, for a total of 10, and says 'Ten.'
            # Alice cannot go, as she has run out of cards, and so says 'Go'. [ Bob pegs 1 point for the go. ]

            # Bob the Pone
            pone = PlayFirstLegalCardPlayer(cards=[self.stringcard(x) for x in ['4h', '4d', '2c', 'Qh']],
                                            dealer=False, score=0, name="Bob")
            # Alice the Dealer
            dealer = PlayFirstLegalCardPlayer(cards=[self.stringcard(x) for x in ['4c', '3d', '5c', '9d']],
                                              dealer=True, score=0, name="Alice")
            self.do_play(dealer, pone)
            # WORKY!!!!!!!!!!!!!!!!!!

            print(
                "SENERIO 5 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            # then try a variant of the first senerio so Alice plays last in 1st count, ensure dealer plays first
            # Alice the Pone
            pone = PlayFirstLegalCardPlayer(cards=[self.stringcard(x) for x in ['4c', '4d', '5h', 'Qd']],
                                            dealer=False, score=0, name="Alice")
            # Bob the Dealer
            dealer = PlayFirstLegalCardPlayer(cards=[self.stringcard(x) for x in ['7c', 'Jd', 'Qh', 'Jh']],
                                              dealer=True, score=0, name="Bob")
            self.do_play(dealer, pone)
            # WORKY!!!!!!!!!!!!

            # TODO: come up with other cases and how to make this work as unit tests with visibility into what happens
            # inside the play; perhaps play function should return an ordering of how the cards were played, one list
            # of cards per count, also noting who played them, and final scores?

            print("TEMP END ===========================================================================")
            sys.exit(0)

        # OK NOW FOR THE REAL THING ======================================================================================
        # Create players
        print("Creating players...")
        players = [HumanPlayer(self,name="Human"), Player(self,name="Computer")]
        dealer = None
        pone = None
        for player in players:
            player.print()
        print("-----------------------------------------------------")

        # Initial shuffle
        print("*** Initial shuffle...")
        self.srandom(1043865)
        deck = self.shuffle()
        cardnum = 0;  # first card to be dealt, when dealing in order
        # print("deck is",deck)
        print("---")

        # TODO: ACC rules say cut for deal of the first game, thereafter the loser of the previous game is dealer.
        # TODO: am I planning to do multiple game sessions? I guess so
        # Cut for deal
        #     Each player cuts
        #         according to their class's algorithm, human player or computer
        #     Low card is dealer
        #         i.e., set dealer flag in the player who got the low card
        #         Per cribbage.org Thereafter the loser of the previous game deals first.
        # I guess do this until there is a clear difference in rank
        # with the usual seed, choosing 38 gets a tie, then 11 gets another one! if deck reused
        # let's reshuffle between the cuts so we never run out of cards
        comprank = -1
        playerrank = -1
        while comprank == playerrank:
            print("*** Cut for deal!")
            cutspot = self.get_input(4, 48)
            deck = self.cut(deck, cutspot)
            # print("Deck is now",deck)
            (deck, playercard) = self.deal_card(deck)
            print("You turned up ", self.cardstring(playercard))
            print("*** Now I cut!")
            compcutspot = self.get_computer_input(4, len(deck) - 4)
            print("my cut spot", compcutspot)
            deck = self.cut(deck, compcutspot)
            # print("Deck is now",deck)
            (deck, compcard) = self.deal_card(deck)
            print("I turned up", self.cardstring(compcard))
            playerrank = self.rank(playercard)
            comprank = self.rank(compcard)
            if playerrank < comprank:
                print("You get first deal!")
                players[0].set_dealer(True)
                players[1].set_dealer(False)
                dealer = players[0]
                pone = players[1]
            elif playerrank > comprank:
                print("I get first deal!")
                players[0].set_dealer(False)
                players[1].set_dealer(True)
                dealer = players[1]
                pone = players[0]
            else:
                print("Tie! do it again! - reshuffling")
                deck = self.shuffle()

        print("************************* THE GAME BEGINS! *************************************************")

        # Until somebody wins:
        while players[0].get_score() < 121 and players[1].get_score() < 121:
            #     Shuffle

            print(
                "NEW HAND %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            print("*** Shuffling...")
            deck = self.shuffle()

            #     Pone Cut
            # print("Deck is now",deck)
            print("*** cut...")
            deck = pone.cut(deck)
            # print("Deck is now",deck)

            #     Deal 6 cards to each player
            print("*** Dealing...")
            for j in range(0, 6):
                (deck, nextcard) = self.deal_card(deck)
                pone.add_card(nextcard)
                (deck, nextcard) = self.deal_card(deck)
                dealer.add_card(nextcard)

            print("*** now players are like this")
            for player in players:
                player.print()

            #     Discard
            #         See below re: thoughts on how to do this
            print("Discard...")
            players[0].discard(players[1])
            players[1].discard(players[0])

            #     Pone Cuts to get starter card
            #         If it's a jack, dealer gets 2
            print("Cut for starter ...")
            pone.cut(deck)
            (deck, starter) = self.deal_card(deck)
            print("*** starter card is", self.cardstring(starter))
            # 2 points to dealer if it's a jack - cut at 34 to get this w/default
            if self.rank(starter) == self.rank(self.stringcard('JH')):
                print("*** Heels! 2 points to dealer!")
                if dealer.add_score(2) == True:
                    # dealer wins
                    break

            print("*** now players are like this")
            for player in players:
                player.print()

            #     Play
            #         I believe this is done as of 3/21, other than "go"
            print("*** now for the play! ================================================= ")
            # let's break this out into a function that can be unit-tested!
            self.do_play(dealer, pone)

            print("*** now for the shew! ================================================= ")
            #     Shew
            # restore players' used_cards back to their hand
            pone.set_cards(pone.get_used_cards())
            pone.set_used_cards([])
            dealer.set_cards(dealer.get_used_cards())
            dealer.set_used_cards([])

            # looks like the show counts as a single pegging per player, so no need to fiddle with score_shew, I think.
            # per rules,
            # When both players have played all their cards,
            # the pone’s hand is counted and pegged by the
            # pone (see scoring chart). The dealer then does
            # the same for the dealer’s hand and then for the
            # crib.

            print("*** pone shew:")
            (ponescore, scoresubs) = self.score_shew(pone.get_cards(), starter)
            self.render_score_subsets(pone.get_cards(), starter, scoresubs)
            print("Adding score for pone:", ponescore)
            if pone.add_score(ponescore) == True:
                # pone wins!
                break
            print("*** dealer shew:")
            (dealerscore, dealersubs) = self.score_shew(dealer.get_cards(), starter)
            self.render_score_subsets(dealer.get_cards(), starter, dealersubs)
            print("Adding score for dealer:", dealerscore)
            if dealer.add_score(dealerscore) == True:
                # dealer wins
                break
            print("*** dealer crib shew:")
            (cribscore, cribsubs) = self.score_shew(dealer.get_crib(), starter)
            self.render_score_subsets(dealer.get_crib(), starter, cribsubs)
            print("Adding crib score for dealer:", cribscore)
            if dealer.add_score(cribscore) == True:
                # dealer wins
                break

            print(pone.get_name(), "score:", pone.get_score())
            print(dealer.get_name(), "score:", dealer.get_score())

            # if nobody won,
            if dealer.get_score() < 121 and pone.get_score() < 121:
                # clear hands and get ready for another round
                # swap dealer and pone - or rather, says whoever lost the last hand deals next
                pone.set_cards([])

                dealer.set_cards([])
                dealer.set_crib([])

                # choose new dealer - per ACC rules, The pack is cut to determine which player will
                # deal first in the first game of a match; the low card wins the deal. Thereafter the loser of the
                # previous game deals first.
                # but that's over games; cribbage corner says deal alternates bt hands, so let's do that.
                if players[0].is_dealer():
                    pone = players[0]
                    dealer = players[1]
                else:
                    pone = players[1]
                    dealer = players[0]
                pone.set_dealer(False)
                dealer.set_dealer(True)

        # OK, somebody won!
        print(
            "THE GAME ENDS! ###########################################################################################")
        if dealer.get_score() > 120:
            print(dealer.get_name(), "WINS!!!!!!!!!!!!!!!!!!!")
        else:
            print(pone.get_name(), "WINS!!!!!!!!!!!!!!!!!!!")# main -------------------------------------------------------------------------------------------


if __name__ == "__main__":

    print("Hello and welcome to PYBBAGE, the python cribbage mockup for my mcu cribbage games.")

    pyb = Pybbage()
    pyb.do_game()

