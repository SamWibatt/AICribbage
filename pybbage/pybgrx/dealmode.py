# deal mode!
# includes pone cut!

import arcade
import os
import pyglet.gl as gl
# then my actual game mechanics!
from pyb import pybbage as pyb

# not happy with import * so keep an eye on it
from pybgrx.constants import *
from pybgrx.base import *


# play screen =====================================================================================================

class DealMode(Mode):
    def setup(self):
        self.add_textures("background", [arcade.load_texture("pybgrx_assets/CribbageBoardBackground.png")])

        # HERE put in a deck of cards, yes? TODO replace this with new_game and all the stuff
        self.deck = self.get_parent().gamestate.shuffle()

        # on enter we have not cut the deck
        self.deck_cut = False

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
        newcards.left = STACK_DEAL_LEFT_MARGIN
        newcards.bottom = STACK_DEAL_BOTTOM_MARGIN
        cards_list.append(newcards)
        self.add_sprite_list("stack",cards_list,[newcards])

        # sprites for rail for arrow to slide along - also little extender for before one card is cut
        rail_list = arcade.SpriteList(is_static=True)
        newrail = Generic("pybgrx_assets/DeckCut-ArrowRail.png",scale=SPRITE_SCALING)
        newrail.left = SLIDER_DEAL_LEFT_MARGIN
        newrail.bottom = SLIDER_DEAL_BOTTOM_MARGIN
        rail_list.append(newrail)
        newrailext = Generic("pybgrx_assets/DeckCut-ArrowRailExtender.png",scale=SPRITE_SCALING)
        newrailext.left = SLIDEREXT_DEAL_LEFT_MARGIN
        newrailext.bottom = SLIDER_DEAL_BOTTOM_MARGIN
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
        self.arrow_move_tick_counter = ARROW_DEAL_TICKS_PER_MOVE
        # if player presses enter/action before moving the arrow, it hops to a random spot and picks a card
        self.arrow_has_been_moved = False
        newarrow.center_x = SLIDER_DEAL_LEFT_MARGIN + (self.arrow_position * ARROW_DEAL_CARD_STRIDE)
        newarrow.bottom = ARROW_DEAL_BOTTOM_MARGIN
        arrow_list.append(newarrow)
        self.add_sprite_list("arrow",arrow_list,[newarrow])

        # highlight showing which card the arrow is pointing at
        cardhighlight_list = arcade.SpriteList(is_static=False)
        newchl = Generic("pybgrx_assets/DealCutCardHighlight.png",scale=SPRITE_SCALING)
        newchl.left = (SLIDER_DEAL_LEFT_MARGIN + (self.arrow_position * ARROW_DEAL_CARD_STRIDE)) - \
                      STACKHL_DEAL_ARROWCTR_OFFSET
        newchl.bottom = STACK_DEAL_BOTTOM_MARGIN + STACKHL_DEAL_BOTTOM_OFFSET
        cardhighlight_list.append(newchl)
        self.add_sprite_list("cardhighlight",cardhighlight_list,[newchl])

        # turned-up cards TODO Deal only has 1 - actually, none, just cutting the deck
        card_textures = arcade.load_spritesheet("pybgrx_assets/CardDeck.png",sprite_width=CARD_WIDTH,
                                                sprite_height=CARD_HEIGHT,columns=4,count=52)
        self.add_textures("cards",card_textures)
        # make two cards, backs-up and at the two rightmost positions to start
        # ...although we do need those last 2 card backs
        newendcards = []
        newendcards_list = arcade.SpriteList(is_static=False)
        for j in range(2):
            newendcard = Card("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING) 
            # put at the right end of the deck
            newendcard.left = STACK_DEAL_LEFT_MARGIN  + (ARROW_DEAL_CARD_STRIDE * (50+j))
            newendcard.bottom = STACK_DEAL_BOTTOM_MARGIN
            newendcards_list.append(newendcard)
            newendcards.append(newendcard)
        self.add_sprite_list("endcards",newendcards_list,newendcards)

        # cards dealt to player after deck is cut
        # initially invisible though TODO that isn't enforced until I write an on_draw
        card_list = arcade.SpriteList(is_static = True)
        card_sprites = []

        for j in range(6):
            # this is a kludge, load a card back sprite to set the image size, then use texture
            newcard = Card("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING, visible=False)
            for t in range(52):
                newcard.append_texture(card_textures[t])  # swh
            # TODO TEMP set texture to a real card
            newcard.set_texture(2 + (7*j))

            newcard.left = CARD_DEAL_LEFT_MARGIN + (j * (CARD_SCREEN_WIDTH + CARD_DEAL_INTERCARD_MARGIN))
            newcard.bottom = STACK_DEAL_BOTTOM_MARGIN
            card_sprites.append(newcard)
            card_list.append(newcard)
        self.add_sprite_list("cards",card_list,card_sprites)


    # the way I'm handling motion isn't cricket according to how you're supposed to do it with arcade - but
    # I really want an on_key_held_down but they don't have it. That's more arduiny
    # so what I do is just note that the arrow is in motion. I don't want it to move every frame,
    # ...or at least I don't want it to have to move every frame. I'm thinking a controllable speed, clicky from one
    # card to the next in the stack, so I'll do it in on_tick, hopework.
    def on_key_press(self, key, modifiers):
        # once a card has been cut, stop taking moves
        # let's say human always goes first - but we'll get to that later
        if self.deck_cut == False:
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
            self.parent.set_nextmode_index(0)

        elif key == arcade.key.ENTER:
            if self.deck_cut == False:
                # note that we've cut a card! and stop arrow!
                self.deck_cut = True
                self.arrow_motion = 0

                # if the arrow hasn't been moved, pick a random card
                # for now, jump-cut, can do fancy in real game or later in this
                if self.arrow_has_been_moved == False:
                    self.position_arrow(self.parent.gamestate.random_at_most(ARROW_DEAL_MAX_POSITION))
                # TODO here switch to the mode that shows the cards actually being dealt -
                # really should have some cool animation of the deck cutting and cards twirling to their
                # spots, but wev.
                # TODO make arrow, rail, rail extension, stack, cardhighlight, and end cards invisible
                # easy way is just to none-out their sprite lists, yes?
                self.replace_sprite_list_by_name("stack", None, None)
                self.replace_sprite_list_by_name("arrow", None, None)
                self.replace_sprite_list_by_name("rail", None, None)
                self.replace_sprite_list_by_name("cardhighlight", None, None)
                self.replace_sprite_list_by_name("endcards", None, None)

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
        elif self.arrow_position > ARROW_DEAL_MAX_POSITION:
            self.arrow_position = ARROW_DEAL_MAX_POSITION
        arrow_sprite.center_x = SLIDER_DEAL_LEFT_MARGIN + (self.arrow_position * ARROW_DEAL_CARD_STRIDE)
        cardhighlight_sprite.left = (SLIDER_DEAL_LEFT_MARGIN + (self.arrow_position * ARROW_DEAL_CARD_STRIDE)) - \
                                    STACKHL_DEAL_ARROWCTR_OFFSET
        # do I need to do this? not building a new list
        # self.replace_sprite_list_by_name("cardhighlight", cardhighlight_list["SpriteList"], cardhighlight_list["sprites"])
        # self.replace_sprite_list_by_name("arrow", arrow_list["SpriteList"], arrow_list["sprites"])

    def on_tick(self,delta_time):
        #print("delta_time is ",delta_time)
        # so here is where we update the arrow
        self.arrow_move_tick_counter -= 1       # was delta_time but let's just call everything 1 tick
        if self.arrow_move_tick_counter <= 0:
            # reset tick counter
            self.arrow_move_tick_counter = ARROW_DEAL_TICKS_PER_MOVE
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
        self.deck_cut = False
        # TODO FIGURE OUT HOW TO HANDLE UPCARDS - SEE SETUP
        sl_upcards = self.get_sprite_list_by_name("upcards")
        print("sl_upcards is:",sl_upcards)
        # if sl_upcards is not None:
        #     for j in range(2):
        #         upcards_sprite = sl_upcards["sprites"][j]
        #         #upcards_sprite.set_visible(False)
        #     self.replace_sprite_list_by_name("upcards", None, sl_upcards["sprites"])
        self.deck = self.get_parent().gamestate.shuffle()
