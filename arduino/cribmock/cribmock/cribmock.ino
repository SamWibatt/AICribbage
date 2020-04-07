// Cribbage mockup - for ESP32 and Adafruit 2.8" display https://www.adafruit.com/product/1770
// in spi mode. 

// WIRING DIAGRAM!

// display stuff - 
//#define TFT_MISO 19
//#define TFT_MOSI 23
//#define TFT_SCLK 18
//#define TFT_CS   5  // Chip select control pin

//then other pins
//#define TFT_DC    21  // Data Command control pin
//#define TFT_RST   4  // Reset pin (could connect to RST pin)
//#define TFT_BL   22  // LED back-light

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
#include "data/dogs240.h"
#include "data/Ent240.h"
#include "data/leaf240.h"

// Let's see if we can allocate a RAM buffer for a 240x240x2 byte blit
// not seeing it come off the RAM of 13716 bytes
// Drat, we get the dram0_0_seg overflowed by 4344 bytes
// which puts us like 9 lines short.
// let's do 200x200 and blit the leaf 4 times
// or let's do 240*120 and blit the same half a picture twice or whatever
uint16_t blitBuffer[240*120];

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

  uint32_t usecImage = testImage();
  Serial.print(F("Image test               "));
  Serial.println(usecImage);
  delay(100);

  uint32_t usecRAMImage = testRAMImage();
  Serial.print(F("RAM Image test           "));
  Serial.println(usecRAMImage);
  delay(100);

	uint32_t usecFillScreen = testFillScreen();
	Serial.print(F("Screen fill              "));
	Serial.println(usecFillScreen);
	delay(100);

	uint32_t usecText = testText();
	Serial.print(F("Text                     "));
	Serial.println(usecText);
	delay(100);

	uint32_t usecPixels = testPixels();
	Serial.print(F("Pixels                   "));
	Serial.println(usecPixels);
	delay(100);

	uint32_t usecLines = testLines(TFT_BLUE);
	Serial.print(F("Lines                    "));
	Serial.println(usecLines);
	delay(100);

	uint32_t usecFastLines = testFastLines(TFT_RED, TFT_BLUE);
	Serial.print(F("Horiz/Vert Lines         "));
	Serial.println(usecFastLines);
	delay(100);

	uint32_t usecRects = testRects(TFT_GREEN);
	Serial.print(F("Rectangles (outline)     "));
	Serial.println(usecRects);
	delay(100);

	uint32_t usecFilledRects = testFilledRects(TFT_YELLOW, TFT_MAGENTA);
	Serial.print(F("Rectangles (filled)      "));
	Serial.println(usecFilledRects);
	delay(100);

	uint32_t usecFilledCircles = testFilledCircles(10, TFT_MAGENTA);
	Serial.print(F("Circles (filled)         "));
	Serial.println(usecFilledCircles);
	delay(100);

	uint32_t usecCircles = testCircles(10, TFT_WHITE);
	Serial.print(F("Circles (outline)        "));
	Serial.println(usecCircles);
	delay(100);

	uint32_t usecTriangles = testTriangles();
	Serial.print(F("Triangles (outline)      "));
	Serial.println(usecTriangles);
	delay(100);

	uint32_t usecFilledTrangles = testFilledTriangles();
	Serial.print(F("Triangles (filled)       "));
	Serial.println(usecFilledTrangles);
	delay(100);

	uint32_t usecRoundRects = testRoundRects();
	Serial.print(F("Rounded rects (outline)  "));
	Serial.println(usecRoundRects);
	delay(100);

	uint32_t usedFilledRoundRects = testFilledRoundRects();
	Serial.print(F("Rounded rects (filled)   "));
	Serial.println(usedFilledRoundRects);
	delay(100);

	Serial.println(F("Done!"));

	uint16_t c = 4;
	int8_t d = 1;
	for (int32_t i = 0; i < tft.height(); i++)
	{
		tft.drawFastHLine(0, i, tft.width(), c);
		c += d;
		if (c <= 4 || c >= 11)
			d = -d;
	}
	
	tft.setCursor(0, 0);
	//tft.setTextColor(TFT_MAGENTA);
	tft.setTextSize(1);

 	//tft.println(F("   TFT_eSPI test"));

  /*
	tft.setTextSize(1);
	tft.setTextColor(TFT_WHITE);
	tft.println(F(""));
	tft.setTextSize(1);
	tft.println(F(""));
	tft.setTextColor(tft.color565(0x80, 0x80, 0x80));

	tft.println(F(""));
 */


	tft.setTextColor(TFT_GREEN);
	tft.println(F(" Benchmark               microseconds"));
	tft.println(F(""));
	tft.setTextColor(TFT_YELLOW);

  /*
	tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
	tft.print(F("HaD pushColor      "));
	tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
	printnice(usecHaD);
 */


  tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
  tft.print(F("Image test         "));
  tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
  printnice(usecImage);

  tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
  tft.print(F("RAM Image test     "));
  tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
  printnice(usecRAMImage);

	tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
	tft.print(F("Screen fill        "));
	tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
	printnice(usecFillScreen);

	tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
	tft.print(F("Text               "));
	tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
	printnice(usecText);

	tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
	tft.print(F("Pixels             "));
	tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
	printnice(usecPixels);

	tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
	tft.print(F("Lines              "));
	tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
	printnice(usecLines);

	tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
	tft.print(F("Horiz/Vert Lines   "));
	tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
	printnice(usecFastLines);

	tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
	tft.print(F("Rectangles         "));
	tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
	printnice(usecRects);

	tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
	tft.print(F("Rectangles-filled  "));
	tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
	printnice(usecFilledRects);

	tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
	tft.print(F("Circles            "));
	tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
	printnice(usecCircles);

	tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
	tft.print(F("Circles-filled     "));
	tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
	printnice(usecFilledCircles);

	tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
	tft.print(F("Triangles          "));
	tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
	printnice(usecTriangles);

	tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
	tft.print(F("Triangles-filled   "));
	tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
	printnice(usecFilledTrangles);

	tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
	tft.print(F("Rounded rects      "));
	tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
	printnice(usecRoundRects);

	tft.setTextColor(TFT_CYAN); tft.setTextSize(1);
	tft.print(F("Rounded rects-fill "));
	tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
	printnice(usedFilledRoundRects);

	tft.setTextSize(1);
	tft.setTextColor(TFT_GREEN); tft.setTextSize(1);
	tft.print(F("Benchmark Complete!"));

	delay(60 * 1000L);
}

