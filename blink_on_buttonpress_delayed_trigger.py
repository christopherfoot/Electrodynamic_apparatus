# Blinking leds 
# https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/5
from machine import Pin, Timer
timer = Timer()
# assign Pins to 
pin10 = Pin(10, Pin.OUT)
pin11 = Pin(11, Pin.OUT)
pin12 = Pin(12, Pin.OUT)
pin13 = Pin(13, Pin.OUT)
# initialise
pin10.on()
pin11.off()
pin12.off()
pin13.on()
# define blinking = toggling at set frequency
def blink1(timer):
    pin10.toggle()
    pin11.toggle()
    pin12.toggle()
    pin13.toggle()
#    print(0.1+pin10.value(),-0.1+pin11.value(),pin12.value(),pin13.value())
     
#      
timer.init(freq=50., mode=Timer.PERIODIC, callback=blink1)

#def blink_1Hz(timer):
#for i in range(100):
#       led10.on()
#       timer.sleep(0.5)
#       led10.off()
#       timer.sleep(0.5)