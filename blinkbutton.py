# https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/3
# Thonny on PC or RPi 

from machine import Pin
import time

led10 = Pin(10, Pin.OUT)
led11 = Pin(11, Pin.OUT)
led12 = Pin(12, Pin.OUT)
led13 = Pin(13, Pin.OUT)
button =  Pin(14, Pin.IN, Pin.PULL_DOWN)
led10.on()
led11.off()
led13.off()
led12.on()
print(button.value())

while True:
    print(button.value())
    time.sleep(.1)
    if button.value():
        led10.toggle()
#       time.sleep(.5)
        led11.toggle()
        led12.toggle()
#        time.sleep(.5)
        led13.toggle()
#        time.sleep(1.5)