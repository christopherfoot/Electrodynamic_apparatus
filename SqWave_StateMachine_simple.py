# Prog PIO
# https://docs.micropython.org/en/latest/rp2/quickref.html
# operates at freq/2000 (for freq >100MHz - test) 
from machine import Pin
import rp2

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink_twothou():
    # Default: Cycles: 1 + 7 + 32 * (30 + 1) = 1000
    # Cycles: 1 + 7 + 32 * (20 + 1) = 1000 - 10*32 
    set(pins, 1)
    set(x, 21)                  [6]
    label("delay_high")
    nop()                       [29]
    jmp(x_dec, "delay_high")

    # Default: Cycles: 1 + 7 + 32 * (30 + 1) = 1000
    # Cycles: 1 + 7 + 32 * (40 + 1) = = 1000 - 10*32 
    set(pins, 0)
    set(x, 41)                  [6]
    label("delay_low")
    nop()                       [29]
    jmp(x_dec, "delay_low")

# Create and start a StateMachine with blink_..., outputting on Pin(10) - changed from 25 in example
sm = rp2.StateMachine(0, blink_twothou, freq=2000000, set_base=Pin(10))
sm.active(1)