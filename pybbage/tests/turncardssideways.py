# oops, I made the cards sideways
# deck should be columns by rank w ace at top, king at bottom, rows by suit, heart diamond club spade
# so pop open the original, which is (41*13) wide and (4*64) tall, yes? yes.

import sys
import png

if __name__ == "__main__":
    # deck should be columns by rank w ace at top, king at bottom, rows by suit, heart diamond club spade
    # so pop open the original, which is (41*13) wide and (4*64) tall, yes? yes.
    r = png.Reader(file = open("../pybgrx_assets/CardDeckOrigSideways.png","rb"))
    (pngWidth, pngHeight, pngRows, pngInfo) = r.read()
    print("Info re sideways cards:",pngInfo)

    rowlists = []
    for row in pngRows:
        rowlists.append(row)

    # so now we have the list of rows

    # create a new image that's (41*4) wide and (64*13) high
    # or rather make the rows; 41*4 * 3 bytes ber pixel, 832 = (13*64) rows
    # oh wait this is rgba, yes? 4 bytes ber pixel
    outrowlists = [ [0,0,0,0] * (41 * 4) for x in range(13*64) ]

    # debug non-rotated to make sure I'm getting the source correct
    odbrowlists = [[0,0,0,0] * (41*13) for x in range(4*64)]

    # so: step through the original row-major, copy 41x64 blocks col-major or wev
    for orow in range(4):
        for ocol in range(13):
            #print("orow:",orow,"ocol:",ocol)
            # ok! now go by pixels in a card
            for rowpix in range(64):
                for colpix in range(41):
                    for rgbapix in range(4):
                        # source row and column (remembering 3 bberp):
                        sourcerow = (64 * orow) + rowpix
                        sourcecol = (41 * 4 * ocol) + colpix * 4
                        sourcebyte = sourcecol + rgbapix
                        odbrowlists[sourcerow][sourcebyte] = rowlists[sourcerow][sourcebyte]
                        #print("orow:",orow,"ocol:",ocol,"sourcerow:",sourcerow,"sourcecol:",sourcecol,"sourcebyte:",sourcebyte)
                        # destination:
                        destrow = (64 * ocol) + rowpix
                        destcol = (41 * 4 * orow) + colpix * 4
                        destbyte = destcol + rgbapix
                        #print("destrow:",destrow,"destcol:",destcol,"destbyte:",destbyte)
                        # then assign!
                        outrowlists[destrow][destbyte] = rowlists[sourcerow][sourcebyte]


    f = open('out.png', 'wb')
    w = png.Writer(41*4, 64*13, greyscale=False, alpha=True)
    w.write(f, outrowlists)
    f.close()

    f = open('debug.png', 'wb')
    w = png.Writer(41*13, 64*4, greyscale=False, alpha=True)
    w.write(f, odbrowlists)
    f.close()
