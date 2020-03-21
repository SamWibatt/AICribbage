import sys

#print("I am pybbage!")

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

global rand_next, random_max
rand_next = 1
random_max = 0x7FFFFFFF

def do_random(ctx):
    global rand_next
    x = ctx
    # Can't be initialized with 0, so use another value.
    if (x == 0):
        x = 123459876
    hi = x // 127773       # // should be integer divide
    lo = x % 127773
    x = 16807 * lo - 2836 * hi
    if (x < 0):
        x += 0x7fffffff
    rand_next = x
    return x % (random_max + 1)


def random():
    global rand_next
    return do_random(rand_next)

def srandom(seed):
    global rand_next
    rand_next = seed;

# card handling routines -------------------------------------------------------------------------

def rank(card):
    return card // 4

def val(card):
    '''value, s.t. ace = 1, 2 = 2, ... 10 and face cards = 10'''
    return rank(card)+1 if rank(card) < 10 else 10

def suit(card):
    return card % 4


def cardstring(card):
    '''card is a number from 0-51; card %4 is rank, where 0 = hearts, 1 = diamonds, 2 = clubs, 3 = spades.
    card // 4 is rank, 0 = ace .. 12 = king
    '''
    if card not in range(0,52):
        print("Illegal card value",card)
        return None
    return 'A234567890JQK'[rank(card)] + '♥♦♣♠'[suit(card)]

