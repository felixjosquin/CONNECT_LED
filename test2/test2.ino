#include <Adafruit_NeoPixel.h>
#define PIN 6
#define NUMPIXELS  10
#define n_step 10
#define pause 3000
#define di 0.1

float in = 1;

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
int r0[NUMPIXELS] ;
int g0[NUMPIXELS] ;
int b0[NUMPIXELS] ;
int r1[NUMPIXELS] ;
int g1[NUMPIXELS] ;
int b1[NUMPIXELS] ;



int value() {
  while (Serial.available() < 2) {
  }
  int x1 = Serial.read();
  int x2 = Serial.read();
  return f(x1) * 16 + f(x2);
}


int f(int x) {
  if (x > 90) {
    return x - 87;
  }
  else {
    return x - 48;
  }
}



void setup() {
  Serial.begin(9600);
  pixels.begin();
  for (int j = 0; j < NUMPIXELS; j++) {
    r0[j] = 0;
    g0[j] = 0;
    b0[j] = 0;
  }
}
void loop() {
  if (Serial.available() > 0) {
    if (Serial.peek() == 99) {
      Serial.read();
      for (int j = 0; j < NUMPIXELS; j++) {
        r1[j] = value();
        g1[j] = value();
        b1[j] = value();
      }
      show ();
      for (int j = 0; j < NUMPIXELS; j++) {
        r0[j] = r1[j];
        g0[j] = g1[j];
        b0[j] = b1[j];
      }
    }
    else if (Serial.peek() == 105) {
      Serial.read();
      while (Serial.available() < 1) {
      }
      if (Serial.peek() == 43 && in + di <= 1) {
        Serial.read();
        in = in + di;
      }
      if (Serial.peek() == 45 && in  > 0) {
        Serial.read();
        in = in - di;
      }
    }
    else {
      Serial.read();
    }
  }
}

void show () {
  for (int k = 1; k <= n_step; k++) {
    for (int j = 0; j < NUMPIXELS; j++) {
      float dr = (r1[j] - r0[j]) / n_step;
      float dg = (g1[j] - g0[j]) / n_step;
      float db = (b1[j] - b0[j]) / n_step;
      pixels.setPixelColor(j, pixels.Color(round((r0[j] + k * dr)*in), round((g0[j] + k * dg)*in), round ((b0[j] + k * db)*in)));
    }
    pixels.show();
    delayMicroseconds(round(pause / n_step));
  }
  for (int j = 0; j < NUMPIXELS; j++) {
    pixels.setPixelColor(j, pixels.Color(round(r1[j] * in), round(in * g1[j]), round(in * b1[j])));
    pixels.show();
  }

}
