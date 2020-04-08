// Cribbage mockup - for ESP32 and Adafruit 2.8" display https://www.adafruit.com/product/1770
// in spi mode. Version 2.2.0 of TFT_eSPI (and prolly some updates)
// Run the rip with rotation of 1 
// python ../../../ConvertPngToTFT.py -r1 Cribmock2serpNSuch.png cribmock > cribmock.h

// WIRING DIAGRAM!

// If using the adafruit 2.8" and the IM1, IM2, IM3 jumpers on the board are not soldered, need to do:

// display wiring:
// IM1 - 3Vo pin on display
// IM2 - "
// IM3 - "

//SPI Mode Jumpers
//Before you start, we'll need to tell the display to put us in SPI mode so it will know which pins to listen to. 
// To do that, we have to connect tbe IM1, IM2 and IM3 pins to 3.3V. The easiest way to do that is to solder closed the IMx 
// jumpers on the back of the PCB. Turn over the PCB and find the solder jumpers  With your soldering iron, melt solder to 
// close the three jumpers indicated IM1 IM2 and IM3 (do not solder closed IM0!)
// If you really don't want to solder them, you can also wire the breakout pins to the 3vo pin, just make sure you don't tie 
// them to 5V by accident! For that reason, we suggest going with the solder-jumper route.

// display stuff - all of these to the pin of the same name on the display
//#define TFT_MISO 19 
//#define TFT_MOSI 23
//#define TFT_SCLK 18
//#define TFT_CS   5  // Chip select control pin

//then other pins
//#define TFT_DC    21  // Data Command control pin
//#define TFT_RST   4  // Reset pin (could connect to RST pin)
//#define TFT_BL   22  // LED back-light

//Then of course the gnd to gnd and Vin to 3.3V

// And at some point there'll be buttons and stuff, if this evolves into the game

//based upon

//TFT_graphicstest_PDQ_SeantwAda320 - TFT_eSPI test, SPI, adafruit 2.8" ILI9341 LCD with either SPI or parallel
//320x240
//based on:
//SEAN'S THING THAT GOT THE TINY SMOL TFT 240x240 TO WORK WITH HW SPI by doing it the way other people did it!
//it was not entirely clear what they did, I thought.
//but here we are.
//and I'm developing a tool to rip png to the rgb format this thing likes to see how fast I can blit a bitmap.
//occurs that this windowing thing the ILI chips do will be most helpy

/*
 Adapted from the Adafruit and Xark's PDQ graphicstest sketch.

 See end of file for original header text and MIT license info.
 
 This sketch uses the GLCD font only.

 Make sure all the display driver and pin comnenctions are correct by
 editting the User_Setup.h file in the TFT_eSPI library folder.

 #########################################################################
 ###### DON'T FORGET TO UPDATE THE User_Setup.h FILE IN THE LIBRARY ######
 #########################################################################
 */

#include "SPI.h"
#include "TFT_eSPI.h"


//can you do this? before, sketch used 243056 bytes - 552616 after! Looks worky - but that gets us to 42% of program storage space.
//- can we wind that up? Is the rest OS stuff or something?
//- adding OTA to that is pretty hopeless
//- SPIFFS, if nothing else, I guess
//- in the SNES days we had VRAM
//- perhaps I can compile out all the stuff I don't need from TFT_eSPI - have a look in the chunky chunky example setup header
//- fonts should save a bit, let's go get rid of them, pulling out all but the default adafruit font = 530264, so 22,352 bytes savings!
//  enough for a ~149x149 8-bit image! or 349 8-bit tile images! gobs of 16-color! hideYOBS of 2-color! which amounts to fonts.
//  could do my own speshul 16-color fonts with tiles like we did in the snes dez, give it that nice sheen
//if the files change they don't automatically reload in the Ardy IDE but it does seem to compile from the newest one
//there may be compilation slowness incurred by this, look into
//#include "data/dogs240.h"
//#include "data/Ent240.h"
//#include "data/leaf240.h"
#include "data/cribmock.h"

// Let's see if we can allocate a RAM buffer for a 240x240x2 byte blit
// not seeing it come off the RAM of 13716 bytes
// Drat, we get the dram0_0_seg overflowed by 4344 bytes
// which puts us like 9 lines short.
// let's do 200x200 and blit the leaf 4 times
// or let's do 240*120 and blit the same half a picture twice or whatever
uint16_t blitBuffer[240*160];

