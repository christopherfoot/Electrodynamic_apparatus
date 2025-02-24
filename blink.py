# https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/5
from machine import Pin, Timer
timer = Timer()
led10 = Pin(10, Pin.OUT)
led11 = Pin(11, Pin.OUT)
led12 = Pin(12, Pin.OUT)
led13 = Pin(13, Pin.OUT)


def blink1(timer):
     led10.toggle()
     led11.toggle()
     led12.toggle()
     led13.toggle()
     
timer.init(freq=1535.25, mode=Timer.PERIODIC, callback=blink1)