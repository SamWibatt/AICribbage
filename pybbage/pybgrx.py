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
SCREEN_TITLE = "Hello and welcome to PYBBAGE"

SPRITE_SCALING = 1.0 * SCALE_FACTOR

# for screen arrangement, in pixels.
CARD_SHOW_LEFT_MARGIN = (21 * SCALE_FACTOR)
CARD_SHOW_INTERCARD_MARGIN = (3 * SCALE_FACTOR)
CARD_WIDTH = (41 * SCALE_FACTOR)                # hm
# need to figure out how to handle arcade's backwards y coordinates - yeah, I SAID IT
CARD_SHOW_BOTTOM_MARGIN = (29 * SCALE_FACTOR)

# highlight offset from card left/bottom
HIGHLIGHT_WIDTH = (3*SCALE_FACTOR)

# for putting the starter to the right of the board
CARD_STARTER_BOTTOM = (153 * SCALE_FACTOR)
CARD_STARTER_LEFT = (265 * SCALE_FACTOR)

# left, bottom coords for all the holes in the cribbage board
# TODO add starter and finish holes
# list of 2 - outer lists are per player, player 0 gets the row that is at the top at start and end,
# player 1 gets the other
# entries are tuple of left, bottom for drawing a peg there
# maybe not perfect but wev
hole_positions = [
    [
        [ 11, 204],  #  1 and # 61 - all holes are n and 60+n bc twice around
        [ 23, 204],  #  2
        [ 35, 204],  #  3
        [ 47, 204],  #  4
        [ 59, 204],  #  5
        [ 73, 204],  #  6
        [ 85, 204],  #  7
        [ 97, 204],  #  8
        [109, 204],  #  9
        [121, 204],  # 10

        [134, 204],  # 11
        [146, 204],  # 12
        [158, 204],  # 13
        [170, 204],  # 14
        [182, 204],  # 15
        [195, 204],  # 16
        [210, 204],  # 17
        [224, 203],  # 18
        [236, 198],  # 19
        [242, 187],  # 20

        [242, 175],  # 21
        [236, 164],  # 22
        [224, 158],  # 23
        [210, 157],  # 24
        [195, 157],  # 25
        [182, 157],  # 26
        [170, 157],  # 27
        [158, 157],  # 28
        [146, 157],  # 29
        [134, 157],  # 30

        [121, 157],  # 31
        [109, 157],  # 32
        [ 97, 157],  # 33
        [ 85, 157],  # 34
        [ 73, 157],  # 35
        [ 60, 157],  # 36
        [ 52, 157],  # 37
        [ 44, 157],  # 38
        [ 36, 157],  # 39
        [ 28, 155],  # 40

        [ 28, 143],  # 41
        [ 36, 141],  # 42
        [ 44, 141],  # 43
        [ 52, 141],  # 44
        [ 60, 141],  # 45
        [ 73, 141],  # 46
        [ 85, 141],  # 47
        [ 97, 141],  # 48
        [109, 141],  # 49
        [121, 141],  # 50

        [134, 141],  # 51
        [146, 141],  # 52
        [158, 141],  # 53
        [170, 141],  # 54
        [182, 141],  # 55
        [195, 141],  # 56
        [207, 141],  # 57
        [219, 141],  # 58
        [231, 141],  # 59
        [243, 141],  # 60
    ],
    [
        [ 11, 189],  #  1 and # 61 - all holes are n and 60+n bc twice around
        [ 23, 189],  #  2
        [ 35, 189],  #  3
        [ 47, 189],  #  4
        [ 59, 189],  #  5
        [ 73, 189],  #  6
        [ 85, 189],  #  7
        [ 97, 189],  #  8
        [109, 189],  #  9
        [121, 189],  # 10

        [134, 189],  # 11
        [146, 189],  # 12
        [158, 189],  # 13
        [170, 189],  # 14
        [182, 189],  # 15
        [195, 189],  # 16
        [203, 189],  # 17
        [211, 189],  # 18
        [219, 189],  # 19
        [227, 187],  # 20

        [227, 175],  # 21
        [219, 173],  # 22
        [211, 173],  # 23
        [203, 173],  # 24
        [195, 173],  # 25
        [182, 173],  # 26
        [170, 173],  # 27
        [158, 173],  # 28
        [146, 173],  # 29
        [134, 173],  # 30

        [121, 173],  # 31
        [109, 173],  # 32
        [ 97, 173],  # 33
        [ 85, 173],  # 34
        [ 73, 173],  # 35
        [ 59, 173],  # 36
        [ 45, 173],  # 37
        [ 31, 172],  # 38
        [ 19, 166],  # 39
        [ 12, 155],  # 40

        [ 12, 143],  # 41
        [ 19, 132],  # 42
        [ 31, 126],  # 43
        [ 45, 125],  # 44
        [ 60, 125],  # 45
        [ 73, 125],  # 46
        [ 85, 125],  # 47
        [ 97, 125],  # 48
        [109, 125],  # 49
        [121, 125],  # 50

        [134, 125],  # 51
        [146, 125],  # 52
        [158, 125],  # 53
        [170, 125],  # 54
        [182, 125],  # 55
        [195, 125],  # 56
        [207, 125],  # 57
        [219, 125],  # 58
        [231, 125],  # 59
        [243, 125],  # 60
    ]
]