void printnice(int32_t v)
{
	char	str[32] = { 0 };
	sprintf(str, "%lu", v);
	for (char *p = (str+strlen(str))-3; p > str; p -= 3)
	{
		memmove(p+1, p, strlen(p)+1);
		*p = ',';
		
	}
	while (strlen(str) < 10)
	{
		memmove(str+1, str, strlen(str)+1);
		*str = ' ';
	}
	tft.println(str);
}

static inline uint32_t micros_start() __attribute__ ((always_inline));
static inline uint32_t micros_start()
{
	uint8_t oms = millis();
	while ((uint8_t)millis() == oms)
		;
	return micros();
}

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
  totalTime += testImageSub(choggles, choggles_w, choggles_h);
  totalTime += testImageSub(loggles, loggles_w, loggles_h);
  totalTime += testImageSub(goggles, goggles_w, goggles_h);
  return totalTime;
}

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

  tft.fillScreen(TFT_BLACK); //clear screen for cleanliness on 320
  totalTime += testRAMImageSub(choggles, choggles_w, choggles_h);
  totalTime += testRAMImageSub(loggles, loggles_w, loggles_h);
  totalTime += testRAMImageSub(goggles, goggles_w, goggles_h);
  return totalTime;
}

uint32_t testFillScreen()
{
	uint32_t start = micros_start();
    // Shortened this tedious test!
		tft.fillScreen(TFT_WHITE);
		tft.fillScreen(TFT_RED);
		tft.fillScreen(TFT_GREEN);
		tft.fillScreen(TFT_BLUE);
		tft.fillScreen(TFT_BLACK);

	return (micros() - start)/5;
}

