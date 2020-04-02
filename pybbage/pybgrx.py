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


# original:
#SCREEN_WIDTH = 800
#SCREEN_HEIGHT = 600

# changing to use a background image: cribbage board mockup 3, for now.
# kept in pybgrx_assets/CribbageBoardBackground.png which is 320x240, intended for arduino.
# hence,
BG_WIDTH = 320
BG_HEIGHT = 240

# for shewing on pc, scale up by a factor of 3 in each dimension (later settable)
# for a total of 960x720, which should fit on my ancient laptop's screen OK.
# nah let's try 2, 640 x 480
SCALE_FACTOR = 2

SCREEN_WIDTH = (BG_WIDTH * SCALE_FACTOR)
SCREEN_HEIGHT = (BG_HEIGHT * SCALE_FACTOR)
SCREEN_TITLE = "Fifteen Two and The Rest Is Poo"

SPRITE_SCALING = 1.0 * SCALE_FACTOR

# for screen arrangement, in pixels.
CARD_SHOW_LEFT_MARGIN = (22 * SCALE_FACTOR)
CARD_SHOW_INTERCARD_MARGIN = (3 * SCALE_FACTOR)
CARD_WIDTH = (41 * SCALE_FACTOR)                # hm
# need to figure out how to handle arcade's backwards y coordinates - yeah, I SAID IT
CARD_SHOW_BOTTOM_MARGIN = (38 * SCALE_FACTOR)

# for putting the starter in the middle of the serpentine board
# weird, should be 96 for bottom, not sure what's up bc the other stuff has
CARD_STARTER_BOTTOM = (144 * SCALE_FACTOR)
CARD_STARTER_LEFT = (138 * SCALE_FACTOR)

# for old sprite demo
MOVEMENT_SPEED = 5


class Player(arcade.Sprite):

    def update(self):
        self.left += self.change_x
        self.top += self.change_y
        #self.center_x += self.change_x
        #self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

# for cards - stub for the moment
# TODO: add stuff for highlight, whatever else a card needs to have
class Card(arcade.Sprite):

    # currently not much needs to be done
    def update(self):
        pass

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

        # from bg image demo
        # Background image will be stored in this variable
        self.background = None

        # Variables that will hold sprite lists
        self.player_list = None
        #self.coin_list = None

        # Set up the player info
        self.player_sprite = None
        #self.score = 0
        #self.score_text = None

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Load the background image. Do this in the setup so we don't keep reloading it all the time.
        # Image from:
        # http://wallpaper-gallery.net/single/free-background-images/free-background-images-22.html
        # self.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")
        self.background = arcade.load_texture("pybgrx_assets/CribbageBoardBackground.png")      # hopework

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Set up the player - let's try a king of hearts
        self.player_sprite = Player("pybgrx_assets/KingHorts.png", SPRITE_SCALING)
        # let us reckon from left and top
        self.player_sprite.left = 0
        self.player_sprite.top = self.player_sprite.height
        #self.player_sprite.center_x = 50
        #self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # then let's make some stationary card sprites for where I think they might be in the real game
        # normal list of them to be able to access each and change things - do we need it?
        self.card_list = arcade.SpriteList(is_static = True)
        self.card_sprites = []
        # so let's do 4 cards and a starter, say, and see what we get trying to use pixels
        # just take a swing, say 22 pixels in
        for j in range(4):
            # TODO get all the card images made into sprites - but for mockups, kinghorts
            newcard = Card("pybgrx_assets/KingHorts.png", SPRITE_SCALING)
            newcard.left = CARD_SHOW_LEFT_MARGIN + (j * (CARD_WIDTH + CARD_SHOW_INTERCARD_MARGIN))
            newcard.bottom = CARD_SHOW_BOTTOM_MARGIN
            self.card_sprites.append(newcard)
            self.card_list.append(newcard)
        # then the starter card
        newcard = Card("pybgrx_assets/KingHorts.png", SPRITE_SCALING)
        newcard.left = CARD_STARTER_LEFT
        newcard.bottom = CARD_STARTER_BOTTOM
        self.card_sprites.append(newcard)
        self.card_list.append(newcard)


    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the background texture
        # TODO find out if there's a way to do this unsmoothed
        scale = SCREEN_WIDTH / self.background.width
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        # Draw all the sprites. Let's try a filter of gl.GL_NEAREST to avoid smoothing.
        # for which you need pyglet.gl imported as gl
        # card_list
        self.card_list.draw(filter = gl.GL_NEAREST)

        # player_list
        self.player_list.draw(filter = gl.GL_NEAREST)


    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    """ Main method """
    print("HEY welcome to pybgrx")
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
