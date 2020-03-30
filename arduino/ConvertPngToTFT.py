# convert png to 565 RGB for cribbage mockup and game
# requires pypng:
#     https://pypi.org/project/pypng/
#     https://github.com/drj11/pypng
#     https://pypng.readthedocs.io/en/latest/ex.html
#
# TODO: ==============================================================================================================
# - rotate by 90, 180, 270 degrees to match native display orientation for best speed
# - RLE compression, bc that will help a lot
#    - and arduino side to handle that which will probably be my own version of pushcolors
# =====================================================================================================================
# based on converter for 240x240 TFT which had these notes:
# ---
# e.g.  - this way makes them show up as tabs in the arduino IDE, not sure that'll work
#Sean@Takkun /cygdrive/c/Users/Sean/Dropbox/Private/make/esp32/Arduino/TFT_graphicstest_PDQ_Seantweak/data
#$ python3 ConvertPngToTFT.py Ent240.png goggles > ../Ent240.h
#Sean@Takkun /cygdrive/c/Users/Sean/Dropbox/Private/make/esp32/Arduino/TFT_graphicstest_PDQ_Seantweak/data
#$ python3 ConvertPngToTFT.py dogs240.png choggles > ../dogs240.h
#Sean@Takkun /cygdrive/c/Users/Sean/Dropbox/Private/make/esp32/Arduino/TFT_graphicstest_PDQ_Seantweak/data
#$ python3 ConvertPngToTFT.py leaf240.png loggles > ../leaf240.h
# after including those, Sketch uses 358532 bytes (27%) of program storage space. Maximum is 1310720 bytes.
# and the dog png worked! The icky bit is that you can't reload the tabs when you change the files w/o restarting  IDE.
# ---

import sys
import png
import itertools

# int16_t x,y;
# uint8_t r, g, b;
# uint16_t colr;

# //super hardcodey assuming 240x240, r, g, b 8 bits each
# for(y=0;y<240;y++) {
    # for(x=0;x<240;x++) {
      # r = file.read();
      # g = file.read();
      # b = file.read();

      # //assemble into 16 bit RGB 565, yes?
      # //so retain top 5 bits of R, shift left by 8
      # colr = ((uint16_t)(r & 0xF8)) << 8;
      # //retain top 6 bits of G, shift left 3, OR onto colr
      # colr |= ((uint16_t)(g & 0xFC)) << 3;
      # //retain top 5 bits of B, shift right 3, OR onto colr
      # colr |= ((uint16_t)(b & 0xF8)) >> 3;
      # tft.drawPixel(x, y, colr);
    # }
# }


