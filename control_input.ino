// This version writes to the circuit electronics but doesnt have the reading back

#include <TimeLib.h>
String incomingString;

int t;
int cycles;
float duty_cycle;
int freq;
int str;


void setup() {
  Serial.begin(115200);
  pinMode(7, OUTPUT);
  pinMode(4, OUTPUT);
  digitalWrite(7, LOW);
  digitalWrite(4,LOW);
  delay(500);
}

void loop() {
  if (Serial.available() > 0) {
    incomingString = Serial.readString();
    str = incomingString.toInt();
    static int freq;
    
    
  }
  freq = str - 10000;
  t = 500000 / freq;
  

  if ( (freq > 0) && (freq<50)) {
    float tprime= t/1000;
    digitalWrite(7, HIGH);
    delay(tprime);

    digitalWrite(7, LOW);
    delay(tprime);
  } 
  else if (freq >= 50) {
    digitalWrite(7, HIGH);
    delayMicroseconds(t);

    digitalWrite(7, LOW);
    delayMicroseconds(t);
  }

  else if (freq < 0) {
    digitalWrite(7, LOW);
    digitalWrite(4, HIGH);

  }
}