# for old sprite demo
MOVEMENT_SPEED = 3


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

# for highlighs - stub for the moment
# TODO: add stuff for enabled whatever else a highlight needs to have
class Highlight(arcade.Sprite):

    # currently not much needs to be done
    def update(self):
        pass

# for pegs - stub for the moment
# TODO: add stuff for whatever else a peg needs to have
class Peg(arcade.Sprite):

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
        # would this work for loading the whole set of them?
        # https://arcade.academy/_modules/arcade/texture.html#load_spritesheet
        # was self.player_sprite = Player("pybgrx_assets/CardBack.png", SPRITE_SCALING)
        # arcade.load_spritesheet(file_name: str, sprite_width: int, sprite_height: int, columns: int, count: int)
        # → List[source]
        # it totally works!
        # temp, make it a peg so we can reckon all the hole positions
        # then make a highlight
        card_textures = arcade.load_spritesheet("pybgrx_assets/CardDeck.png",sprite_width=41,sprite_height=64,
                                                columns=13,count=52)
        self.player_sprite = Player("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING)
        self.player_sprite.left = 18 * SCALE_FACTOR
        self.player_sprite.bottom = 26 * SCALE_FACTOR
        #self.player_sprite.center_x = 50
        #self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # then some peg sprites!
        peg_textures = arcade.load_spritesheet("pybgrx_assets/Pegs.png",sprite_width=9,sprite_height=9,
                                                columns=8,count=8)
        self.peg_list = arcade.SpriteList()
        self.peg_sprites = []       # for keeping track of each player's front and back peg
        peg_colors = [1,7]          # hardcoded orange and pink
        peg_positions = [[[182,141],[121, 141]],[[207,125],[45,125]]]
        for plnum in range(0,2):          # each player's pegs = list of 2 sprites, peg_sprites = list of those lists
            self.peg_sprites.append([])
            # argh we need a dummy peg to load for this until I figure out how to get None filename constructed
            # sprites to work, which might be never, bc this is a prototype
            # two pegs per player
            for j in range(0,2):
                newpeg = Peg("pybgrx_assets/GreenPeg.png",scale=SPRITE_SCALING)
                newpeg.append_texture(peg_textures[peg_colors[plnum]])  # swh
                newpeg.set_texture(1)
                newpeg.left = peg_positions[plnum][j][0] * SCALE_FACTOR
                newpeg.bottom = peg_positions[plnum][j][1] * SCALE_FACTOR
                self.peg_sprites[plnum].append(newpeg)
                self.peg_list.append(newpeg)

        # then let's make some stationary card sprites for where I think they might be in the real game
        # normal list of them to be able to access each and change things - do we need it?
        self.card_list = arcade.SpriteList(is_static = True)
        self.card_sprites = []
        # so let's do 4 cards and a starter, say, and see what we get trying to use pixels
        # just take a swing, say 22 pixels in
        # TEMP TEST for 29 hand
        cards = [4,43,30,23,17]  # = 5 of horts, 5s, 5c, Jd, 5d
        for j in range(4):
            # this is a kludge, load a card back sprite to set the image size, then use texture
            newcard = Card("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING)
            newcard.append_texture(card_textures[cards[j]])  # swh
            newcard.set_texture(1)
            newcard.left = CARD_SHOW_LEFT_MARGIN + (j * (CARD_WIDTH + CARD_SHOW_INTERCARD_MARGIN))
            newcard.bottom = CARD_SHOW_BOTTOM_MARGIN
            self.card_sprites.append(newcard)
            self.card_list.append(newcard)
        # then the starter card
        newcard = Card("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING)
        newcard.append_texture(card_textures[cards[4]])  # swh
        newcard.set_texture(1)
        newcard.left = CARD_STARTER_LEFT
        newcard.bottom = CARD_STARTER_BOTTOM
        self.card_sprites.append(newcard)
        self.card_list.append(newcard)

        # highlights - non-moving, just can appear or disappear, find out how to do that
        # may have to do it by moving them offscireen, so I'll say is_static is false. Not like this game is
        # much of a performance hog
        self.highlight_list = arcade.SpriteList(is_static = False)
        self.highlight_sprites = []
        # highlights for all 4 cards and starter (shew version
        for j in range(4):
            # For now there is only one kind of highlight, later can use others like I do with cards and pegs
            newhighlight = Highlight("pybgrx_assets/YellowHighlight.png",scale=SPRITE_SCALING)
            newhighlight.left = (CARD_SHOW_LEFT_MARGIN - HIGHLIGHT_WIDTH) + (j * (CARD_WIDTH + CARD_SHOW_INTERCARD_MARGIN))
            newhighlight.bottom = CARD_SHOW_BOTTOM_MARGIN - HIGHLIGHT_WIDTH
            self.highlight_sprites.append(newhighlight)
            self.highlight_list.append(newhighlight)
        # then the starter highlight
        newhighlight = Highlight("pybgrx_assets/YellowHighlight.png",scale=SPRITE_SCALING)
        newhighlight.left = CARD_STARTER_LEFT - HIGHLIGHT_WIDTH
        newhighlight.bottom = CARD_STARTER_BOTTOM - HIGHLIGHT_WIDTH
        self.highlight_sprites.append(newhighlight)
        self.highlight_list.append(newhighlight)



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
        #dunt work - ,filter = gl.GL_NEAREST)

        # Draw all the sprites. Let's try a filter of gl.GL_NEAREST to avoid smoothing.
        # for which you need pyglet.gl imported as gl
        # card_list
        self.card_list.draw(filter = gl.GL_NEAREST)
        # debug
        #for card in self.card_list.sprite_list:
        #    card.draw_hit_box(color = arcade.YELLOW)

        # then pegs
        self.peg_list.draw(filter = gl.GL_NEAREST)

        # then highlights
        self.highlight_list.draw(filter = gl.GL_NEAREST)

        # player_list
        self.player_list.draw(filter = gl.GL_NEAREST)

        # then for TODO TEMP hole finding print the player's bottom and left.
        # start_x and start_y make the start point for the text. We draw a dot to make it easy too see
        # the text in relation to its start x and y.
        # start_x = self.player_sprite.left + self.player_sprite.width
        # start_y = self.player_sprite.top
        # arcade.draw_point(start_x, start_y, arcade.color.BLUE, 5)
        # pstring = "{},{}".format(self.player_sprite.left // SCALE_FACTOR, self.player_sprite.bottom // SCALE_FACTOR)
        # arcade.draw_text(pstring, start_x, start_y, arcade.color.WHITE, 20)

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
