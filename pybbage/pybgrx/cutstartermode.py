# cut for starter card mode!

import arcade
import os
import pyglet.gl as gl
# then my actual game mechanics!
from pyb import pybbage as pyb

# not happy with import * so keep an eye on it
from pybgrx.constants import *
from pybgrx.base import *

# play screen =====================================================================================================

class CutStarterMode(Mode):
    def setup(self):
        self.add_textures("background", [arcade.load_texture("pybgrx_assets/CribbageBoardBackground.png")])

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

        # sprite for big long streak of 40 card backs
        cards_list = arcade.SpriteList(is_static=True)
        newcards = Generic("pybgrx_assets/StarterCut-40cards.png",scale=SPRITE_SCALING)
        newcards.left = CARD_CUTST_LEFT_MARGIN
        newcards.bottom = CARD_CUTST_BOTTOM_MARGIN
        cards_list.append(newcards)
        self.add_sprite_list("cards",cards_list,[newcards])

        # sprite for rail for arrow to slide along
        rail_list = arcade.SpriteList(is_static=True)
        newrail = Generic("pybgrx_assets/StarterCut-ArrowRail.png",scale=SPRITE_SCALING)
        newrail.left = SLIDER_CUTST_LEFT_MARGIN
        newrail.bottom = SLIDER_CUTST_BOTTOM_MARGIN
        rail_list.append(newrail)
        self.add_sprite_list("rail",rail_list,[newrail])
        
        # arrow sprite - it will move
        arrow_list = arcade.SpriteList(is_static=False)
        newarrow = Generic("pybgrx_assets/StarterCutArrow.png",scale=SPRITE_SCALING)
        # try putting it in the middle
        # self.arrow_position is the arrow's position in cards i.e. widths of card showing in the stack
        self.arrow_position = 16;
        newarrow.center_x = ARROW_CUTST_MIN_CENTER_X + (self.arrow_position * ARROW_CUTST_CARD_STRIDE)
        newarrow.bottom = ARROW_CUTST_BOTTOM_MARGIN
        arrow_list.append(newarrow)
        self.add_sprite_list("arrow",arrow_list,[newarrow])

        # highlight showing which card the arrow is pointing at
        cardhighlight_list = arcade.SpriteList(is_static=False)
        newchl = Generic("pybgrx_assets/StarterCutCardHighlight.png",scale=SPRITE_SCALING)
        newchl.left = (ARROW_CUTST_MIN_CENTER_X + (self.arrow_position * ARROW_CUTST_CARD_STRIDE)) - \
                      CARDHL_CUTST_ARROWCTR_OFFSET
        newchl.bottom = CARD_CUTST_BOTTOM_MARGIN + CARDHL_CUTST_BOTTOM_OFFSET
        cardhighlight_list.append(newchl)
        self.add_sprite_list("cardhighlight",cardhighlight_list,[newchl])


    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.parent.set_nextmode_index(0)
