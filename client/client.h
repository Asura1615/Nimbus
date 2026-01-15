#include <FastLED.h>

class LedStrip{
  int start;
  int end;
  int stripId;
  CRGB *leds;

  public:
    LedStrip(CRGB *leds, int stripId, int start, int end){
        this -> stripId = stripId;
        this -> start = start-1;
        this -> end = end -1;
        this -> leds = leds;

        for (int i =start; i < end; i++){
          this ->leds[i] = CRGB::Black;
        }
        FastLED.show();
    }

    void powerON(){
      for (int i = this -> start; i < this -> end; i++){
        this -> leds[i] = CRGB::White;
      }
    }

    void powerOFF(){
      for (int i = this -> start; i < this -> end; i++){
        this -> leds[i] = CRGB::Black;
      }
    }
};