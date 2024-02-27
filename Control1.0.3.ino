// This version writes to the circuit electronics, includes power control

//Author: Francesco Straniero
//Date: 26/02/2024


#include <TimeLib.h>
String incomingString;

int t;
int duty_cycle;
int freq;
String str;
int ttl;
int voltage;
int voltage_1000;
int voltage_100;
int voltage_10;
int voltage_1;
int lolol;
int freq_1000;
int freq_100;
int freq_10;
int freq_1;


void setup() {
  Serial.begin(115200);
  pinMode(7, OUTPUT);   //clock pin
  pinMode(4, OUTPUT);   //ttl pin
  pinMode(10, OUTPUT);  //voltage pin
  digitalWrite(7, LOW);
  digitalWrite(4, LOW);
  digitalWrite(10, LOW);
  delay(500);
}

void loop() {

  // This next if loop reads the Serial only if there is any communication available and creates a static variable which doesnt change until new communications come
  //this is very important for two reasons: 1) the variable values is kept through loops; 2)this is memory efficient.
  if (Serial.available() > 0) {
    incomingString = Serial.readString();
    str = incomingString.toInt();
    static int voltage;
    static int freq;
    static int ttl;
    static int lolol;
  }
  ttl = String(str.charAt(0)).toInt();
  freq_1000 = String(str.charAt(1)).toInt();
  freq_100 = String(str.charAt(2)).toInt();
  freq_10 = String(str.charAt(3)).toInt();
  freq_1 = String(str.charAt(4)).toInt();
  freq = 1000 * freq_1000 + 100 * freq_100 + 10 * freq_10 + freq_1;
  voltage_1000 = String(str.charAt(5)).toInt();
  voltage_100 = String(str.charAt(6)).toInt();
  voltage_10 = String(str.charAt(7)).toInt();
  voltage_1 = String(str.charAt(8)).toInt();
  voltage = 1000 * voltage_1000 + 100 * voltage_100 + 10 * voltage_10 + voltage_1;
  t = 500000 / freq;
  lolol = (255 * voltage) / 100;
  duty_cycle = truncf(lolol);

  while (true) {
    if (Serial.available()>0){
      break;
    }

    if (ttl == 0) {
      digitalWrite(7, LOW);
      digitalWrite(4, HIGH);
      digitalWrite(10, LOW);
    }

    if (ttl == 1) {
      analogWrite(10, duty_cycle);

      if ((freq > 0) && (freq < 50)) {
        float tprime = t / 1000;
        digitalWrite(7, HIGH);
        delay(tprime);

        digitalWrite(7, LOW);
        delay(tprime);

      } else if (freq >= 50) {
        digitalWrite(7, HIGH);
        delayMicroseconds(t);

        digitalWrite(7, LOW);
        delayMicroseconds(t);
      }
    }
  }
}
