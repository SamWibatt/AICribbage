# cut for deal mode!

import arcade
import os
import pyglet.gl as gl
# then my actual game mechanics!
from pyb import pybbage as pyb

# not happy with import * so keep an eye on it
from pybgrx.constants import *
from pybgrx.base import *

# play screen =====================================================================================================

class CutForDealMode(Mode):
    def setup(self):
        self.add_textures("background", [arcade.load_texture("pybgrx_assets/CribbageBoardBackground.png")])

        # HERE put in a deck of cards, yes? TODO replace this with new_game and all the stuff
        self.deck = self.get_parent().gamestate.shuffle()

        # on enter we have not cut any cards
        self.player1_card_cut = False
        self.player2_card_cut = False

        # then some peg sprites! Would be nice not to have to copy this everywhere. REFACTOR
        peg_textures = arcade.load_spritesheet("pybgrx_assets/Pegs.png",sprite_width=9,sprite_height=9,
                                                columns=8,count=8)
        self.add_textures("pegs",peg_textures)

        peg_list = arcade.SpriteList()
        peg_sprites = []       # for keeping track of each player's front and back peg
        peg_colors = [1,7]          # hardcoded orange and pink
        peg_positions = [[[182,141],[121, 141]],[[207,125],[45,125]]]
        for plnum in range(0,2):          # each player's pegs = list of 2 sprites, peg_sprites = list of those lists
            peg_sprites.append([])
            # argh we need a dummy peg to load for this until I figure out how to get None filename constructed
            # sprites to work, which might be never, bc this is a prototype
            # two pegs per player
            for j in range(0,2):
                newpeg = Peg("pybgrx_assets/GreenPeg.png",scale=SPRITE_SCALING)
                newpeg.append_texture(peg_textures[peg_colors[plnum]])  # swh
                newpeg.set_texture(1)
                newpeg.left = peg_positions[plnum][j][0] * SCALE_FACTOR
                newpeg.bottom = peg_positions[plnum][j][1] * SCALE_FACTOR
                peg_sprites[plnum].append(newpeg)
                peg_list.append(newpeg)
        self.add_sprite_list("pegs",peg_list,peg_sprites)

        # sprite for big long streak of 50 card backs
        cards_list = arcade.SpriteList(is_static=True)
        newcards = Generic("pybgrx_assets/DeckCut-50cards.png",scale=SPRITE_SCALING)
        newcards.left = CARD_CUTDL_LEFT_MARGIN
        newcards.bottom = CARD_CUTDL_BOTTOM_MARGIN
        cards_list.append(newcards)
        self.add_sprite_list("stack",cards_list,[newcards])

        # sprites for rail for arrow to slide along - also little extender for before one card is cut
        rail_list = arcade.SpriteList(is_static=True)
        newrail = Generic("pybgrx_assets/DeckCut-ArrowRail.png",scale=SPRITE_SCALING)
        newrail.left = SLIDER_CUTDL_LEFT_MARGIN
        newrail.bottom = SLIDER_CUTDL_BOTTOM_MARGIN
        rail_list.append(newrail)
        newrailext = Generic("pybgrx_assets/DeckCut-ArrowRailExtender.png",scale=SPRITE_SCALING)
        newrailext.left = SLIDEREXT_CUTDL_LEFT_MARGIN
        newrailext.bottom = SLIDER_CUTDL_BOTTOM_MARGIN
        rail_list.append(newrailext)
        self.add_sprite_list("rail",rail_list,[newrail,newrailext])

        # arrow sprite - it will move
        arrow_list = arcade.SpriteList(is_static=False)
        newarrow = Generic("pybgrx_assets/StarterCutArrow.png",scale=SPRITE_SCALING)
        # try putting it in the middle
        # self.arrow_position is the arrow's position in cards i.e. widths of card showing in the stack
        self.arrow_position = 16
        # also it is not in motion
        self.arrow_motion = 0
        # also once it is in motion it needs some ticks before it moves
        self.arrow_move_tick_counter = ARROW_CUTDL_TICKS_PER_MOVE
        # if player presses enter/action before moving the arrow, it hops to a random spot and picks a card
        self.arrow_has_been_moved = False
        newarrow.center_x = SLIDER_CUTDL_LEFT_MARGIN + (self.arrow_position * ARROW_CUTDL_CARD_STRIDE)
        newarrow.bottom = ARROW_CUTDL_BOTTOM_MARGIN
        arrow_list.append(newarrow)
        self.add_sprite_list("arrow",arrow_list,[newarrow])

        # highlight showing which card the arrow is pointing at
        cardhighlight_list = arcade.SpriteList(is_static=False)
        newchl = Generic("pybgrx_assets/DeckCutCardHighlight.png",scale=SPRITE_SCALING)
        newchl.left = (SLIDER_CUTDL_LEFT_MARGIN + (self.arrow_position * ARROW_CUTDL_CARD_STRIDE)) - \
                      CARDHL_CUTDL_ARROWCTR_OFFSET
        newchl.bottom = CARD_CUTDL_BOTTOM_MARGIN + CARDHL_CUTDL_BOTTOM_OFFSET
        cardhighlight_list.append(newchl)
        self.add_sprite_list("cardhighlight",cardhighlight_list,[newchl])

        # turned-up cards
        card_textures = arcade.load_spritesheet("pybgrx_assets/CardDeck.png",sprite_width=CARD_WIDTH,
                                                sprite_height=CARD_HEIGHT,columns=4,count=52)
        self.add_textures("cards",card_textures)
        # make two cards, backs-up and at the two rightmost positions to start
        # TODO TEMP MAKE THEM FACE UP SO YOU CAN SEE THEM
        newupcards = []
        newupcards_list = arcade.SpriteList(is_static=False)
        for j in range(2):
            newupcard = Card("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING)
            for t in range(52):
                newupcard.append_texture(card_textures[t])  # swh
            # TODO TEMP set texture to a real card
            newupcard.set_texture(1+j)
            # put at the right end of the deck
            newupcard.left = CARD_CUTDL_LEFT_MARGIN  + (ARROW_CUTDL_CARD_STRIDE * (50+j))
            newupcard.bottom = CARD_CUTDL_BOTTOM_MARGIN
            newupcards_list.append(newupcard)
            newupcards.append(newupcard)
        self.add_sprite_list("upcards",newupcards_list,newupcards)

    # the way I'm handling motion isn't cricket according to how you're supposed to do it with arcade - but
    # I really want an on_key_held_down but they don't have it. That's more arduiny
    # so what I do is just note that the arrow is in motion. I don't want it to move every frame,
    # ...or at least I don't want it to have to move every frame. I'm thinking a controllable speed, clicky from one
    # card to the next in the stack, so I'll do it in on_tick, hopework.
    def on_key_press(self, key, modifiers):
        # once a card has been cut, stop taking moves
        # TODO: THIS IS A HOLDOVER FROM STARTERCUT - IRL one of the players will be the random computer
        # let's say human always goes first - but we'll get to that later
        if self.player1_card_cut == False and self.player2_card_cut == False:
            if key == arcade.key.RIGHT:
                self.arrow_motion = 1
                self.arrow_has_been_moved = True
            elif key == arcade.key.LEFT:
                self.arrow_motion = -1
                self.arrow_has_been_moved = True
        else:
            self.arrow_motion = 0

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.parent.set_nextmode_index(5)

        # TODO holdover from cutstarter - need to implement this - first player is human, chooses a card, second
        # TODO is computer, handled in on_tick or something
        # elif key == arcade.key.ENTER:
        #     if self.card_cut == False:
        #         # note that we've cut a card! and stop arrow!
        #         self.card_cut = True
        #         self.arrow_motion = 0
        #
        #         # if the arrow hasn't been moved, pick a random card
        #         # for now, jump-cut, can do fancy in real game or later in this
        #         if self.arrow_has_been_moved == False:
        #             self.position_arrow(self.parent.gamestate.random_at_most(ARROW_CUTDL_MAX_POSITION))
        #
        #         # choose the current card! the 4 is there bc if arrow position is 0, 4 cards are to its left by the
        #         # RULES
        #         self.deck = self.parent.gamestate.cut(self.deck,4+self.arrow_position)
        #         (self.deck,cutcard) = self.parent.gamestate.deal_card(self.deck)
        #         print("Cut card value is",cutcard)
        #         sl_upcard = self.get_sprite_list_by_name("upcard")
        #         upcard_list = arcade.SpriteList()
        #         # grab the upcard and set its texture to the value of the cut card (plus one to skip the back, yes?)
        #         upcard_sprite = sl_upcard["sprites"][0]
        #         upcard_sprite.set_texture(1+cutcard)
        #         # set position center to same as arrow center, swh - kludgy copy of calculation for arrow center so don't
        #         # have to fetch arrow sprite list, etc. Will break if the calculation for arrow center x changes
        #         # (see on_tick below)
        #         upcard_sprite.center_x = SLIDER_CUTDL_LEFT_MARGIN + (self.arrow_position * ARROW_CUTDL_CARD_STRIDE)
        #         upcard_sprite.bottom = CARD_CUTDL_BOTTOM_MARGIN
        #         print("Upcard sprite position = (",upcard_sprite.center_x,",",upcard_sprite.bottom,")")
        #         upcard_sprite.set_visible(True)
        #         upcard_list.append(upcard_sprite)
        #         self.replace_sprite_list_by_name("upcard",upcard_list,sl_upcard["sprites"])
        elif key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.arrow_motion = 0

    def position_arrow(self,newpos):
        self.arrow_position = newpos
        arrow_list = self.get_sprite_list_by_name("arrow")
        arrow_sprite = arrow_list["sprites"][0]
        cardhighlight_list = self.get_sprite_list_by_name("cardhighlight")
        cardhighlight_sprite = cardhighlight_list["sprites"][0]
        if self.arrow_position < 0:
            self.arrow_position = 0
        elif self.arrow_position > ARROW_CUTDL_MAX_POSITION:
            self.arrow_position = ARROW_CUTDL_MAX_POSITION
        arrow_sprite.center_x = SLIDER_CUTDL_LEFT_MARGIN + (self.arrow_position * ARROW_CUTDL_CARD_STRIDE)
        cardhighlight_sprite.left = (SLIDER_CUTDL_LEFT_MARGIN + (self.arrow_position * ARROW_CUTDL_CARD_STRIDE)) - \
                                    CARDHL_CUTDL_ARROWCTR_OFFSET
        # do I need to do this? not building a new list
        # self.replace_sprite_list_by_name("cardhighlight", cardhighlight_list["SpriteList"], cardhighlight_list["sprites"])
        # self.replace_sprite_list_by_name("arrow", arrow_list["SpriteList"], arrow_list["sprites"])

    def on_tick(self,delta_time):
        #print("delta_time is ",delta_time)
        # so here is where we update the arrow
        self.arrow_move_tick_counter -= 1       # was delta_time but let's just call everything 1 tick
        if self.arrow_move_tick_counter <= 0:
            # reset tick counter
            self.arrow_move_tick_counter = ARROW_CUTDL_TICKS_PER_MOVE
            # move arrow and card highlight if able to move
            if self.arrow_motion != 0:
                self.position_arrow(self.arrow_position + self.arrow_motion)


    def on_leave(self):
        self.arrow_motion = 0

    def on_resume(self):
        # should we just re-setup? TODO revisit when real game is here
        # no, don't do this, we get two sets of the sprites
        #self.setup()
        # instead, just reset things...? We don't really need this to work right bc it's not the real game
        # parent will have smarter setup code
        self.player1_card_cut = False
        self.player2_card_cut = False
        # TODO FIGURE OUT HOW TO HANDLE UPCARDS - SEE SETUP
        sl_upcards = self.get_sprite_list_by_name("upcards")
        print("sl_upcards is:",sl_upcards)
        # if sl_upcards is not None:
        #     for j in range(2):
        #         upcards_sprite = sl_upcards["sprites"][j]
        #         #upcards_sprite.set_visible(False)
        #     self.replace_sprite_list_by_name("upcards", None, sl_upcards["sprites"])
        self.deck = self.get_parent().gamestate.shuffle()
