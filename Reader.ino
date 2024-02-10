#include <TimeLib.h>

int signal;
int static_variable = 500;
int gnd;
int osc;
int diff;
int counter;

void setup() {
  Serial.begin(115200);
  counter = 0;
}

void loop() {
  for (int i = 0; i <= 100000; i++) {
    gnd = analogRead(A1);
    osc = analogRead(A0);
    diff = abs(osc - gnd);
    if (diff > 700) {
      counter++;
    }
    
    delayMicroseconds(10);
  }
  Serial.write(counter);
  counter =0;
}