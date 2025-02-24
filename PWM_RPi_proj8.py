# https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/7

from machine import Pin, PWM
from time import sleep

pwm10 = PWM(Pin(10))
pwm11 = PWM(Pin(11))
pwm12 = PWM(Pin(12))
pwm13 = PWM(Pin(13))

pwm10.freq(10)
pwm11.freq(10)
pwm12.freq(10)
pwm13.freq(10)

while True:
    for duty in range(65025):
#       duty = 60000
         pwm10.duty_u16(duty)
         sleep(.001)
#    for duty in range(65025, 0, -1):
#        pwm11.duty_u16(duty)
#        sleep(0.0001)
#    for duty in range(65025):
#        pwm12.duty_u16(duty)
#        sleep(0.0001)
#    for duty in range(65025, 0, -1):
#        pwm13.duty_u16(duty)
#        sleep(0.0001)