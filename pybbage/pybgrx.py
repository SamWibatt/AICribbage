# PYBGRX.PY - graphic interface to pybbage
# using "arcade" library from https://arcade.academy/index.html
#
# Purpose:
# To experiment and develop a graphical cribbage game that can be ported to small systems like Arduino / 320x240 LCD
# And possibly to fancy glossy version like Gold Fish 3 but for cribbage

# basing this on the sprite_move_keyboard.py example, will just hack up from there

"""
Move Sprite With Keyboard

Simple program to show moving a sprite with the keyboard.
The sprite_move_keyboard_better.py example is slightly better
in how it works, but also slightly more complex.

Artwork from http://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_keyboard
"""

# then extended with background functionality from
# https://arcade.academy/examples/sprite_collect_coins_background.html#sprite-collect-coins-background



import arcade
import os
import pyglet.gl as gl
# then my actual game mechanics!
from pyb import pybbage as pyb

# not happy with import * so keep an eye on it
from pybgrx.constants import *
from pybgrx.base import *
from pybgrx.shewmode import ShewMode
from pybgrx.titlemode import TitleMode
from pybgrx.playmode import PlayMode
from pybgrx.cutstartermode import CutStarterMode
from pybgrx.cutfordealmode import CutForDealMode
from pybgrx.dealmode import DealMode


# *********************************************************************************************************************
# PYBGRX PLAYER OBJECTS
# *********************************************************************************************************************

class PybgrxHumanPlayer(pyb.HumanPlayer):
    def advance_peg_by_score_callback(self,score):
        # OVERRIDE to do graphics of peg advancement, given a total score (for shew)
        print("Advance peg by score callback",score)
        pass

    # this is used by play, and every scoring combination of cards in play is a contiguous set including the
    # newly played card. so if num_cards is 1, the top card is highlighted, on up to e.g. run of 4, highlight
    # 4 cards, top and 3 preceding.
    def advance_peg_by_index_callback(self,score_index,num_cards):
        # OVERRIDE to do graphics of peg advancement, given a score index (for play)
        print("Advance peg by index callback",self.parent.scoreStringsNPoints[score_index][0],"for",
              self.parent.scoreStringsNPoints[score_index][1],"including this many cards:",num_cards)
        pass

class PybgrxComputerPlayer(pyb.PlayFirstLegalCardPlayer):
    def advance_peg_by_score_callback(self,score):
        # OVERRIDE to do graphics of peg advancement, given a total score (for shew)
        print("Advance peg by score callback",score)
        pass

    # this is used by play, and every scoring combination of cards in play is a contiguous set including the
    # newly played card. so if num_cards is 1, the top card is highlighted, on up to e.g. run of 4, highlight
    # 4 cards, top and 3 preceding.
    def advance_peg_by_index_callback(self,score_index,num_cards):
        # OVERRIDE to do graphics of peg advancement, given a score index (for play)
        print("Advance peg by index callback",self.parent.scoreStringsNPoints[score_index][0],"for",
              self.parent.scoreStringsNPoints[score_index][1],"including this many cards:",num_cards)
        pass


# *********************************************************************************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
# MAIN CLASS
# *********************************************************************************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)


        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # no current mode or next
        self.curmode_index = 0
        self.nextmode_index = -1
        self.curmode = None

        # no gamestate yet
        self.gamestate = None

    def setup(self):
        """ Set up the game and initialize the variables. """

        # so here's our game state!
        # ugh, players need a parent pybbage object, which would be the one we're creating with the players in
        # its init params. So, set their parents to none and use the accessor to set them later.
        # GROSS. seat of the pants design, ew
        # It would likely be better to organize it so that Pybbage is the parent and the GUI / console output
        # handler is the child - but bull on here
        randseed = 1043685
        self.player0 = PybgrxHumanPlayer(None,name="You")
        self.player1 = PybgrxComputerPlayer(None,"Me")
        self.gamestate = pyb.Pybbage(randseed, player0 = self.player0, player1 = self.player1)
        # hopework! I assume this will affect the object off in gamestate
        self.player0.set_parent(self.gamestate)
        self.player1.set_parent(self.gamestate)

        self.modes = []
        titlemode = TitleMode(parent = self)
        titlemode.setup()
        self.modes.append(titlemode)     # mode 0: title
        shewmode = ShewMode(parent = self)
        shewmode.setup()
        self.modes.append(shewmode)      # mode 1: (though later another) shew
        playmode = PlayMode(parent=self)
        playmode.setup()
        self.modes.append(playmode)      # mode 2: (though later another) play
        cutstmode = CutStarterMode(parent=self)
        cutstmode.setup()
        self.modes.append(cutstmode)     # mode 3: (though later another) cut for starter
        cutdlmode = CutForDealMode(parent=self)
        cutdlmode.setup()
        self.modes.append(cutdlmode)     # mode 4: (though later another) cut for deal
        dealmode = DealMode(parent=self)
        dealmode.setup()
        self.modes.append(dealmode)     # mode 5: (though later another) deal incl pone cut

        self.curmode_index = 0
        self.curmode = self.modes[self.curmode_index]   # start at mode 0

        # set up the "tick" timer which in real thing will be a 1/50s or so interrupt
        arcade.schedule(self.on_tick, TICK_LENGTH)


    def set_nextmode_index(self,nextmode_index):
        # for letting this object know the current mode is ready to switch to another
        self.nextmode_index = nextmode_index

    def get_gamestate(self):
        return self.gamestate

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        if self.curmode is not None:
            self.curmode.on_draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # MAYBE MOVE THIS INTO A SEPARATE FUNCTION THAT RUNS ON A SCHEDULE OF LIKE 1/20 of a second ===================
        # although the website docs suggest this is a good place to do it - note that delta_time there
        #
        # on_update(delta_time: float)[source]
        #     Move everything. Perform collision checks. Do all the game logic here.
        #     Parameters
        #         delta_time (float) – Time interval since the last time the function was called.

        # check for a new mode
        if self.nextmode_index != -1:
            if self.nextmode_index >= 0 and self.nextmode_index < len(self.modes):
                # stand down current mode
                self.curmode.on_leave()

                self.curmode_index = self.nextmode_index
                self.curmode = self.modes[self.curmode_index]

                # do whatever's needed on restarting this mode
                self.curmode.on_resume()
            else:
                print("Illegal nextmode index:",self.nextmode_index,"setting to -1")
            self.nextmode_index = -1            # silent fail if illegal next index

        if self.curmode is not None:
            self.curmode.on_update(delta_time)
        # MAYBE MOVE THIS INTO A SEPARATE FUNCTION THAT RUNS ON A SCHEDULE OF LIKE 1/20 of a second ===================
        # ektully that'll be 1/50, I think, and that's on_tick

    def on_tick(self,delta_time):
        if self.curmode is not None:
            self.curmode.on_tick(delta_time)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if self.curmode is not None:
            self.curmode.on_key_press(key,modifiers)


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if self.curmode is not None:
            self.curmode.on_key_release(key,modifiers)


def main():
    """ Main method """
    print("HEY welcome to pybgrx")
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