uint32_t testText()
{
	tft.fillScreen(TFT_BLACK);
	uint32_t start = micros_start();
	tft.setCursor(0, 0);
	tft.setTextColor(TFT_WHITE,TFT_BLACK);	tft.setTextSize(1);
	tft.println(F("Hello World!"));
	tft.setTextSize(2);
	tft.setTextColor(tft.color565(0xff, 0x00, 0x00));
	tft.print(F("RED "));
	tft.setTextColor(tft.color565(0x00, 0xff, 0x00));
	tft.print(F("GREEN "));
	tft.setTextColor(tft.color565(0x00, 0x00, 0xff));
	tft.println(F("BLUE"));
	tft.setTextColor(TFT_YELLOW); tft.setTextSize(2);
	tft.println(1234.56);
	tft.setTextColor(TFT_RED);		tft.setTextSize(3);
	tft.println(0xDEADBEEF, HEX);
	tft.setTextColor(TFT_GREEN);
	tft.setTextSize(5);
	tft.println(F("Groop"));
	tft.setTextSize(2);
	tft.println(F("I implore thee,"));
  tft.setTextColor(TFT_GREEN);
	tft.setTextSize(1);
	tft.println(F("my foonting turlingdromes."));
	tft.println(F("And hooptiously drangle me"));
	tft.println(F("with crinkly bindlewurdles,"));
	tft.println(F("Or I will rend thee"));
	tft.println(F("in the gobberwarts"));
	tft.println(F("with my blurglecruncheon,"));
	tft.println(F("see if I don't!"));
	tft.println(F(""));
	tft.setTextColor(TFT_MAGENTA);
	tft.setTextSize(6);
	tft.println(F("Woot!"));
	uint32_t t = micros() - start;
	delay(1111);
	return t;
}

uint32_t testPixels()
{
	int32_t	w = tft.width();
	int32_t	h = tft.height();

	uint32_t start = micros_start();
	tft.startWrite();
	for (uint16_t y = 0; y < h; y++)
	{
		for (uint16_t x = 0; x < w; x++)
		{
			tft.drawPixel(x, y, tft.color565(x<<3, y<<3, x*y));
		}
	}
	tft.endWrite();
  uint32_t t = micros() - start;
  delay(1111);
  return t;
}


uint32_t testLines(uint16_t color)
{
	uint32_t start, t;
	int32_t	x1, y1, x2, y2;
	int32_t	w = tft.width();
	int32_t	h = tft.height();

	tft.fillScreen(TFT_BLACK);

	x1 = y1 = 0;
	y2 = h - 1;

	start = micros_start();

	for (x2 = 0; x2 < w; x2 += 6)
	{
		tft.drawLine(x1, y1, x2, y2, color);
	}

	x2 = w - 1;

	for (y2 = 0; y2 < h; y2 += 6)
	{
		tft.drawLine(x1, y1, x2, y2, color);
	}

	t = micros() - start; // fillScreen doesn't count against timing

	tft.fillScreen(TFT_BLACK);

	x1 = w - 1;
	y1 = 0;
	y2 = h - 1;

	start = micros_start();

	for (x2 = 0; x2 < w; x2 += 6)
	{
		tft.drawLine(x1, y1, x2, y2, color);
	}

	x2 = 0;
	for (y2 = 0; y2 < h; y2 += 6)
	{
		tft.drawLine(x1, y1, x2, y2, color);
	}

	t += micros() - start;

	tft.fillScreen(TFT_BLACK);

	x1 = 0;
	y1 = h - 1;
	y2 = 0;

	start = micros_start();

	for (x2 = 0; x2 < w; x2 += 6)
	{
		tft.drawLine(x1, y1, x2, y2, color);
	}
	x2 = w - 1;
	for (y2 = 0; y2 < h; y2 += 6)
	{
		tft.drawLine(x1, y1, x2, y2, color);
	}
	t += micros() - start;

	tft.fillScreen(TFT_BLACK);

	x1 = w - 1;
	y1 = h - 1;
	y2 = 0;

	start = micros_start();

	for (x2 = 0; x2 < w; x2 += 6)
	{
		tft.drawLine(x1, y1, x2, y2, color);
	}

	x2 = 0;
	for (y2 = 0; y2 < h; y2 += 6)
	{
		tft.drawLine(x1, y1, x2, y2, color);
	}

	t += micros() - start;

	return t;
}

uint32_t testFastLines(uint16_t color1, uint16_t color2)
{
	uint32_t start;
	int32_t x, y;
	int32_t w = tft.width();
	int32_t h = tft.height();

	tft.fillScreen(TFT_BLACK);

	start = micros_start();

	for (y = 0; y < h; y += 5)
		tft.drawFastHLine(0, y, w, color1);
	for (x = 0; x < w; x += 5)
		tft.drawFastVLine(x, 0, h, color2);

	return micros() - start;
}