if __name__ == '__main__':
    # *********************************************************************************
    # set cmdline arg defaults
    # *********************************************************************************
    rotfactor = 0           # rotation: 0 = none, 1 = 90 deg cl, 2 = 180 deg cl, 3 = 270 deg cl
    byteswap = True         # byteswap of 16 bit 565 pixels for pushColors
    debugWrite = True       # write a png to make sure rotation and such worked SHOULD BE DEFAULT FALSE

    if(len(sys.argv) < 3):
        print("Usage: ConvertPNGToTFT [-r0,-r1,-r2,-r3] <input png name> <pixel array name> > <output.inc>")
        print("-r0 = do not rotate")
        print("-r1 = rotate 90 degrees clockwise")
        print("-r2 = rotate 180 degrees clockwise")
        print("-r3 = rotate 270 degrees clockwise")
        print("  prints C array of the png to stdout in the RGB 565 format")
    else:
        j = 1
        while sys.argv[j].startswith('-'):
            if sys.argv[j] == '-r0':
                print("//*** will not rotate")
                rotfactor = 0
            elif sys.argv[j] == '-r1':
                rotfactor = 1
                print("//*** will rotate clockwise 90 degrees")
            elif sys.argv[j] == '-r2':
                rotfactor = 2
                print("//*** will rotate clockwise 180 degrees")
            elif sys.argv[j] == '-r3':
                rotfactor = 3
                print("//*** will rotate clockwise 270 degrees")
            # ********************************************************************************************************
            # PARSE OTHER CMDLINE ARGS HERE like byteswap, debug, compression or whatever
            # ********************************************************************************************************
            j += 1

        # parse png file and array stem
        pngFileName = sys.argv[j]
        j += 1
        pngArrayName = sys.argv[j]


        #print("Aha, we will be dealing with png file {} and making array {}".format(pngFileName,pngArrayName))
        r=png.Reader(file = open(pngFileName,"rb"))
        (pngWidth,pngHeight,pngRows,pngInfo) = r.read()        #  kind of wasteful since we may reread below but
        # this will get us metadata and w/h
        # try this:

        #print("PNG width {} height {} info {} - rows is type {}".format(pngWidth,pngHeight,pngInfo,type(pngRows)))


        # emit array header
        print("// Conversion of {} to 565 RGB - {} x {} pixels".format(pngFileName,pngWidth,pngHeight))
        print("// metadata {}".format(pngInfo))

        # HERE DO THE THING WITH ROTATION?
        # or it's probably easier just to do it in the loop
        # BUT... could try numpy, though be mindful of https://github.com/drj11/pypng/issues/91
        # Normally it works:
        # >> > a = np.array([[0, 1], [2, 3]]).astype(np.int8)
        # >> > i = png.from_array(a, mode='L')
        # >> > i.save('/tmp/i.png')
        # # Transposing breaks it:
        # >> > a_trans = np.transpose(a)
        # >> > i_trans = png.from_array(a_trans, mode='L')
        # >> > i_trans.save('/tmp/i_trans.png')
        #
        # Fix:
        # a_trans = a.transpose().copy() # instead of just np.transpose(a)
        # but doing it by hand is not so bad, I think, unless I get processing big old bunches

        # table that, should be not bad to do this with list comprehensions!

        # so metadata looks like this for my Cribmock3-48x31n64x41cards.png
        # metadata {'greyscale': False, 'alpha': False,
        #     'planes': 3, 'bitdepth': 8, 'interlace': 0, 'size': (320, 240),
        # '    physical': _Resolution(x=11811, y=11811, unit_is_meter=True)}
        #

        # from https://pypng.readthedocs.io/en/latest/png.html#lists-arrays-sequences-and-so-on:
        # I'm currently using read() -
        # read(lenient=False)
        #     Read the PNG file and decode it. Returns (width, height, rows, info).
        #     May use excessive memory.
        #     rows is a sequence of rows; each row is a sequence of values.
        #     If the optional lenient argument is True, checksum failures will raise warnings rather than exceptions.
        #
        # so could inspect metadata and use these to get what I want:
        #
        # asRGB() - I only mention this bc it tells what happens with greyscale; I want 8 bit vals
        #     Return image as RGB pixels. RGB colour images are passed through unchanged; greyscales are expanded into
        #     RGB triplets (there is a small speed overhead for doing this).
        #     An alpha channel in the source image will raise an exception.
        #     The return values are as for the read() method except that the info reflect the returned pixels, not the
        #     source image. In particular, for this method info['greyscale'] will be False.
        #
        #  asRGBA() - I only mention this bc it tells what happens; I want 8 bit vals
        #     Return image as RGBA pixels. Greyscales are expanded into RGB triplets; an alpha channel is synthesized
        #     if necessary. The return values are as for the read() method except that the info reflect the returned
        #     pixels, not the source image. In particular, for this method info['greyscale'] will be False, and
        #     info['alpha'] will be True.
        #
        # asRGB8()
        #     Return the image data as an RGB pixels with 8-bits per sample. This is like the asRGB() method except
        #     that this method additionally rescales the values so that they are all between 0 and 255 (8-bit).
        #     In the case where the source image has a bit depth < 8 the transformation preserves all the information;
        #     where the source image has bit depth > 8, then rescaling to 8-bit values loses precision.
        #     No dithering is performed. Like asRGB(), an alpha channel in the source image will raise an exception.
        #     This function returns a 4-tuple: (width, height, rows, info).
        #     width, height, info are as per the read() method.
        #     rows is the pixel data as a sequence of rows.
        #
        # for alpha, which I can use for spritey things with xparency if I want to do this,
        #
        # asRGBA8()
        #     Return the image data as RGBA pixels with 8-bits per sample. This method is similar to asRGB8() and
        #     asRGBA(): The result pixels have an alpha channel, and values are rescaled to the range 0 to 255.
        #     The alpha channel is synthesized if necessary (with a small speed penalty).

        #
        # above did (pngWidth,pngHeight,pngRows,pngInfo) = r.read() to get metadata and such
        # DO SOME SANITY CHECKING ON METADATA! like that it's not greyscale
        # so metadata looks like this for my Cribmock3-48x31n64x41cards.png
        # metadata {'greyscale': False, 'alpha': False,
        #     'planes': 3, 'bitdepth': 8, 'interlace': 0, 'size': (320, 240),
        # '    physical': _Resolution(x=11811, y=11811, unit_is_meter=True)}
        if 'greyscale' in pngInfo and pngInfo['greyscale'] == True:
            print("// *****************************************************************")
            print("// *****************************************************************")
            print("// *****************************************************************")
            print("// GREYSCALE IMAGES CURRENTLY HANDLED AS RGB!!!!!!!!!!!!!!!!!!!!!!!!")
            print("// *****************************************************************")
            print("// *****************************************************************")
            print("// *****************************************************************")

        # check for alpha
        hasAlpha = False
        if 'alpha' not in pngInfo or pngInfo['alpha'] == False:
            (pngWidth,pngHeight,pngRows,pngInfo2) = r.asRGB8()
        else:
            hasAlpha = True
            (pngWidth,pngHeight,pngRows,pngInfo2) = r.asRGBA8()

        # *************************************************************************************************************
        # *************************************************************************************************************
        # *************************************************************************************************************
        #  OK HERE SO DO ROTATIONS N STUFF
        # actually should do RGB -> 565 first
        # *************************************************************************************************************
        # *************************************************************************************************************
        # *************************************************************************************************************

        # so: convert rows to 565
        # each row is r,g,b,r,g,b,... yes?
        # how to list comprehend that into rgbs? Here's a start:
        # >>> l = [ 0,0,0,255,255,255 ]
        # >>> [ l[3*x:(3*x)+3] for x in range(len(l)//3) ]
        # [[0, 0, 0], [255, 255, 255]]
        # so conversion to 565 is like this:
        # colr = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | ((b & 0xF8) >> 3)
        # # SWAP BYTES TEST see if that helps with pushimage
        # colr = (colr >> 8) | ((colr & 0xFF) << 8)
        # maybe make a cmdline param for that
        # ((l[3*x] & 0xF8) << 8) | ((l[(3*x)+1] & 0xFC) << 3) | ((l[(3*x)+2] & 0xF8) >> 3)

        # so here is the non-byteswapped version
        rows565 = None
        if hasAlpha == False:
            rows565 = [ [ ((l[3*x] & 0xF8) << 8) | ((l[(3*x)+1] & 0xFC) << 3) | ((l[(3*x)+2] & 0xF8) >> 3)
                          for x in range(len(l)//3) ] for l in pngRows ]
            if byteswap == True:
                rows565  =[ [(colr >> 8) | ((colr & 0xFF) << 8) for colr in r] for r in rows565 ]
        else:
            print("//HEY ALPHA NOT HANDLED YET")

        if rotfactor == 1:
            # rotate 90 deg clockwise: we want
            # ABC -> DA
            # DEF    EB
            #        FC
            # swap width and height

            # >>> l = [ ['a','b','c'],['d','e','f']]
            # >>> [ [l[i][j] for i in range(len(l)-1,-1,-1)] for j in range(0,len(l[0])) ]
            # [['d', 'a'], ['e', 'b'], ['f', 'c']]
            rows565 = [[rows565[i][j] for i in range(len(rows565) - 1, -1, -1)] for j in range(0, len(rows565[0]))]
            (pngHeight,pngWidth) = (pngWidth,pngHeight)

        elif rotfactor == 2:
            # rotate 180 deg clockwise: we want
            # ABC -> FED
            # DEF    CBA
            #
            # preserve width and height
            rows565 = [ list(reversed(x)) for x in list(reversed(rows565)) ]


        elif rotfactor == 3:
            # rotate 270 deg clockwise: we want
            # ABC -> CF
            # DEF    BE
            #        AD
            # swap width and height
            # >>> l = [ ['a','b','c'],['d','e','f']]
            # >>> [ [l[i][j] for i in range(0,len(l))] for j in range(len(l[0])-1,-1,-1) ]
            # [['c', 'f'], ['b', 'e'], ['a', 'd']]
            rows565 = [ [rows565[i][j] for i in range(0,len(rows565))] for j in range(len(rows565[0])-1,-1,-1) ]
            (pngHeight,pngWidth) = (pngWidth,pngHeight)


        if debugWrite == True:
            # HERE WRITE DEBUG version of png

            debugPngName = pngFileName.replace('.png','')+"-debug.png"
            if hasAlpha:
                print("// ALPHA NOT SUPPORTED YET FOR DEBUG PNG")
                # DO CONVERSION TO RGBA
                #png.from_array(pixels, 'RGBA').save(debugPngName)
            else:
                # convert to RGB
                rowsrgb = rows565.copy()
                if byteswap == True:
                    #unswap bytes
                    rowsrgb = [[(colr >> 8) | ((colr & 0xFF) << 8) for colr in r] for r in rowsrgb]
                # then unpack RGB
                # pack was this: colr = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | ((b & 0xF8) >> 3)
                # so r = topmost 5 bits, shifted down to be top 5 bits of a byte
                # r = (colr & 0xF800) >> 8
                # g = next 6 bits so mask off 0000 0111 1110 0000 = 0x7E, shift down 3 to get in top of a byte
                # g = (colr & 0x07E0) >> 3
                # b = bottom 5 bits shifted up
                # b = (colr & 0x001F) << 3
                # https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
                # shawn chin's answer, leads to this
                # >>> r = [ [0xffff, 0x7fff],[0x0400,0x0200]]
                # >>> r2 = [ [ [c[i] // 2, c[i]//4] for i in range(len(c))] for c in r]
                # >>> r2
                # [[[32767, 16383], [16383, 8191]], [[512, 256], [256, 128]]]
                # >>> merged = [ list(itertools.chain.from_iterable(s)) for s in r2 ]
                # >>> merged
                # [[32767, 16383, 16383, 8191], [512, 256, 256, 128]]
                # so, first let's get a list of r,g,b for each pixel in the row lists
                # so it'll be [ [packedrgb1, packedrgb2], [packedrgb3, packedrgb4] ] ->
                # [ [ [r1,g1,b1], [r2, g2, b2] ], [ [ r3, g3, b3 ], [ r4, g4, b4 ] ]
                # then use the the itertools thing to flatten the rows to
                # [ [ r1, g1, b1, r2, g2, b2 ], [ r3, g3, b3, r4, g4, b4 ] ]
                # or can I use itertools to avoid the unflat list in the first place?
                # itertools is super cool
                # might be able to use map
                # beh, gets the same kind of thing and I don't want to spend all day on this
                rowsrgb = [ [ [ (row[i] & 0xF800) >> 8, (row[i] & 0x07E0) >> 3, (row[i] & 0x001F) << 3 ]
                              for i in range(len(row)) ] for row in rowsrgb ]
                # then flatten
                rowsrgb = [list(itertools.chain.from_iterable(s)) for s in rowsrgb]

                png.from_array(rowsrgb, 'RGB').save(debugPngName)
            print("//************* Wrote debug PNG:",debugPngName)



        # so now can check hasAlpha for when I do that stuff
        print("const uint32_t {}_w = {};".format(pngArrayName,pngWidth))
        print("const uint32_t {}_h = {};".format(pngArrayName,pngHeight))

        if hasAlpha == False:
            # do we need PROGMEM or anything? we will see! - looks like on esp32 "const" does it...?
            # probably do on uno
            # ESP32 version
            # print("const uint16_t {}[] = {{".format(pngArrayName))
            # uno version
            print("const uint16_t {}[] PROGMEM = {{".format(pngArrayName))
            pixnum = 0

            for row in rows565:
                for colr in row:
                    # do say 16 columns just to keep it neat
                    if pixnum != 0 and (pixnum % 16) == 0:
                        print ("")      # emit newline
                    if pixnum != ((pngWidth * pngHeight)-1):
                        print("{}, ".format(hex(colr)), end=" ")            #emit a comma after every pixel
                    else:
                        print (hex(colr))                                   #except the very last
                    pixnum += 1

            # old way
            # for row in pngRows:
            #     for x in range(pngWidth):
            #         (r,g,b) = row[x*3:(x+1)*3]
            #         # //assemble into 16 bit RGB 565, yes?
            #         # //so retain top 5 bits of R, shift left by 8
            #         # colr = ((uint16_t)(r & 0xF8)) << 8;
            #         # //retain top 6 bits of G, shift left 3, OR onto colr
            #         # colr |= ((uint16_t)(g & 0xFC)) << 3;
            #         # //retain top 5 bits of B, shift right 3, OR onto colr
            #         # colr |= ((uint16_t)(b & 0xF8)) >> 3;
            #         # let's try python's bitwise operators!
            #         colr = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | ((b & 0xF8) >> 3)
            #
            #         # SWAP BYTES TEST see if that helps with pushimage
            #         colr = (colr >> 8) | ((colr & 0xFF) << 8)
            #
            #         # do say 16 columns just to keep it neat
            #         if pixnum != 0 and (pixnum % 16) == 0:
            #             print ("")		# emit newline
            #
            #         if pixnum != (pngWidth * pngHeight):
            #             print("{}, ".format(hex(colr)), end=" ")				#emit a comma after every pixel
            #         else:
            #             print (hex(colr))							#except the very last
            #
            #         pixnum += 1

            # emit array close
            print("};")
        else:
            print("// ALPHA NOT YET SUPPORTED!!!!!!!!!!!!!!!!!!")
