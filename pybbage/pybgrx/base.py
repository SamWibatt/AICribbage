# Pybgrx base classes - cleaning up this:
# PYBGRX.PY - graphic interface to pybbage
# using "arcade" library from https://arcade.academy/index.html
#
# Purpose:
# To experiment and develop a graphical cribbage game that can be ported to small systems like Arduino / 320x240 LCD
# And possibly to fancy glossy version like Gold Fish 3 but for cribbage

# A lot of this will work with other games, might make a game skeleton out of it for prototyping other Arduino
# stuff

# constants - think re: where these should go
# gross, but avoids having to type pybgrx.constants in front of everything

from pybgrx.constants import *

import arcade
import os
import pyglet.gl as gl
# then my actual game mechanics!
from pyb import pybbage as pyb


# TODO move sprite classes to a game-specific file
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
    # also the visible parameter - which should be a part of my arduino base sprite class
    def __init__(self,filename: str = None, scale: float = 1, image_x: float = 0, image_y: float = 0,
                 image_width: float = 0, image_height: float = 0, center_x: float = 0, center_y: float = 0,
                 repeat_count_x: int = 1, repeat_count_y: int = 1,
                 highlighted = False, visible = True):
        self.highlighted = highlighted
        self.visible = visible
        super().__init__(filename,scale,image_x,image_y,image_width,image_height,center_x,center_y,
                         repeat_count_x,repeat_count_y)

    def set_highlighted(self,highlighted):
        self.highlighted = highlighted

    def is_highlighted(self):
        return self.highlighted

    def set_visible(self,visible):
        self.visible = visible

    def is_visible(self):
        return self.visible

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

# for score names
class ScoreName(arcade.Sprite):

    # currently not much needs to be done
    def update(self):
        pass

# for score numbers
class ScoreNumber(arcade.Sprite):

    # currently not much needs to be done
    def update(self):
        pass
# end # TODO move sprite classes to a game-specific file

# EVENT LIST ==========================================================================================================

# maintains a list of lists of [time in millis, callback, parameters]
# lists because then we can modify them if we wanna
# do we want to keep the list sorted? it seems appropriate
# also pass in a name so we can find by name
# parameters are what? *args and **kwargs, try

class EventList:
    def __init__(self):
        self.next_event_index = -1
        self.events = []
        self.accumulated_millis = 0
        self.active = False

    # how to hand in the args and kwargs? see tests/callbacktest.py
    def add_event(self, name, time_millis, callback, *args, **kwargs):
        #print("Add_event name:",name,"time:",time_millis,"cb",callback,"args:",args,"kw:",kwargs)
        # tried just making it a list all in one go like [name, time_millis, callback, *args, **kwargs]
        # but pycharm's syntax checker didn't like that
        # then again, from tests/callbacktest.py, the * and ** are wrong
        event_record = [name, time_millis, callback, args, kwargs]

        self.events.append(event_record)
        # TODO: trying to be fancy and inserting the elements in order is failing? Yup
        # if self.events == []:
        #     self.events = [event_record]
        # elif time_millis < self.events[0][1]:
        #     self.events.insert(0,event_record)
        # elif time_millis > self.events[-1][1]:
        #     self.events.append(event_record)
        # else:
        #     # look through the list until find a timestamp > than the one put on
        #     # so if there are some =, this one will be inserted after them
        #     for j in range(len(self.events)):
        #         if self.events[j][1] > time_millis:
        #             break
        #         # assuming j is within the list, bc the cases above handle other cases
        #         self.events.insert(j,event_record)

    def reset(self):
        # TODO figure out how to stand down whatever has been going on - or is that caller's responsibility?
        # e.g. skipping a shew score animation, how to shut off the sprites?
        self.next_event_index = 0
        self.accumulated_millis = 0
        self.active = False

    def run(self):
        # start things rolling
        self.next_event_index = 0
        self.active = True

    def pause(self):
        self.active = False

    # delta_time in seconds
    def update(self,delta_time):
        if self.active == False:
            return

        # convert to millis and accumulate
        delta_millis = int(delta_time / 0.001)
        self.accumulated_millis += delta_millis
        #print("delta_millis",delta_millis,"acc_millis",self.accumulated_millis)

        # execute events until the next event's timestamp is > accumulated millis
        while self.next_event_index < len(self.events) and \
            self.accumulated_millis >= self.events[self.next_event_index][1]:
            #print("about to do event",self.next_event_index,"out of",len(self.events),"timestamp",
            #      self.events[self.next_event_index][1],"at",self.accumulated_millis)
            # do the event callback - event is [name, time_millis, callback, args, kwargs]
            ev = self.events[self.next_event_index]     # to keep the next line tidy
            # from callbacktest, where it's [callback, args, kwargs]
            #         cbargs = self.callbacks[index][1]
            #         print("cbargs are",cbargs)
            #         cbkwargs = self.callbacks[index][2]
            #         print("cbkwargs are",cbkwargs)
            #         self.callbacks[index][0](*cbargs,**cbkwargs)
            args = ev[3]
            kwargs = ev[4]
            ev[2](*args,**kwargs)
            self.next_event_index += 1

        # halt if we've reached the end of the list
        if self.next_event_index < 0 or self.next_event_index >= len(self.events):
            self.active = False





# MODE CLASS ==========================================================================================================


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


    def update_game_logic(self,delta_time):
        # broken out from on_update so modes can override this without having to duplicate the drawing stuff
        # here, update whatever is relevant for the mode, like animating flying numbers or pegs or whatever
        # aaaand probably calling pybbage logic? Have to think about that. Might happen outside the drawing
        # seems unlikely you'd do heavy thinking in the draw update. TODO LOOK INTO
        pass

    def on_update(self,delta_time):
        # do game logic callback
        self.update_game_logic(delta_time)

        # call update on all the sprite lists
        if self.sprite_lists is not None:
            for sl in self.sprite_lists:
                if sl["SpriteList"] is not None:
                    sl["SpriteList"].update()

    def on_key_press(self, key, modifiers):
        # how to handle? maybe a dict of key constant -> member function to handle it?
        # TODO WRITE DEFAULT VERSION if there is anything - like mode advance
        pass

    def on_key_release(self, key, modifiers):
        # how to handle? maybe a dict of key constant -> member function to handle it?
        # TODO WRITE DEFAULT VERSION if there is anything
        pass

    def on_tick(self,delta_time):
        #print("on_tick dt =",delta_time)
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