// Use hardware SPI
TFT_eSPI tft = TFT_eSPI();

unsigned long total = 0;
unsigned long tn = 0;
void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println(""); Serial.println("");
  Serial.println("Bodmer's TFT_eSPI library Test!"); 
 
  tft.init();

  //sean adds bc rotation might be a problem?
  tft.setRotation(0);   // ew rotation 2 was physically preferable but viewing angle was hideorrible - rot 1 works great for landscape mode with no other changes
}

void loop(void)
{

	Serial.println(F("Benchmark                Time (microseconds)"));

  //RAM image is faster, so let's use that
  //uint32_t usecImage = testImage();
  //Serial.print(F("Image test               "));
  //Serial.println(usecImage);
  //delay(100);

  uint32_t usecRAMImage = testRAMImage();
  Serial.print(F("RAM Image test           "));
  Serial.println(usecRAMImage);
  delay(100000);
}

static inline uint32_t micros_start() __attribute__ ((always_inline));
static inline uint32_t micros_start()
{
	uint8_t oms = millis();
	while ((uint8_t)millis() == oms)
		;
	return micros();
}

/*
uint32_t testImageSub(const uint16_t *pixels,int32_t w,int32_t h) 
{
  uint32_t start = micros_start();

  //center! 
  int32_t leftMargin = (tft.width()/2) - (w/2);
  int32_t topMargin = (tft.height()/2) - (h/2);
  tft.pushImage(leftMargin, topMargin, w, h, pixels);
  uint32_t t = micros() - start;
  delay(1111);
  return t;
}

uint32_t testImage() {
  uint32_t totalTime = 0;

  tft.fillScreen(TFT_BLUE); //clear screen for cleanliness on 320
  //totalTime += testImageSub(choggles, choggles_w, choggles_h);
  //totalTime += testImageSub(loggles, loggles_w, loggles_h);
  //totalTime += testImageSub(goggles, goggles_w, goggles_h);
  totalTime += testImageSub(cribmock, cribmock_w, cribmock_h);
  return totalTime;
}
*/
uint32_t testRAMImageSub(const uint16_t *pixels,int32_t w,int32_t h) 
{
  
  //NOTE THAT WE DO NOT COUNT THE TIME TO COPY FROM FLASH TO RAM unless this comes after the start assignment
  memcpy(blitBuffer,pixels,w*h);    //half the image; whole thing would need w*h*2

  //now try it
  uint32_t start = micros_start();
  uint32_t t = 0;

  //center! 
  int32_t leftMargin = (tft.width()/2) - (w/2);
  int32_t topMargin = (tft.height()/2) - (h/2);
  //top half
  tft.pushImage(leftMargin, topMargin, w, h/2, (const uint16_t *)blitBuffer);
  //bottom half, nother copy of the same - no wait let's try other half copy from flash
  t = micros() - start;   //don't count flash->RAM copy time
  memcpy(blitBuffer,&(pixels[w*h/2]),w*h);    //bottom half of the image
  start = micros_start();
  tft.pushImage(leftMargin, topMargin+h/2, w, h/2, (const uint16_t *)blitBuffer);
  t += micros() - start;
  delay(1111);
  return t;
}


uint32_t testRAMImage() {
  uint32_t totalTime = 0;

  //try clearing screen with the bg color of the mockup, maybe that'll make the drawing a bit less noticeable
  //not really, but wev.
  tft.fillScreen(0xe313); //was TFT_BLACK); //clear screen for cleanliness on 320
  //totalTime += testRAMImageSub(choggles, choggles_w, choggles_h);
  //totalTime += testRAMImageSub(loggles, loggles_w, loggles_h);
  //totalTime += testRAMImageSub(goggles, goggles_w, goggles_h);
  totalTime += testRAMImageSub(cribmock, cribmock_w, cribmock_h);
  return totalTime;
}



/***************************************************
  Original sketch text:

  This is an example sketch for the Adafruit 2.2" SPI display.
  This library works with the Adafruit 2.2" TFT Breakout w/SD card
  ----> http://www.adafruit.com/products/1480
 
  Check out the links above for our tutorials and wiring diagrams
  These displays use SPI to communicate, 4 or 5 pins are required to
  interface (RST is optional)
  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.
  MIT license, all text above must be included in any redistribution
 ****************************************************/
 
