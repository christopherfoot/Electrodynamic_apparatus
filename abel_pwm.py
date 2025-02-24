import machine
import time

# Define pin numbers
# button_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
output_pin = machine.Pin(10, machine.Pin.OUT)

pwm = machine.PWM(output_pin, freq=50, duty_u16=8192)

pwm.init(freq=110000, duty_ns=5000)

for i in range(1000):
    pwm.duty_ns(i*9)
    time.sleep_us(5000)
    