uint32_t testRects(uint16_t color)
{
	uint32_t start;
	int32_t n, i, i2;
	int32_t cx = tft.width() / 2;
	int32_t cy = tft.height() / 2;

	tft.fillScreen(TFT_BLACK);
	n = min(tft.width(), tft.height());
	start = micros_start();
	for (i = 2; i < n; i += 6)
	{
		i2 = i / 2;
		tft.drawRect(cx-i2, cy-i2, i, i, color);
	}

	return micros() - start;
}

uint32_t testFilledRects(uint16_t color1, uint16_t color2)
{
	uint32_t start, t = 0;
	int32_t n, i, i2;
	int32_t cx = tft.width() / 2 - 1;
	int32_t cy = tft.height() / 2 - 1;

	tft.fillScreen(TFT_BLACK);
	n = min(tft.width(), tft.height());
	for (i = n; i > 0; i -= 6)
	{
		i2 = i / 2;

		start = micros_start();

		tft.fillRect(cx-i2, cy-i2, i, i, color1);

		t += micros() - start;

		// Outlines are not included in timing results
		tft.drawRect(cx-i2, cy-i2, i, i, color2);
	}

	return t;
}

uint32_t testFilledCircles(uint8_t radius, uint16_t color)
{
	uint32_t start;
	int32_t x, y, w = tft.width(), h = tft.height(), r2 = radius * 2;

	tft.fillScreen(TFT_BLACK);

	start = micros_start();

	for (x = radius; x < w; x += r2)
	{
		for (y = radius; y < h; y += r2)
		{
			tft.fillCircle(x, y, radius, color);
		}
	}

	return micros() - start;
}

uint32_t testCircles(uint8_t radius, uint16_t color)
{
	uint32_t start;
	int32_t x, y, r2 = radius * 2;
	int32_t w = tft.width() + radius;
	int32_t h = tft.height() + radius;

	// Screen is not cleared for this one -- this is
	// intentional and does not affect the reported time.
	start = micros_start();

	for (x = 0; x < w; x += r2)
	{
		for (y = 0; y < h; y += r2)
		{
			tft.drawCircle(x, y, radius, color);
		}
	}

	return micros() - start;
}

uint32_t testTriangles()
{
	uint32_t start;
	int32_t n, i;
	int32_t cx = tft.width()/ 2 - 1;
	int32_t cy = tft.height() / 2 - 1;

	tft.fillScreen(TFT_BLACK);
	n = min(cx, cy);

	start = micros_start();

	for (i = 0; i < n; i += 5)
	{
		tft.drawTriangle(
			cx		, cy - i, // peak
			cx - i, cy + i, // bottom left
			cx + i, cy + i, // bottom right
			tft.color565(0, 0, i));
	}

	return micros() - start;
}

uint32_t testFilledTriangles()
{
	uint32_t start, t = 0;
	int32_t i;
	int32_t cx = tft.width() / 2 - 1;
	int32_t cy = tft.height() / 2 - 1;

	tft.fillScreen(TFT_BLACK);

	start = micros_start();

	for (i = min(cx,cy); i > 10; i -= 5) {
		start = micros_start();
		tft.fillTriangle(cx, cy - i, cx - i, cy + i, cx + i, cy + i,
			tft.color565(0, i, i));
		t += micros() - start;
		tft.drawTriangle(cx, cy - i, cx - i, cy + i, cx + i, cy + i,
			tft.color565(i, i, 0));
	}

	return t;
}

uint32_t testRoundRects()
 {
	uint32_t start;
	int32_t w, i, i2;
	int32_t cx = tft.width() / 2 - 1;
	int32_t cy = tft.height() / 2 - 1;

	tft.fillScreen(TFT_BLACK);
	
	w = min(tft.width(), tft.height());
	
	start = micros_start();

	for (i = 0; i < w; i += 6)
	{
		i2 = i / 2;
		tft.drawRoundRect(cx-i2, cy-i2, i, i, i/8, tft.color565(i, 0, 0));
	}

	return micros() - start;
}

uint32_t testFilledRoundRects()
{
	uint32_t start;
	int32_t i, i2;
	int32_t cx = tft.width() / 2 - 1;
	int32_t cy = tft.height() / 2 - 1;

	tft.fillScreen(TFT_BLACK);

	start = micros_start();

	for (i = min(tft.width(), tft.height()); i > 20; i -= 6)
	{
		i2 = i / 2;
		tft.fillRoundRect(cx-i2, cy-i2, i, i, i/8, tft.color565(0, i, 0));
	}

	return micros() - start;
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
 
