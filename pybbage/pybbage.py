import sys


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


def cardstring(card):
    '''card is a number from 0-51; card %4 is rank, where 0 = hearts, 1 = diamonds, 2 = clubs, 3 = spades.
    card // 4 is rank, 0 = ace .. 12 = king
    '''
    if card not in range(0,52):
        print("Illegal card value",card)
        return None
    return 'A234567890JQK'[card // 4] + '♥♦♣♠'[card % 4]

# shuffle returns a 52 element list of random numbers, s.t. the index into the list is the card, like 0 = ace of horts,
# .. 51 = King of Spades.
# the LOL here is that this takes 208 bytes and I couldn't use it for vpok bc that's more RAM than a PIC 16F628 has.
# Uno R3 / atmega328 has 2K ram, yes? Some taken by the arduino core but not lots
# also returns the value associated with the lowest value in the list, which is the first card that will be dealt.
# old version with non-rewritten order
#def shuffle():
#    deck = {'order':[random() for i in range(0,52)], 'dealt':[0 for i in range(0,52)] }
#    deckmin = min(deck['order'])
#    return (deck, deckmin)
# this version will do rewriting of order from 0..51
# and that will be the value of the card, the index won't be!
def shuffle():
    deck = {'value':[random() for i in range(0,52)], 'dealt':[0 for i in range(0,52)] }
    curmin = min(deck['value'])
    # the arduino version will look quite different, searching instead of listbuilding
    for val in range(0,52):
        card = deck['value'].index(curmin)
        deck['value'][card] = val
        gtmin = list(filter(lambda x:x>curmin,deck['value']))
        if len(gtmin) > 0:
            curmin = min(gtmin)
    return deck

# cardnum is 0 when the deck is new
def deal_card(deck,cardnum):
    newcardnum = cardnum
    while newcardnum < 52:
        if deck['dealt'][newcardnum] == 1:
            # card has already been dealt, go to next
            print("Card",cardstring(newcardnum),"has been dealt! Moving on")
            newcardnum += 1
        else:
            deck['dealt'][newcardnum] = 1
            return (deck['value'][newcardnum],newcardnum+1)
    print("End of deck")
    return (None,None)


# deal_card "deals" by finding the card with the value curmin. Then it scans deck for the next minimum value, i.e. the one
# that is the next highest.
# returns a tuple of (index of curmin, nextmin)
# i.e. index of curmin is the rank/suit value of the card that is dealt.
# then can be called with deck, nextmin next time
# if nextmin is the highest number in the deck, return None for nextmin, signifiying a need to reshuffle.
# OK THIS WORKS but does not account for things like a randomly yanked card, as from a cut.
# Should I put a flag alongside the cards and if curmin's dealt-flag is set, go to next? yeah.
#def deal_card(deck, curmin):
# before using dealt flag
#    if curmin not in deck['order']:
#        return (None,None)
#    card = deck['order'].index(curmin)
#    gtmin = list(filter(lambda x:x>curmin,deck['order']))
#    if len(gtmin) == 0:
#        return (card,None)
#    return (card, min(gtmin))

# second version with non-rewritten order
#def deal_card(deck, curmin):
#    while curmin is not None:
#        if curmin not in deck['order']:
#            return (None,None)
#        card = deck['order'].index(curmin)
#        gtmin = list(filter(lambda x:x>curmin,deck['order']))
#        if len(gtmin) == 0:
#            # this is the last card - if it's been dealt, we're done
#            if deck['dealt'][card] == 0:
#                # hasn't been dealt: deal it!
#                deck['dealt'][card] = 1
#                return (card,None)
#            else:
#                # has been dealt - we're out!
#                print("**** card", cardstring(card), "has been dealt and we're out")
#                return (None,None)
#        # if the card has been dealt, try another. If not, deal it!
#        if deck['dealt'][card] == 0:
#            #not been dealt, deal it
#            deck['dealt'][card] = 1
#            return (card, min(gtmin))
#        else:
#            print("**** card",cardstring(card),"has been dealt!!!! trying next")
#            # advance curmin, try next card
#            curmin = min(gtmin)
#    # went to where curmin is None...
#    return(None, None)


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
    srandom(1)
    deck = shuffle()
    cardnum = 0;            # first card to be dealt, when dealing in order
    # do a cut!
    # WRITE THIS!!!!!!!!!!!
    # then deal
    for j in range(0,54):
        (card, cardnum) = deal_card(deck, cardnum)
        print(j,cardstring(card),cardnum)
    # MAKE SURE THIS IS RIGHT, MAYBE SEE IF OLD AND NEW CARD DEALS GET THE SAME ORDER? DOES IT MATTER?
    # ALSO MAKE SURE NO CARD IS DUPLICATED OR ANYTHING