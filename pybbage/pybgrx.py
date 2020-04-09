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
    # init adds the highlighted parameter to the regular sprite parameters
    def __init__(self,filename: str = None, scale: float = 1, image_x: float = 0, image_y: float = 0,
                 image_width: float = 0, image_height: float = 0, center_x: float = 0, center_y: float = 0,
                 repeat_count_x: int = 1, repeat_count_y: int = 1,
                 highlighted = False):
        self.highlighted = highlighted
        super().__init__(filename,scale,image_x,image_y,image_width,image_height,center_x,center_y,
                         repeat_count_x,repeat_count_y)

    def set_highlighted(self,highlighted):
        self.highlighted = highlighted

    def is_highlighted(self):
        return self.highlighted

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


# class for containing a "mode" - will see what all gets in there, but I think it's pretty much everything
# that's currently in MyGame - background, sprites, user interface, etc.
# subclass for different game phases like cut for deal, deal, discard, etc.
# so figure out how to refactor the current single screen into
class Mode:

    def __init__(self):
        # self.sprite_lists is a list of dicts like this:
        # {
        #     "name" : name
        #     "SpriteList" : arcade.SpriteList object for rendering,
        #     "sprites": list of the individual sprites in that sprite list
        # }
        # so game logic can look in the "sprites" part to change position, texture, whatever else
        self.sprite_lists = None

        # self.textures is a dict of name to of lists of textures, some of which (like bg texture) might only have
        # one texture in them e.g.
        # {
        #     "background" -> [bg texture],
        #     "cards" -> [ card 0, card 1, card 2, ...],
        #     "pegs" -> [ blue peg, green peg, ...]
        # }
        # this would likely be shared across most or all of the modes
        self.textures = None
        pass

    # accessors ------------------------------------------------------------------------------------------------------

    # self.sprite_lists is a list of dicts like this:
    # {
    #     "name": name
    #     "SpriteList" : arcade.SpriteList object for rendering,
    #     "sprites": list of the individual sprites in that sprite list
    # }
    # so game logic can look in the "sprites" part to change position, texture, whatever else
    # handling it as a list because we want to preserve order of sprite lists, yes?
    def add_sprite_list(self, listname, sprite_list, individual_sprites):
        if self.sprite_lists is None:
            self.sprite_lists = []
        #print("adding sprite list",listname)
        self.sprite_lists.append( { "name": listname, "SpriteList": sprite_list, "sprites": individual_sprites } )


    def get_sprite_list_by_name(self,name):
        # assuming a small number of sprite lists, which there will probably be.
        if self.sprite_lists is None:
            return None
        for sl in self.sprite_lists:
            if sl["name"] == name:
                return sl
        return None

    def get_sprite_list_by_index(self,index):
        if index < 0 or self.sprite_lists is None or index >= len(self.sprite_lists):
            return None
        return self.sprite_lists[index]

    # this lets you overwrite a sprite list while preserving its order
    def replace_sprite_list_by_name(self, listname, sprite_list, individual_sprites):
        if self.sprite_lists is None:
            return
        slist = self.get_sprite_list_by_name(listname)
        if slist is None:
            return
        slist["SpriteList"] = sprite_list
        slist["sprites"] = individual_sprites

    # self.textures is a dict of name to of lists of textures, some of which (like bg texture) might only have
    # one texture in them e.g.
    # {
    #     "background" -> [bg texture],
    #     "cards" -> [ card 0, card 1, card 2, ...],
    #     "pegs" -> [ blue peg, green peg, ...]
    # }
    # this would likely be shared across most or all of the modes
    def add_textures(self, texsetname, texture_list):
        #print("Adding texture set",texsetname)
        if self.textures is None:
            self.textures = {}
        self.textures[texsetname] = texture_list

    def get_textures(self, texsetname):
        if self.textures is None or texsetname not in self.textures:
            #print("textures",texsetname,"is None")
            return None
        return self.textures[texsetname]

    # overrideables --------------------------------------------------------------------------------------------------

    def setup(self):
        pass

    def on_draw(self):
        # draw the bg texture, sprite lists, text, etc.
        # TODO: WRITE DEFAULT VERSION
        pass

    def update_game_logic(self):
        # broken out from on_update so modes can override this without having to duplicate the drawing stuff
        # here, update whatever is relevant for the mode, like animating flying numbers or pegs or whatever
        # aaaand probably calling pybbage logic? Have to think about that. Might happen outside the drawing
        # seems unlikely you'd do heavy thinking in the draw update. TODO LOOK INTO
        pass

    def on_update(self):
        # do game logic callback
        self.update_game_logic()

        # call update on all the sprite lists
        if self.sprite_lists is not None:
            for sl in self.sprite_lists:
                sl["SpriteList"].update()

    def on_key_press(self, key, modifiers):
        # how to handle? maybe a dict of key constant -> member function to handle it?
        # TODO WRITE DEFAULT VERSION if there is anything
        pass

    def on_key_release(self, key, modifiers):
        # how to handle? maybe a dict of key constant -> member function to handle it?
        # TODO WRITE DEFAULT VERSION if there is anything
        pass


