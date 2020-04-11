import arcade
import os
import pyglet.gl as gl
# then my actual game mechanics!
from pyb import pybbage as pyb

# not happy with import * so keep an eye on it
from pybgrx.constants import *
from pybgrx.base import *

# title screen ====================================================================================================

class TitleMode(Mode):
    def setup(self):
        self.add_textures("background", [arcade.load_texture("pybgrx_assets/PybbageTitleScreen.png")])

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.parent.set_nextmode_index(1)

