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




# sprite h/w for score names and numbers (i.e., play and show incremental scores, not total scores.)
# given in literal pixel dimensions for cutting out of a sprite sheet
SCORENAME_HEIGHT = 44
SCORENAME_WIDTH = 320
SCORENUMBER_HEIGHT = 26
SCORENUMBER_WIDTH = 21

# for putting the incremental score to the right of the cards
SCORENUMBER_LEFT = (209 * SCALE_FACTOR)
SCORENUMBER_BOTTOM = (49 * SCALE_FACTOR)
SCORENUMBER_SCREEN_WIDTH = (SCORENUMBER_WIDTH * SCALE_FACTOR)

# similar for cards
CARD_HEIGHT = 64
CARD_WIDTH = 41

# for screen arrangement, in pixels.
CARD_SHOW_LEFT_MARGIN = (21 * SCALE_FACTOR)
CARD_SHOW_INTERCARD_MARGIN = (3 * SCALE_FACTOR)
CARD_SCREEN_WIDTH = (CARD_WIDTH * SCALE_FACTOR)                # hm
# need to figure out how to handle arcade's backwards y coordinates - yeah, I SAID IT
CARD_SHOW_BOTTOM_MARGIN = (29 * SCALE_FACTOR)

# highlight offset from card left/bottom
HIGHLIGHT_SCREEN_WIDTH = (3*SCALE_FACTOR)

# for putting the starter to the right of the hand
#CARD_STARTER_BOTTOM = (153 * SCALE_FACTOR)
#CARD_STARTER_LEFT = (265 * SCALE_FACTOR)
CARD_STARTER_BOTTOM = (29 * SCALE_FACTOR)
CARD_STARTER_LEFT = (265 * SCALE_FACTOR)

#CARD_DECK_BOTTOM = (29 * SCALE_FACTOR)
#CARD_DECK_LEFT = (265 * SCALE_FACTOR)
CARD_DECK_BOTTOM = (153 * SCALE_FACTOR)
CARD_DECK_LEFT = (265 * SCALE_FACTOR)

# play mode
# for screen arrangement, in pixels.
# hand cards to choose from - currently building on the right
CARD_PLAY_HAND_LEFT_MARGIN = (127 * SCALE_FACTOR)
CARD_PLAY_INTERCARD_MARGIN = (3 * SCALE_FACTOR)
# cards in the piled up cards on the left
CARD_PLAY_LEFT_MARGIN = (21 * SCALE_FACTOR)
CARD_PLAY_BOTTOM_MARGIN = (29 * SCALE_FACTOR)
# distance from the left edge of one card to the next, they overlap
CARD_PLAY_NEXTCARD_DIST = (21 * SCALE_FACTOR)

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
