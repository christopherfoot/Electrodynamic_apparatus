// This version reads and calculates the trap frequency, and sends it to the UI, where it is displayed on the monitor.

//Author: Francesco Straniero
//Date: 03/03/2024


const int analogInputPin = A0; 
const int samplingInterval = 2000; // Sampling interval in ms

void setup() {
  pinMode(A0,INPUT);
  Serial.begin(115200); 
}

void loop() {
  unsigned long startTime = millis(); // Record the start time of the sampling interval
  int pulseCount = 1; // Initialize count, it is set to 1, so that when trap is off, the code doesn't have to divide by zero.

  // The way this code works is as follows: it counts how many peaks are in a 2 seconds interval, then calculates the frequency and sends it through the serial port to the UI.
  while (millis() - startTime < samplingInterval) {
    if (analogRead(analogInputPin) > 700) { 
      pulseCount++;
      while (analogRead(analogInputPin) > 700) {} 
    }
  }

  // calculate frequency
  float frequency = pulseCount/ (samplingInterval / 1000.0); // Convert pulse count to frequency (Hz)

  Serial.println(frequency);
  
}
