//Monitor
"""
Author: Francesco Straniero
Date: 20/02/2024
"""
#include <TimeLib.h>
#include <math.h>

int gnd;
int osc;
int diff;

int freq;




void setup() {
  Serial.begin(115200);
  diff = 1; 
  delay(1000);
}

void loop() {
  //reads the difference in the analog pins 0-5V --> 0-1024
  //gnd is the ground pin, osc is the oscillating voltage pin
  gnd = analogRead(A1);
  osc = analogRead(A0);
  diff = abs(osc - gnd);
  if (diff >= 0) {

    Serial.println(diff);
    delayMicroseconds(500);
    diff = 1;
  }
  else{
    Serial.println(0);
  }
}
