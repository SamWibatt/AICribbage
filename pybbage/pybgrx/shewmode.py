import arcade
import os
import pyglet.gl as gl
# then my actual game mechanics!
from pyb import pybbage as pyb

# not happy with import * so keep an eye on it
from pybgrx.constants import *
from pybgrx.base import *


# shew mode ==========================================================================================================

class ShewMode(Mode):

    # default init should work

    def setup(self):
        # Load the background image. Do this in the setup so we don't keep reloading it all the time.
        # Image from:
        # http://wallpaper-gallery.net/single/free-background-images/free-background-images-22.html
        # self.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")
        # note that we need a list of textures in the Mode object, for every texture set
        # main py file sets the working directory to its own so relative from there?
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

        # switch back to title screen, TODO TEMP
        if key == arcade.key.SPACE:
            self.parent.set_nextmode_index(0)


        player_sprite_list = self.get_sprite_list_by_name("player")

        if player_sprite_list is None:
            return

        player_sprite = player_sprite_list["sprites"][0]

        if key == arcade.key.UP or key == arcade.key.DOWN:
            player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            player_sprite.change_x = 0