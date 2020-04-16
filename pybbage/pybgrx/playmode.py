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

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.parent.set_nextmode_index(1)

