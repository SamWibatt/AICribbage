# play mode!

import arcade
import os
import pyglet.gl as gl
# then my actual game mechanics!
from pyb import pybbage as pyb

# not happy with import * so keep an eye on it
from pybgrx.constants import *
from pybgrx.base import *

# play screen =====================================================================================================

class PlayMode(Mode):
    def setup(self):
        self.add_textures("background", [arcade.load_texture("pybgrx_assets/CribbageBoardBackground.png")])

        # set up cards. The idea is that the cards pile up from left to right, overlapping.
        # after a "go", the cards so far get turned over to shew card back and keep going from there
        # may not be according to Hoyle, but wevly buckets
        # refer to Cribmock2Count.png -
        # for screen arrangement, in pixels.
        # hand cards to choose from -
        # CARD_PLAY_HAND_LEFT_MARGIN(6 * SCALE_FACTOR)
        # CARD_PLAY_HAND_SPACING(41 * SCALE_FACTOR)
        # # cards in the piled up cards on the right
        # CARD_PLAY_LEFT_MARGIN = (175 * SCALE_FACTOR)
        # CARD_PLAY_BOTTOM_MARGIN = (29 * SCALE_FACTOR)
        # # distance from the left edge of one card to the next, they overlap
        # CARD_PLAY_NEXTCARD_DIST = (21 * SCALE_FACTOR)
        # then let's make some stationary card sprites for where I think they might be in the real game
        # normal list of them to be able to access each and change things - do we need it?
        card_textures = arcade.load_spritesheet("pybgrx_assets/CardDeck.png",sprite_width=CARD_WIDTH,
                                                sprite_height=CARD_HEIGHT,columns=4,count=52)
        self.add_textures("cards",card_textures)

        # 8 cards in the play - later will only draw the ones that have been played, for now do a bunch
        # of card backs
        play_card_list = arcade.SpriteList(is_static = True)
        play_card_sprites = []
        for j in range(8):
            # this is a kludge, load a card back sprite to set the image size, then use texture
            newcard = Card("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING)
            for t in range(52):
                newcard.append_texture(card_textures[t])  # swh
            newcard.left = CARD_PLAY_LEFT_MARGIN + (j * CARD_PLAY_NEXTCARD_DIST)
            newcard.bottom = CARD_PLAY_BOTTOM_MARGIN
            newcard.set_texture(1+ (4*j))   # temp
            play_card_sprites.append(newcard)
            play_card_list.append(newcard)
        self.add_sprite_list("playcards",play_card_list,play_card_sprites)

        # we have 4 cards in the hand
        hand_card_list = arcade.SpriteList(is_static = True)
        hand_card_sprites = []
        for j in range(4):
            # this is a kludge, load a card back sprite to set the image size, then use texture
            newcard = Card("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING)
            for t in range(52):
                newcard.append_texture(card_textures[t])  # swh
            newcard.left = CARD_PLAY_HAND_LEFT_MARGIN + (j * (CARD_SCREEN_WIDTH + CARD_PLAY_INTERCARD_MARGIN))
            newcard.bottom = CARD_PLAY_BOTTOM_MARGIN
            newcard.set_texture(1+ (38 + (4*j)))   # temp
            hand_card_sprites.append(newcard)
            hand_card_list.append(newcard)
        self.add_sprite_list("handcards",hand_card_list,hand_card_sprites)

        # then the deck up in the corner
        deck_list = arcade.SpriteList(is_static=True)
        newcard = Card("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING)
        newcard.left = CARD_DECK_LEFT
        newcard.bottom = CARD_DECK_BOTTOM
        deck_list.append(newcard)
        self.add_sprite_list("deck",deck_list,[newcard])


    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.parent.set_nextmode_index(0)

