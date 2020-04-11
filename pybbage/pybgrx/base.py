# Pybgrx base classes - cleaning up this:
# PYBGRX.PY - graphic interface to pybbage
# using "arcade" library from https://arcade.academy/index.html
#
# Purpose:
# To experiment and develop a graphical cribbage game that can be ported to small systems like Arduino / 320x240 LCD
# And possibly to fancy glossy version like Gold Fish 3 but for cribbage

# constants - think re: where these should go
# gross, but avoids having to type pybgrx.constants in front of everything
from pybgrx.constants import *

import arcade
import os
import pyglet.gl as gl
# then my actual game mechanics!
from pyb import pybbage as pyb



# SPRITE CLASSES ======================================================================================================

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

# for cards
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

# for highlights
class Highlight(arcade.Sprite):

    # currently not much needs to be done
    def update(self):
        pass

# for pegs
class Peg(arcade.Sprite):

    # currently not much needs to be done
    def update(self):
        pass


# class for containing a "mode" - will see what all gets in there, but I think it's pretty much everything
# that's currently in MyGame - background, sprites, user interface, etc.
# subclass for different game phases like cut for deal, deal, discard, etc.
# so figure out how to refactor the current single screen into
class Mode:

    def __init__(self, sprite_lists = None, textures = None, parent = None):
        # self.sprite_lists is a list of dicts like this:
        # {
        #     "name" : name
        #     "SpriteList" : arcade.SpriteList object for rendering,
        #     "sprites": list of the individual sprites in that sprite list
        # }
        # so game logic can look in the "sprites" part to change position, texture, whatever else
        self.sprite_lists = sprite_lists

        # self.textures is a dict of name to of lists of textures, some of which (like bg texture) might only have
        # one texture in them e.g.
        # {
        #     "background" -> [bg texture],
        #     "cards" -> [ card 0, card 1, card 2, ...],
        #     "pegs" -> [ blue peg, green peg, ...]
        # }
        # this would likely be shared across most or all of the modes
        self.textures = textures

        # and parent game, so this can do stuff like ask it to advance to a new mode
        self.parent = parent

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

    def set_parent(self,parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    # overrideables --------------------------------------------------------------------------------------------------

    def setup(self):
        pass

    def on_draw(self):
        # Draw the background texture
        # TODO find out if there's a way to do this unsmoothed
        bgtexs = self.get_textures("background")
        #print("bgtexs =",bgtexs)
        if bgtexs is not None:
            scale = SCREEN_WIDTH / bgtexs[0].width
            if bgtexs is not None:
                arcade.draw_lrwh_rectangle_textured(0, 0,
                                                    SCREEN_WIDTH, SCREEN_HEIGHT,
                                                    bgtexs[0]) # assuming only 1 bg texture
        # draw sprites
        if self.sprite_lists is not None:
            for sl in self.sprite_lists:
                if "SpriteList" in sl and sl["SpriteList"] is not None:
                    #print("Drawing sprite list",sl["name"])
                    sl["SpriteList"].draw(filter = gl.GL_NEAREST)


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
        # TODO WRITE DEFAULT VERSION if there is anything - like mode advance
        pass

    def on_key_release(self, key, modifiers):
        # how to handle? maybe a dict of key constant -> member function to handle it?
        # TODO WRITE DEFAULT VERSION if there is anything
        pass

    def on_leave(self):
        # called when switching to another mode
        pass

    def on_resume(self):
        # called when switching back to this mode
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

        # so here's our game state!
        self.gamestate = pyb.Pybbage()

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

    def setup(self):
        """ Set up the game and initialize the variables. """

        # TODO here we will be setting up various mode objects

        # STUFF TO BREAK OUT INTO A MODE OBJECT ----------------------------------------------------------------------
        self.modes = []
        titlemode = TitleMode(parent = self)
        titlemode.setup()
        self.modes.append(titlemode)     # mode 0: title
        shewmode = ShewMode(parent = self)
        shewmode.setup()
        self.modes.append(shewmode)      # mode 1: (though later another) shew
        self.curmode_index = 0
        self.curmode = self.modes[self.curmode_index]   # start at mode 0
        # TODO later have multiple


    def set_nextmode_index(self,nextmode_index):
        # for letting this object know the current mode is ready to switch to another
        self.nextmode_index = nextmode_index

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
            self.curmode.on_update()
        # MAYBE MOVE THIS INTO A SEPARATE FUNCTION THAT RUNS ON A SCHEDULE OF LIKE 1/20 of a second ===================

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if self.curmode is not None:
            self.curmode.on_key_press(key,modifiers)


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if self.curmode is not None:
            self.curmode.on_key_release(key,modifiers)