# this is mostly for debugging and unit testing
def stringcard(strc):
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
def shuffle():
    newdeck = {'order':[random() for i in range(0,52)],
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

# cardnum is 0 when the deck is new - no longer using dealt flag
# deck is just an array now
def deal_card(deck,cardnum):
    if cardnum is not None and cardnum < 52:
        return (deck[cardnum],cardnum+1)
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
# TODO encode all this!!!!!!!!!!!!!!!!!!!!!!!!!
def cut(deck,index):
    if index >= 1 and index < len(deck):
        return deck[index:] + deck[:index]
    print("Illegal cut index",index,"- not doing cut")
    return deck;


# classes ----------------------------------------------------------------------------------------

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

# K so I have a player object. What do we know about players?
# - what cards they hold and which are "used"
# - whether they're the dealer
# - their score
class Player:
    def __init__(self):
        self.cards = []
        self.used_cards = []
        pass

    def add_card(self,card):
        self.cards.append(card)


# let's just try scoring a show, damn the data structures for now
# where hand is a list of 0..51, starter is the up-card 0..51
# assumed to be correct i.e. no duplicates or illegal values
def score_shew(hand,starter):
    curscore = 0

    # for convenience
    cards = hand + [starter]

    # look for fifteens ===============================================================================================
    # what is the power set of cards? I suppose we need to check
    # all two-card sums (of which there are 5 choose 2 = 10)
    for i in range(0,4):
        for j in range(i+1,5):
            if val(cards[i]) + val(cards[j]) == 15:
                curscore += 2
                print(cardstring(cards[i]),cardstring(cards[j]),"... 15 -",curscore)
    # all three-card sums (of which there are 5 choose 3 = 10, which = inverse of 5 choose 2, I guess)
    for i in range(0,3):
        for j in range(i+1,4):
            for k in range(j+1,5):
                if val(cards[i]) + val(cards[j]) + val(cards[k]) == 15:
                    curscore += 2
                    print(cardstring(cards[i]), cardstring(cards[j]), cardstring(cards[k]), "... 15 -", curscore)
    # all four-card sums (of which there are 5 choose 4 = 5)
    for i in range(0,5):
        subcards = [x for x in cards]           # need to make a new copy...??? yup
        #print("About to remove",cards[i],"from",subcards)
        subcards.remove(cards[i])
        if sum([val(x) for x in subcards]) == 15:
            curscore += 2
            for cs in [cardstring(x) for x in subcards]:
                print(cs,end=' ')
            print("... 15 -",curscore)

    # all 5 cards' sum (1 sum)
    if sum([val(x) for x in cards]) == 15:
        curscore += 2
        for cs in [cardstring(x) for x in cards]:
            print(cs, end=' ')
        print("... 15 -", curscore)

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
    sortcards = sorted(cards)
    sortranks = [rank(x) for x in sortcards]
    normsranks = [x - min(sortranks) for x in sortranks]
    #print("sortcards =",[cardstring(x) for x in sortcards],"sortranks =",sortranks,"normsranks =",normsranks)

    # 5-card scores: sequence, name, points. VERIFY SCORING
    # 5-carders preclude any other scores for runs or pairs. 15s, flushes, nobs still ok.
    fivecarders = [
        [[0, 1, 2, 3, 4], "run of 5", 5],           #  5 = 5*1 per card
        [[0, 0, 0, 1, 2], "triple run", 15],        # 15 = 3*3 runs + 3*2 pairs
        [[0, 1, 1, 1, 2], "triple run", 15],
        [[0, 1, 2, 2, 2], "triple run", 15],
        [[0, 0, 1, 1, 2], "double double run", 16], # 16 = 4*3 runs + 2*2 pairs
        [[0, 0, 1, 2, 2], "double double run", 16],
        [[0, 1, 1, 2, 2], "double double run", 16],
        [[0, 0, 1, 2, 3], "double run of 4", 10],   # 10 = 2*4 runs + 1*2 pairs
        [[0, 1, 1, 2, 3], "double run of 4", 10],
        [[0, 1, 2, 2, 3], "double run of 4", 10],
        [[0, 1, 2, 3, 3], "double run of 4", 10]]

    found_fivecarder = 0            # flag: if any five-carders found, don't use pairs
    for fivey in fivecarders:
        if normsranks == fivey[0]:
            found_fivecarder = 1
            curscore += fivey[2]
            for cs in [cardstring(x) for x in cards]:
                print(cs,end=' ')
            print("...", fivey[1],"-",curscore)
            break

    if found_fivecarder == 0:
        # runs! first look for 4s - if there are any, can't be any 3s, yes?
        found_fourcarders = 0
        # so try the first 4 and last 4 among the normsranks, yes?
        if normsranks[:4] == [0,1,2,3]:
            found_fourcarders = 1
            curscore += 4
            for i in range(0,4):
                print(cardstring(sortcards[i]),end=' ')
            print("... run of 4 -",curscore)
        elif normsranks[:4] == [0,0,1,2] or normsranks[:4] == [0,1,1,2] or normsranks[:4] == [0,1,2,2]:
            found_fourcarders = 1
            curscore += 8           # 2*3 + pr
            for i in range(0,4):
                print(cardstring(sortcards[i]),end=' ')
            print("... double run -",curscore)
        else:
            nranks2 = [x - min(normsranks[1:]) for x in normsranks[1:]]
            #print("normsranks =",normsranks,"nranks2 =",nranks2)
            if nranks2 == [0,1,2,3]:
                found_fourcarders = 2
                curscore += 4
                for i in range(1, 5):
                    print(cardstring(sortcards[i]), end=' ')
                print("... run of 4 -", curscore)
            elif nranks2 == [0, 0, 1, 2] or nranks2 == [0, 1, 1, 2] or nranks2 == [0, 1, 2, 2]:
                found_fourcarders = 2
                curscore += 8  # 2*3 + pr
                for i in range(1, 5):
                    print(cardstring(sortcards[i]), end=' ')
                print("... double run -", curscore)

    # Count pairs if no higher-order hand precludes
    if found_fivecarder == 0 and found_fourcarders == 0:
        pairranks = []
        numpairs = 0
        for i in range(0,4):
            for j in range(i+1,5):
                if rank(cards[i]) == rank(cards[j]):
                    numpairs +=1
                    if rank(cards[i]) not in pairranks:
                        pairranks.append(rank(cards[i]))
        curscore += 2 * numpairs
        # if there were pairs, emit participating cards
        for ranky in pairranks:
            for i in range(0,5):
                if rank(cards[i]) == ranky:
                    print(cardstring(cards[i]),end=' ')
        if numpairs > 0:
            if numpairs == 1:
                print("... pair",end=' ')
            elif numpairs == 2:
                print("... two pair",end=' ')
            elif numpairs == 3:
                print("... 3 of a kind",end=' ')
            elif numpairs == 4:
                # this is kind of gross but w/e
                print("... 3 of a kind and pair",end=' ')
            elif numpairs == 6:
                print("... 4 of a kind",end=' ')
            print("-",curscore)
            #print("Found",numpairs,"pairs")  # debug do we need?

        # so if found_fourcarders = 1, the first 4 were a run, so the last card can be in other scores?
        # if it's 2, the last 4 were, so first card can be in other scores? Does it matter?
        if found_fourcarders == 0:
            # nicked from the fifteens:
            for i in range(0, 3):
                for j in range(i + 1, 4):
                    for k in range(j + 1, 5):
                        # how do we look for a run? get the sorted of the 3 cards' ranks.
                        nsrnks = sorted([rank(cards[i]),rank(cards[j]),rank(cards[k])])
                        nsrnks = [x-min(nsrnks) for x in nsrnks]
                        if nsrnks == [0,1,2]:
                            curscore += 3
                            print(cardstring(cards[i]),cardstring(cards[j]),cardstring(cards[k]),"... run of 3 -",
                                  curscore)

    # flushes =========================================================================================================
    # not quite clear on this - from the rules
    # Four cards of the same suit held in the
    # hand count four points; five cards of the
    # same suit (including the starter card)
    # count five points in the hand or crib.
    # I think that means if the non-starters are all the same suit, it's 4, and the starter only counts
    # as the 5th
    if suit(hand[0]) == suit(hand[1]) and suit(hand[1]) == suit(hand[2]) and suit(hand[2]) == suit(hand[3]):
        if suit(hand[3]) == suit(starter):
            curscore += 5
            for cs in [cardstring(x) for x in cards]:
                print(cs,end=' ')
            print("... 5 card flush -",curscore)
        else:
            curscore += 4
            for cs in [cardstring(x) for x in hand]:
                print(cs,end=' ')
            print("... 4 card flush -",curscore)

    # and finally, nobs ===============================================================================================
    for i in range(0,4):
       if rank(hand[i]) == 10 and suit(hand[i]) == suit(starter):
            curscore += 1
            print(cardstring(hand[i]), cardstring(starter),"... nobs -", curscore)
            break

    # finally, at long last, return score - but if it's 0, say nineteen bc that's all clever
    if curscore == 0:
        for cs in [cardstring(x) for x in cards]:
            print(cs,end=' ')
        print("... NINETEEN!")

    return curscore


# SCORING THE PLAY / COUNT ============================================================================================
# given: the cards that have been played so far, list of 0..51
# and card to be played
# return: (cards now played = cards so far + played, score for playing the given card or -1 for error)
# not a serious error, I expect this to be a "lookahead" function for deciding what card to play for the computer
def play_card(curcards, newcard):
    newcards = curcards if curcards is not None else []
    curscore = 0

    newcards = newcards + [newcard]
    curtotal = sum([val(x) for x in newcards])

    print("-- running total",curtotal)

    # figure out if newcard CAN be played on newcards, yes?
    # - can't go over 31 - is that the only limitation? I suppose so
    if curtotal > 31:
        return(curcards,-1)         # error

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
    currank = rank(newcard)
    # pairs are easy bc you can only go up to 4 of a kind. loopify this when I see a pattern
    # or leave it like it is if I want to
    # ifs are nested bc if there is a discontinuity, the chain breaks.
    if len(curcards) >=1 and rank(curcards[-1]) == currank:
        numrankmatch += 1
        if len(curcards) >=2 and rank(curcards[-2]) == currank:
            numrankmatch += 1
            if len(curcards) >=3 and rank(curcards[-3]) == currank:
                numrankmatch += 1
    # so, numrankmatch + 1 is the number of matching cards, not including the played card.
    if numrankmatch == 1:
        curscore += 2
        print("... pair - ",curscore)
    elif numrankmatch == 2:
        curscore += 6
        print("... three of a kind - ",curscore)
    elif numrankmatch == 3:
        curscore += 12
        print("... four of a kind - ",curscore)

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
        sorty = [rank(x) for x in sorted(newcards[i:])]
        ns = [x-min(sorty) for x in sorty]
        if ns == list(range(0,-i)):
            longestrun = -i

    if longestrun != 0:
        curscore += longestrun
        print(" ... run of",longestrun,"-",curscore)


    return(newcards,curscore)
    pass

# main -------------------------------------------------------------------------------------------


if __name__ == "__main__":
    print("Hello and welcome to PYBBAGE, the python cribbage mockup for my mcu cribbage games.")
    #print("Let's see some cards")
    #for j in range(0,53):
    #    print(j,cardstring(j))
    # print the first hundred million random numbers and see if they agree with the c version
    # which worked!
    #for j in range(0,100000000):
    #    print(random())
    srandom(1043865)
    deck = shuffle()
    cardnum = 0;            # first card to be dealt, when dealing in order
    # do a cut!
    # WRITE THIS!!!!!!!!!!!
    # then deal
    #for j in range(0,54):
    #    (card, cardnum) = deal_card(deck, cardnum)
    #    print(j,cardstring(card),cardnum)

    # let's dump the new one as csv and see what's up - seems correct! sorting by order made the value column
    # consecutive. So away goes the auld way.
    #print("card,value,order")
    #for j in range(0,52):
    #    print("{},{},{}".format(cardstring(deck['value'][j]),deck['value'][j],deck['order'][j]))

    # scoring! - now moved basically to unit tests - can recover from old commits if I want to, pre 3/20/20 8:36 pm
    # such as e45edf3fcba455880b91da589c6d2f9842996641 "initial show unit tests"

    # so ok, time for the play/count!
    print("Time for play. ----------------------")
    totalscore = 0
    curcards = []
    handcards = ['5h','5c','5d','5s','4h','6d','as','qh']
    for nc in handcards:
        newcard = stringcard(nc)
        print("playing",cardstring(newcard),"on",[cardstring(x) for x in curcards])
        (resultcards,resscore) = play_card(curcards,newcard)
        print("Result cards:",[cardstring(x) for x in resultcards],"score",resscore)
        if resscore == -1:
            print("done")
            break
        else:
            # accumulate total score and played cards
            curcards = resultcards
            totalscore += resscore
    print("total score:",totalscore)