class ShewMode(Mode):

    def __init__(self):
        super().__init__()
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

        # clear other lists
        self.card_list = None
        self.card_sprites = None
        self.peg_list = None
        self.peg_sprites = None
        self.highlight_list = None
        self.highlight_sprites = None
        self.highlight_active = None

    def setup(self):
        # Load the background image. Do this in the setup so we don't keep reloading it all the time.
        # Image from:
        # http://wallpaper-gallery.net/single/free-background-images/free-background-images-22.html
        # self.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")
        # note that we need a list of textures in the Mode object, for every texture set
        self.add_textures("background", [arcade.load_texture("pybgrx_assets/CribbageBoardBackground.png")])     # hopework

        # Sprite lists
        # THEY WILL BE DRAWN IN THE ORDER THEY'RE ADDED, SO LAST ONE IS FRONT


        # then some peg sprites!
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

        # then let's make some stationary card sprites for where I think they might be in the real game
        # normal list of them to be able to access each and change things - do we need it?
        card_textures = arcade.load_spritesheet("pybgrx_assets/CardDeck.png",sprite_width=41,sprite_height=64,
                                                columns=13,count=52)
        self.add_textures("cards",card_textures)
        card_list = arcade.SpriteList(is_static = True)
        card_sprites = []
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
            card_sprites.append(newcard)
            card_list.append(newcard)
        # then the starter card
        newcard = Card("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING)
        newcard.append_texture(card_textures[cards[4]])  # swh
        newcard.set_texture(1)
        newcard.left = CARD_STARTER_LEFT
        newcard.bottom = CARD_STARTER_BOTTOM
        card_sprites.append(newcard)
        card_list.append(newcard)

        # set some highlights - TODO debug rip out
        card_sprites[1].set_highlighted(True)
        card_sprites[2].set_highlighted(True)
        card_sprites[4].set_highlighted(True)

        # build initial list of which cards are highlighted - actually init to all false
        self.last_highlighted = [False] * len(card_sprites)

        self.add_sprite_list("cards",card_list,card_sprites)


        # highlights - non-moving, just can appear or disappear, find out how to do that
        # rebuilds the highlight sprite list every frame using a list of flags for whether each card is highlighted
        # works, but seems clumsy; better way might be ... different textures? Alpha? I dunno. Stick w/this for now
        # so we don't even really need self.highligh_list - but might if we do this a different way
        # now it gets rebuilt every frame in onDraw.
        # TODO have a flag for highlights_changed and only rebuild (and clear the flag) on frames where it's true
        # actually now will just keep an array of previous highlighted cards and compare in the draw
        # and highlight_list will get re-created there
        # but create it here and register
        highlight_list = arcade.SpriteList()
        highlight_sprites = []
        # highlights for all 4 cards and starter (shew version
        for j in range(4):
            # For now there is only one kind of highlight, later can use others like I do with cards and pegs
            newhighlight = Highlight("pybgrx_assets/YellowHighlight.png",scale=SPRITE_SCALING)
            newhighlight.left = (CARD_SHOW_LEFT_MARGIN - HIGHLIGHT_WIDTH) + (j * (CARD_WIDTH + CARD_SHOW_INTERCARD_MARGIN))
            newhighlight.bottom = CARD_SHOW_BOTTOM_MARGIN - HIGHLIGHT_WIDTH
            highlight_sprites.append(newhighlight)
            #highlight_list.append(newhighlight)
        # then the starter highlight
        newhighlight = Highlight("pybgrx_assets/YellowHighlight.png",scale=SPRITE_SCALING)
        newhighlight.left = CARD_STARTER_LEFT - HIGHLIGHT_WIDTH
        newhighlight.bottom = CARD_STARTER_BOTTOM - HIGHLIGHT_WIDTH
        highlight_sprites.append(newhighlight)
        #highlight_list.append(newhighlight)
        self.add_sprite_list("highlights",highlight_list,highlight_sprites)
        self.now_highlighted = [False] * len(highlight_sprites)

        # Set up the player - let's try a king of hearts
        # would this work for loading the whole set of them?
        # https://arcade.academy/_modules/arcade/texture.html#load_spritesheet
        # was self.player_sprite = Player("pybgrx_assets/CardBack.png", SPRITE_SCALING)
        # arcade.load_spritesheet(file_name: str, sprite_width: int, sprite_height: int, columns: int, count: int)
        # → List[source]
        # it totally works!
        # temp, make it a peg so we can reckon all the hole positions
        # then make a highlight
        player_list = arcade.SpriteList()
        player_sprite = Player("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING)
        player_sprite.left = 18 * SCALE_FACTOR
        player_sprite.bottom = 26 * SCALE_FACTOR
        player_list.append(player_sprite)
        self.add_sprite_list("player",player_list,[player_sprite])


    def update_game_logic(self):
        pass

    def on_draw(self):
        # print("on_draw")
        # this doesn't seem to be working
        # Draw the background texture
        # TODO find out if there's a way to do this unsmoothed
        bgtexs = self.get_textures("background")
        #print("bgtexs =",bgtexs)
        if bgtexs is not None:
            scale = SCREEN_WIDTH / bgtexs[0].width #self.background.width
            #print("scale =",scale)
            if bgtexs is not None:
                arcade.draw_lrwh_rectangle_textured(0, 0,
                                                    SCREEN_WIDTH, SCREEN_HEIGHT,
                                                    bgtexs[0]) # assuming only 1 bg texture
        #dunt work - ,filter = gl.GL_NEAREST)
        #
        #
        # build highlight list
        # which is now automated by checking if the highlights are different from when we looked last
        card_sprites = self.get_sprite_list_by_name("cards")
        highlight_sprites = self.get_sprite_list_by_name("highlights")
        #rint("card sprites =",card_sprites)
        #print("highlight sprites =",highlight_sprites)
        if (card_sprites is not None) and (highlight_sprites is not None):
            now_highlighted = [x.is_highlighted() for x in card_sprites["sprites"]]
            if self.last_highlighted != now_highlighted:
                #print("now_highlighted", now_highlighted, "last_highlighted", self.last_highlighted)
                highlight_list = arcade.SpriteList()
                for i in range(len(card_sprites["sprites"])):
                    if now_highlighted[i] == True:
                        #print("Adding highlight sprite",i,"which is",highlight_sprites["sprites"][i])
                        highlight_list.append(highlight_sprites["sprites"][i])
                self.last_highlighted = now_highlighted
                self.replace_sprite_list_by_name("highlights",highlight_list,highlight_sprites["sprites"])

        for sl in self.sprite_lists:
            if "SpriteList" in sl and sl["SpriteList"] is not None:
                #print("Drawing sprite list",sl["name"])
                sl["SpriteList"].draw(filter = gl.GL_NEAREST)



        # then for TODO TEMP hole finding print the player's bottom and left.
        # start_x and start_y make the start point for the text. We draw a dot to make it easy too see
        # the text in relation to its start x and y.
        # start_x = self.player_sprite.left + self.player_sprite.width
        # start_y = self.player_sprite.top
        # arcade.draw_point(start_x, start_y, arcade.color.BLUE, 5)
        # pstring = "{},{}".format(self.player_sprite.left // SCALE_FACTOR, self.player_sprite.bottom // SCALE_FACTOR)
        # arcade.draw_text(pstring, start_x, start_y, arcade.color.WHITE, 20)

    def on_key_press(self, key, modifiers):
        player_sprite_list = self.get_sprite_list_by_name("player")

        if player_sprite_list is None:
            return

        player_sprite = player_sprite_list["sprites"][0]
        #print("Player_sprite is",player_sprite)

        if key == arcade.key.UP:
            player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        player_sprite_list = self.get_sprite_list_by_name("player")

        if player_sprite_list is None:
            return

        player_sprite = player_sprite_list["sprites"][0]

        if key == arcade.key.UP or key == arcade.key.DOWN:
            player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            player_sprite.change_x = 0




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

        # no current mode
        self.curmode = None

    def setup(self):
        """ Set up the game and initialize the variables. """

        # TODO here we will be setting up various mode objects

        # STUFF TO BREAK OUT INTO A MODE OBJECT ----------------------------------------------------------------------
        self.curmode = ShewMode()
        self.curmode.setup()
        # TODO later have multiple



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
        if self.curmode is not None:
            self.curmode.on_update()

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
