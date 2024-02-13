#include <TimeLib.h>
#include <math.h>
int signal;
int static_variable = 500;
int gnd;
int osc;
int diff;
float counter;
int previous_freq;
int current_freq;

float read_freq;

void setup() {
  Serial.begin(115200);
  counter = 1;
}

void loop() {

  previous_freq = current_freq;  //takes the last frequency reading

  while (true) {
    gnd = analogRead(A1);
    osc = analogRead(A0);
    diff = abs(osc - gnd);
    if (diff > 700) {
      counter++;  //this adds to the counter every 10micro sec
      delayMicroseconds(10);
    }
    if (diff < 700) {
      break;
    }
  }
  current_freq = truncf (100000 / (2 * counter));
  if (previous_freq != current_freq) {
    Serial.println(current_freq);
  }
  counter = 1;
}
