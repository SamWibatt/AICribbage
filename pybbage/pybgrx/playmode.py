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

        # then some peg sprites! Would be nice not to have to copy this everywhere. REFACTOR
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
        # then let's make some stationary card sprites for where I think they might be in the real game
        # normal list of them to be able to access each and change things - do we need it?
        card_textures = arcade.load_spritesheet("pybgrx_assets/CardDeck.png",sprite_width=CARD_WIDTH,
                                                sprite_height=CARD_HEIGHT,columns=4,count=52)
        self.add_textures("cards",card_textures)

        # 8 cards in the play - draw the ones that have been played so start them all invisible.
        # making non-static
        # actually let's do a single list for both cards and highlights
        # bc they both end up getting drawn in the same list
        play_card_n_hl_list = arcade.SpriteList(is_static = False)
        play_card_n_hl_sprites = []
        # build it s.t. first 8 sprites are cards, then second 8 are hls
        for j in range(8):
            # this is a kludge, load a card back sprite to set the image size, then use texture
            newcard = Card("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING,visible=True,highlighted=True)
            for t in range(52):
                newcard.append_texture(card_textures[t])  # swh
            newcard.left = CARD_PLAY_LEFT_MARGIN + (j * CARD_PLAY_NEXTCARD_DIST)
            newcard.bottom = CARD_PLAY_BOTTOM_MARGIN
            newcard.set_texture(1+ (4*j))   # temp
            play_card_n_hl_sprites.append(newcard)
            # we're going to do a thing like with higlights in shew, build sprite list at display time with
            # visible cards and these are all invisible

        # THEN PLAY-CARD HIGHLIGHT SPRITES
        for j in range(8):
            # For now there is only one kind of highlight, later can use others like I do with cards and pegs
            newhighlight = Highlight("pybgrx_assets/YellowHighlight.png",scale=SPRITE_SCALING)
            newhighlight.left = (CARD_PLAY_LEFT_MARGIN - HIGHLIGHT_SCREEN_WIDTH) + \
                                (j * CARD_PLAY_NEXTCARD_DIST)
            newhighlight.bottom = CARD_PLAY_BOTTOM_MARGIN - HIGHLIGHT_SCREEN_WIDTH
            play_card_n_hl_sprites.append(newhighlight)

        self.add_sprite_list("playcardsnhighlights",None,play_card_n_hl_sprites)
        # build visible and highlighted lists to detect if we need to
        # update display - start out with empties to force draw
        self.play_last_visible = [] #[play_card_n_hl_sprites[x].is_visible() for x in range(8)]
        self.play_last_highlighted = [] #[play_card_n_hl_sprites[x].is_highlighted() for x in range(8)]

        # we have 4 cards in the hand
        hand_card_list = arcade.SpriteList(is_static = False)
        hand_card_sprites = []
        for j in range(4):
            # this is a kludge, load a card back sprite to set the image size, then use texture
            newcard = Card("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING,visible=True,highlighted=False)
            for t in range(52):
                newcard.append_texture(card_textures[t])  # swh
            newcard.left = CARD_PLAY_HAND_LEFT_MARGIN + (j * (CARD_SCREEN_WIDTH + CARD_PLAY_INTERCARD_MARGIN))
            newcard.bottom = CARD_PLAY_BOTTOM_MARGIN
            newcard.set_texture(1+ (38 + (4*j)))   # temp
            hand_card_sprites.append(newcard)
            hand_card_list.append(newcard)
        hand_card_sprites[0].set_highlighted(True)  # TEMP TEST KLUDGE RIP OUT
        hand_card_sprites[2].set_highlighted(True)  # TEMP TEST KLUDGE RIP OUT
        self.add_sprite_list("handcards",hand_card_list,hand_card_sprites)
        # build visible and highlighted lists to detect if we need to
        # update display - start out with empties to force draw
        self.hand_last_visible = [] # x.is_visible() for x in hand_card_sprites]
        self.hand_last_highlighted = [] # [x.is_highlighted() for x in hand_card_sprites]

        # then the deck up in the corner - should prolly be part of bg
        deck_list = arcade.SpriteList(is_static=True)
        newcard = Card("pybgrx_assets/CardBack.png",scale=SPRITE_SCALING)
        newcard.left = CARD_DECK_LEFT
        newcard.bottom = CARD_DECK_BOTTOM
        deck_list.append(newcard)
        self.add_sprite_list("deck",deck_list,[newcard])

        # TODO HERE SPECIAL WEIRD highlights for hand cards' highlights: just make the sprites and have a
        # None list for them; their list will be built at draw time
        # TODO do I need to do the only-redraw-if-changed thing like in shew?
        hand_highlight_sprites = []
        # highlights for all 4 cards (hand version)
        for j in range(4):
            # For now there is only one kind of highlight, later can use others like I do with cards and pegs
            newhighlight = Highlight("pybgrx_assets/YellowHighlight.png",scale=SPRITE_SCALING)
            newhighlight.left = (CARD_PLAY_HAND_LEFT_MARGIN - HIGHLIGHT_SCREEN_WIDTH) + \
                                (j * (CARD_SCREEN_WIDTH + CARD_PLAY_INTERCARD_MARGIN))
            newhighlight.bottom = CARD_PLAY_BOTTOM_MARGIN - HIGHLIGHT_SCREEN_WIDTH
            hand_highlight_sprites.append(newhighlight)
        #highlight_list.append(newhighlight)
        self.add_sprite_list("handhighlights",None,hand_highlight_sprites)



    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.parent.set_nextmode_index(0)

    # need to do custom on_draw here because cards can move, appear, and disappear

    def on_draw(self):
        # print("on_draw")
        # this doesn't seem to be working
        # Draw the background texture - pity we have to copy this from the superclass
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

        # TODO here build sprite list of cards in hand and highlight (if there is one) according to card highlight
        # TODO flag. Also leave cards/corresponding highlight out where the card's visible flag is false.
        # do we need the visible flag? let's say we do. Leave the card and any highlight it might have
        # out of the list if if its visible flag is false.
        # reckon we need a list of invisible highlight sprites too? That's the way I did it in shewmode but
        # kind of silly. Welp, prototype. It's also not that bad.
        sl_handcards = self.get_sprite_list_by_name("handcards")

        # first see if anything has changed in visibility or highlights.
        hand_visible = [x.is_visible() for x in sl_handcards["sprites"]]
        hand_highlighted = [x.is_highlighted() for x in sl_handcards["sprites"]]

        if hand_visible != self.hand_last_visible or hand_highlighted != self.hand_last_highlighted:
            sl_handhl = self.get_sprite_list_by_name("handhighlights")
            highlight_list = arcade.SpriteList()
            handcard_list = arcade.SpriteList()
            # ok so build the card list: card = visible means put the card in
            # the card list; if card also = highlighted means put the corresponding
            # highlight in the highlight list.
            for j in range(4):      # danger hardcodey 4 - but I won't change the # of cards in a hand
                if sl_handcards["sprites"][j].is_visible():
                    handcard_list.append(sl_handcards["sprites"][j])
                    if sl_handcards["sprites"][j].is_highlighted():
                        highlight_list.append(sl_handhl["sprites"][j])

            self.replace_sprite_list_by_name("handcards",handcard_list,sl_handcards["sprites"])
            self.replace_sprite_list_by_name("handhighlights",highlight_list,sl_handhl["sprites"])
            self.hand_last_visible = hand_visible
            self.hand_last_highlighted = hand_highlighted

        # TODO HERE build sprite list for  stack cards - this is a little different - build a list of card, highlight,
        # TODO card, highlight - where highlight is driven by card's highlight flag.
        # TODO also mind the card's visible flag.
        sl_playcards_n_hl = self.get_sprite_list_by_name("playcardsnhighlights")
        playcard_n_hl_list = arcade.SpriteList()

        # look for changes - a little bit different since both card & hl in same list
        play_visible = [sl_playcards_n_hl["sprites"][x].is_visible() for x in range(8)]
        play_highlighted = [sl_playcards_n_hl["sprites"][x].is_highlighted() for x in range(8)]

        if play_visible != self.play_last_visible or play_highlighted != self.play_last_highlighted:
            # so for each card, if it's visible:
            # - add it to the list ["sprites"][j]
            # - if it's visible, also add its highlight ["sprites"][j+8]
            for j in range(8):
                if sl_playcards_n_hl["sprites"][j].is_visible():
                    playcard_n_hl_list.append(sl_playcards_n_hl["sprites"][j])
                    if sl_playcards_n_hl["sprites"][j].is_highlighted():
                        playcard_n_hl_list.append(sl_playcards_n_hl["sprites"][j+8])

            self.replace_sprite_list_by_name("playcardsnhighlights",playcard_n_hl_list,sl_playcards_n_hl["sprites"])
            self.play_last_visible = play_visible
            self.play_last_highlighted = play_highlighted

        # then render all the sprite lists
        for sl in self.sprite_lists:
            if "SpriteList" in sl and sl["SpriteList"] is not None:
                #print("Drawing sprite list",sl["name"])
                sl["SpriteList"].draw(filter = gl.GL_NEAREST)


        # then the rest of this is from shewmode, and I will do something like it here, see above
        # #dunt work - ,filter = gl.GL_NEAREST)
        # #
        # #
        # # build highlight list
        # # which is now automated by checking if the highlights are different from when we looked last
        # card_sprites = self.get_sprite_list_by_name("cards")
        # highlight_sprites = self.get_sprite_list_by_name("highlights")
        # #rint("card sprites =",card_sprites)
        # #print("highlight sprites =",highlight_sprites)
        # if (card_sprites is not None) and (highlight_sprites is not None):
        #     now_highlighted = [x.is_highlighted() for x in card_sprites["sprites"]]
        #     if self.last_highlighted != now_highlighted:
        #         #print("now_highlighted", now_highlighted, "last_highlighted", self.last_highlighted)
        #         highlight_list = arcade.SpriteList()
        #         for i in range(len(card_sprites["sprites"])):
        #             if now_highlighted[i] == True:
        #                 #print("Adding highlight sprite",i,"which is",highlight_sprites["sprites"][i])
        #                 highlight_list.append(highlight_sprites["sprites"][i])
        #         self.last_highlighted = now_highlighted
        #         self.replace_sprite_list_by_name("highlights",highlight_list,highlight_sprites["sprites"])
        #
        # for sl in self.sprite_lists:
        #     if "SpriteList" in sl and sl["SpriteList"] is not None:
        #         #print("Drawing sprite list",sl["name"])
        #         sl["SpriteList"].draw(filter = gl.GL_NEAREST)

