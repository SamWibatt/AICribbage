# convert png to 565 RGB for little LCD thing
# e.g.  - this way makes them show up as tabs in the arduino IDE, not sure that'll work
#Sean@Takkun /cygdrive/c/Users/Sean/Dropbox/Private/make/esp32/Arduino/TFT_graphicstest_PDQ_Seantweak/data
#$ python3 ConvertPngToTFT.py Ent240.png goggles > ../Ent240.h
#Sean@Takkun /cygdrive/c/Users/Sean/Dropbox/Private/make/esp32/Arduino/TFT_graphicstest_PDQ_Seantweak/data
#$ python3 ConvertPngToTFT.py dogs240.png choggles > ../dogs240.h
#Sean@Takkun /cygdrive/c/Users/Sean/Dropbox/Private/make/esp32/Arduino/TFT_graphicstest_PDQ_Seantweak/data
#$ python3 ConvertPngToTFT.py leaf240.png loggles > ../leaf240.h
# after including those, Sketch uses 358532 bytes (27%) of program storage space. Maximum is 1310720 bytes.
# and the dog png worked! The icky bit is that you can't reload the tabs when you change the files w/o restarting the IDE.
#
# this will read it in ... or could I just use a png? Yeah, see if pypng works
# did at work with anaconda, swh at home - seems to!
#
# let's try swapping the bytes bc pushImage looks weird and I wanna use it
import sys
import png

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
	if(len(sys.argv) < 3):
		print("Usage: ConvertPNGToTFT <input png name> <pixel array name> > <output.inc>")
		print("  prints C array of the png to stdout in the RGB 565 format used by the little SPI LCD")
	else:
		pngFileName = sys.argv[1]
		pngArrayName = sys.argv[2]
		#print("Aha, we will be dealing with png file {} and making array {}".format(pngFileName,pngArrayName))
		r=png.Reader(file = open(pngFileName,"rb"))	# was (file=urllib.urlopen('http://www.schaik.com/pngsuite/basn0g02.png'))
		(pngWidth,pngHeight,pngRows,pngInfo) = r.read()
		#print("PNG width {} height {} info {} - rows is type {}".format(pngWidth,pngHeight,pngInfo,type(pngRows)))

		# DO SOME SANITY CHECKING ON METADATA! like that it's not greyscale

		# emit array header
		print("// Conversion of {} to 565 RGB - {} x {} pixels".format(pngFileName,pngWidth,pngHeight))
		print("// metadata {}".format(pngInfo))
		print("const uint32_t {}_w = {};".format(pngArrayName,pngWidth))
		print("const uint32_t {}_h = {};".format(pngArrayName,pngHeight))
		print("const uint16_t {}[] = {{".format(pngArrayName))			# do we need PROGMEM or anything? we will see! - looks like on esp32 "const" does it...?

		pixnum = 0
		for row in pngRows:
			for x in range(pngWidth):
				(r,g,b) = row[x*3:(x+1)*3]
				# //assemble into 16 bit RGB 565, yes?
				# //so retain top 5 bits of R, shift left by 8
				# colr = ((uint16_t)(r & 0xF8)) << 8;
				# //retain top 6 bits of G, shift left 3, OR onto colr
				# colr |= ((uint16_t)(g & 0xFC)) << 3;
				# //retain top 5 bits of B, shift right 3, OR onto colr
				# colr |= ((uint16_t)(b & 0xF8)) >> 3;
				# let's try python's bitwise operators!
				colr = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | ((b & 0xF8) >> 3)

				# SWAP BYTES TEST see if that helps with pushimage
				colr = (colr >> 8) | ((colr & 0xFF) << 8)

				# do say 16 columns just to keep it neat
				if pixnum != 0 and (pixnum % 16) == 0:
					print ("")		# emit newline

				if pixnum != (pngWidth * pngHeight):
					print("{}, ".format(hex(colr)), end=" ")				#emit a comma after every pixel
				else:
					print (hex(colr))							#except the very last

				pixnum += 1

		# emit array close
		print("};")
