#include "MCUFRIEND_kbv.h"
MCUFRIEND_kbv tft;

#define LOWFLASH (defined(__AVR_ATmega328P__) && defined(MCUFRIEND_KBV_H_))

#include "bitmap_RGB.h"

#define BLACK   0x0000
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF
#define GREY    0x8410
#define ORANGE  0xE880

void setup()
{
    Serial.begin(9600);
    uint16_t ID = tft.readID();

    Serial.print(F("ID = 0x"));
    Serial.println(ID, HEX);

    Serial.println(F("GFX drawBitmap() plots one mono pixel at a time"));
    Serial.println(F("it defaults to transparent plotting"));
    Serial.println(F("unless you specify foreground and background colours"));
    Serial.println(F("it can plot a monochrome bitmap from Flash or SRAM"));

    Serial.println(F(""));
    Serial.println(F("GFX drawGrayscaleBitmap() is not relevant for OLED, TFT"));
    Serial.println(F("GFX drawRGBBitmap() plots one colour pixel at a time"));
    Serial.println(F("from Flash or SRAM and with a monochrome transparent bitmask"));
    Serial.println(F(""));
    Serial.println(F("Using the hardware pushColors() methods is faster"));
    Serial.println(F("pushColors() expects uint16 array in SRAM"));
    Serial.println(F("for any runtime generated images"));
    Serial.println(F("but it expects uint8_t array of serialised bytes in Flash"));
    Serial.println(F(""));

    Serial.println(F("Colour TFTs are natively big-endian"));
    Serial.println(F("Many microcontrollers and Tools are little-endian"));
    Serial.println(F("you can use the optional argument to select big-end"));
    tft.begin(ID);
}

void msg_time(int x, int y, String msg, uint32_t t)
{
    t = millis() - t;
    tft.setCursor(x, y);
    tft.print(msg);
    tft.print(t);
    tft.print(F("ms"));
}

void loop(void)
{
    int x = 5, y, w = 128, h = 64;
    uint32_t t;
    const int SZ = w * h / 8;
    uint8_t sram[SZ];

    tft.fillScreen(BLACK);
    y = 0; t = millis();
    tft.setAddrWindow(x, y, x + 64 - 1, y + 64 - 1);
    tft.pushColors((const uint8_t*)marilyn_64x64, 64 * 64, 1, false);
    tft.setAddrWindow(0, 0, tft.width() - 1, tft.height() - 1);
    msg_time(0, y + 66, F("pushColors() flash "), t);
    delay(10000);
}
