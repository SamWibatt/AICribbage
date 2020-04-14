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
        card_textures = arcade.load_spritesheet("pybgrx_assets/CardDeck.png",sprite_width=CARD_WIDTH,
                                                sprite_height=CARD_HEIGHT,columns=4,count=52)
        self.add_textures("cards",card_textures)
        card_list = arcade.SpriteList(is_static = True)
        card_sprites = []
        # so let's do 4 cards and a starter, say, and see what we get trying to use pixels
        # just take a swing, say 22 pixels in
        # TEMP TEST for 29 hand
        #cards = [4,43,30,23,17]  # = 5 of horts, 5s, 5c, Jd, 5d
        for j in range(4):
            # this is a kludge, load a card back sprite to set the image size, then use texture
            newcard = Card("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING)
            for t in range(52):
                newcard.append_texture(card_textures[t])  # swh
            #newcard.set_texture(1)
            newcard.left = CARD_SHOW_LEFT_MARGIN + (j * (CARD_SCREEN_WIDTH + CARD_SHOW_INTERCARD_MARGIN))
            newcard.bottom = CARD_SHOW_BOTTOM_MARGIN
            card_sprites.append(newcard)
            card_list.append(newcard)
        # then the starter card
        newcard = Card("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING)
        for t in range(52):
            newcard.append_texture(card_textures[t])  # swh
        #newcard.set_texture(1)
        newcard.left = CARD_STARTER_LEFT
        newcard.bottom = CARD_STARTER_BOTTOM
        card_sprites.append(newcard)
        card_list.append(newcard)

        # set some highlights - TODO debug rip out
        #card_sprites[1].set_highlighted(True)
        #card_sprites[2].set_highlighted(True)
        #card_sprites[4].set_highlighted(True)

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
            newhighlight.left = (CARD_SHOW_LEFT_MARGIN - HIGHLIGHT_SCREEN_WIDTH) + \
                                (j * (CARD_SCREEN_WIDTH + CARD_SHOW_INTERCARD_MARGIN))
            newhighlight.bottom = CARD_SHOW_BOTTOM_MARGIN - HIGHLIGHT_SCREEN_WIDTH
            highlight_sprites.append(newhighlight)
            #highlight_list.append(newhighlight)
        # then the starter highlight
        newhighlight = Highlight("pybgrx_assets/YellowHighlight.png",scale=SPRITE_SCALING)
        newhighlight.left = CARD_STARTER_LEFT - HIGHLIGHT_SCREEN_WIDTH
        newhighlight.bottom = CARD_STARTER_BOTTOM - HIGHLIGHT_SCREEN_WIDTH
        highlight_sprites.append(newhighlight)
        #highlight_list.append(newhighlight)
        self.add_sprite_list("highlights",highlight_list,highlight_sprites)
        self.now_highlighted = [False] * len(highlight_sprites)

        # Here, one sprite for showing the score name
        scorename_textures = arcade.load_spritesheet("pybgrx_assets/ScoreNames-xparent.png",
                                                     sprite_width=SCORENAME_WIDTH,
                                                     sprite_height=SCORENAME_HEIGHT,columns=1,count=20)
        self.add_textures("scorenames",scorename_textures)
        scorename_list = arcade.SpriteList(is_static = True)
        # this is a kludge, load a card back sprite to set the image size, then use texture
        # note that TransparentScoreName can't be entirely transparent or the load fails. This one just has one pixel
        # of the background color in each corner
        newscorename = ScoreName("pybgrx_assets/TransparentScoreName.png",scale=SPRITE_SCALING)
        for j in range(20):
            #print("scorename_textures",j,"is",scorename_textures[j])
            newscorename.append_texture(scorename_textures[j])  # swh
        #newscorename.set_texture(20)        # test
        newscorename.left = 0
        newscorename.bottom = (SCREEN_HEIGHT // 2) - ((SCORENAME_HEIGHT//2) * SCALE_FACTOR)
        scorename_list.append(newscorename)
        self.add_sprite_list("scorenames",scorename_list,[newscorename])
        # TEMP TEST RIP OUT
        self.nextscoretexindex = 0

        #print("newscorename.texture is",newscorename.texture)

        # tens and ones digit for per-hand score i.e. fifteen two fifteen four
        scorenumber_textures = arcade.load_spritesheet("pybgrx_assets/ScoreNumbers-xparent.png",
                                                       sprite_width=SCORENUMBER_WIDTH,
                                                       sprite_height=SCORENUMBER_HEIGHT,columns=10,count=10)
        self.add_textures("scorenumbers",scorenumber_textures)
        # I plan for these to fly up and "kick" a peg into motion, so they're not static.
        scorenumber_list = arcade.SpriteList(is_static=False)
        scorenumber_sprites = []
        # so create 2 digits, each with 11 possible textures (blank, then 0..9)
        # so setting to a digit means adjusting by 1 but games are not all grace
        for i in range(2):
            newscorenumber = ScoreNumber("pybgrx_assets/TransparentScoreNumber.png",scale=SPRITE_SCALING)
            for j in range(10):
                newscorenumber.append_texture(scorenumber_textures[j])
            newscorenumber.left = SCORENUMBER_LEFT + (i * SCORENUMBER_SCREEN_WIDTH)
            newscorenumber.bottom = SCORENUMBER_BOTTOM
            scorename_list.append(newscorenumber)
            scorenumber_sprites.append(newscorenumber)
        self.add_sprite_list("scorenumbers",scorenumber_list,scorenumber_sprites)
        # TEMP to shew a number, later the ScoreNumber class will govern?
        #scnums = self.get_sprite_list_by_name("scorenumbers")
        #scnums["sprites"][0].set_texture(2+1)           # set tens digit to 2
        #scnums["sprites"][1].set_texture(9+1)           # set tens digit to 9



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
        player_sprite.left = CARD_DECK_LEFT
        player_sprite.bottom = CARD_DECK_BOTTOM
        player_list.append(player_sprite)
        self.add_sprite_list("player",player_list,[player_sprite])

        # event lists!
        self.score_evlist = EventList()
        self.peg_move_evlist = EventList()


    def update_game_logic(self,delta_time):
        #print("shew ugl dt =",delta_time)
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

    # on_tick emulates the system-wide timer interrupt I plan to set up in the ESP32/ardy version
    # which will make it less portable but is needed for debouncing and such
    def on_tick(self,delta_time):
        #print("shew tick dt =",delta_time)
        # test: step through score names
        # scorelist = self.get_sprite_list_by_name("scorenames")
        # if scorelist is not None:
        #     self.nextscoretexindex = (self.nextscoretexindex + 1) % 21
        #     # print("nexttexindex =",self.nextscoretexindex)
        #     scorelist["sprites"][0].set_texture(self.nextscoretexindex)
        # advance event lists...?
        # TODO: Might want to have a list of event lists like we do with textures and sprites in the base class
        self.score_evlist.update(delta_time)
        self.peg_move_evlist.update(delta_time)

    def on_leave(self):
        # TEMP? clear score name showing
        scorelist = self.get_sprite_list_by_name("scorenames")
        if scorelist is not None:
            scorelist["sprites"][0].set_texture(0)
        # TODO probably highlights and stuff


    def on_resume(self):
        # TEMP TODO RIP OUT
        self.nextscoretexindex = 0

        # OK so let's try a hand! - worky!
        # TODO Later I reckon this will get loaded up with the players' actual hands, or just
        # fish them out of the gamestate, then load them up for
        pyb = self.parent.get_gamestate()
        # for 29
        # hand = [pyb.stringcard(x) for x in ['5c', '5d', 'jh', '5s']]
        # starter = pyb.stringcard('5h')
        # for awesome double double run
        hand = [pyb.stringcard(x) for x in ['4c', '5c', '6s', '6h']]
        starter = pyb.stringcard('5d')
        cards = hand + [starter]
        print("cards",cards)
        print("hand",[pyb.cardstring(x) for x in hand],"starter",pyb.cardstring(starter)) # DEBUG TODO RIP OUT
        (score,subsets) = pyb.score_shew(hand,starter)
        pyb.render_score_subsets(hand, starter, subsets)  # renders to console # DEBUG TODO RIP OUT

        # TEMP need to set cards to the cards in the hand
        card_sprites = self.get_sprite_list_by_name("cards")["sprites"]
        for j in range(5):
            card_sprites[j].set_texture(cards[j]+1)

        # experiment: build an event list! From my 02 page in wiki! The "scriptoid" is an EventList.
        #     * basically need a "submit subset list" thing that builds a scriptoid for the on_tick to follow.
        #     * set incremental score display to 0
        #     * for each entry in the subset list:
        #         * say a total of a second display, can tighten or fiddle timings as needed
        #         * show highlights and score name immediately
        #         * wait 1/2 second
        #         * add subset scorelet to incremental score (later animated with a little number sprite and sparkles)
        #         * render new incremental score
        #         * wait 1/4 second
        #         * remove score name display
        #         * wait 1/4 second
        #         * if the skip button is pressed during all that
        #             * render final incremental score and go to next step
        # second event list:
        #     * after the incremental score is all added up, OR skip,
        #         * move inc score to the player's back peg. Pretty fast, like 1/5 second?
        #         * back peg flies to its new spot
        self.score_evlist = EventList()
        # TODO figure out how to register a skip callback
        # loop based on pyb.render_score_subsets
        cur_acc_millis = 0          # start off at time 0
        # at timestamp 0:
        # - callback that sets incremental score to 0, and prints inc. score display
        self.score_evlist.add_event("reset_score",cur_acc_millis,self.set_incremental_score_evcallback,0)
        # maybe wait a tick like 1/4s
        cur_acc_millis += 250
        total_inc_score = 0
        j = 0
        for subset in subsets:
            j += 1
            # partcards is list of 0..4, where 0..3 are cards in hand, 4 is starter
            # should align for our highlights and such
            (partcards,scoreindex) = subset
            # add up the total incremental score before starting the animation, in case it gets skipped
            total_inc_score += self.parent.get_gamestate().scoreStringsNPoints[scoreindex][1]
            # at cur_acc_millis:
            # - callback to set cards' highlights according to partcards
            self.score_evlist.add_event("highlight"+str(j), cur_acc_millis, self.set_card_highlights_evcallback, partcards)
            # - callback to set score name's texture according to scoreindex - add 1 to skip blank at texture 0
            self.score_evlist.add_event("set_scorename"+str(j), cur_acc_millis, self.set_scorename_evcallback, scoreindex+1)
            # add 500 to cur_acc millis for 1/2 second delay - let's slow this down
            cur_acc_millis += 750
            # - callback add subset score to running total and display new running score
            self.score_evlist.add_event("reset_score"+str(j), cur_acc_millis, self.set_incremental_score_evcallback,
                                   total_inc_score)
            # add 250 to cur_acc_millis for 1/4 second delay
            cur_acc_millis += 350
            # - callback to set score name display to blank/off
            self.score_evlist.add_event("clr_scorename"+str(j),cur_acc_millis, self.set_scorename_evcallback,0)
            # add 250 to cur_acc_millis for 1/4 second delay
            cur_acc_millis += 350
        # clear all highlights
        self.score_evlist.add_event("highlight"+str(j), cur_acc_millis, self.set_card_highlights_evcallback, [])

        # TODO separate event list for the score flying up and kicking the peg
        self.peg_move_evlist = EventList()

        # then set it rolling!
        self.score_evlist.run()

    # callbacks for event list
    def set_incremental_score_evcallback(self,newscore):
        # set score sprites to whatever newscore says
        scnums = self.get_sprite_list_by_name("scorenumbers")
        # set tens digit: if it's 0, draw the blank sprite
        tens = newscore // 10
        if (tens) == 0:
            scnums["sprites"][0].set_texture(0)         # set tens digit to blank
        else:
            scnums["sprites"][0].set_texture(tens+1)    # set tens digit to number
        scnums["sprites"][1].set_texture((newscore % 10)+1)           # set ones digit to number

    def set_scorename_evcallback(self,scoreindex_plus_one):
        # set score name to appropriate score name index
        # we will pass in scoreindex + 1 to skip over the blank - if we want blank, pass in 0
        scname = self.get_sprite_list_by_name("scorenames")
        scname["sprites"][0].set_texture(scoreindex_plus_one)

    def set_card_highlights_evcallback(self,partcards):
        cards = self.get_sprite_list_by_name("cards")["sprites"]
        for j in range(5):
            cards[j].set_highlighted(j in partcards)

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
