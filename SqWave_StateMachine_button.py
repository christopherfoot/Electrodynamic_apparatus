from machine import Pin
import rp2
# pull up resistor - 10k, and 1k to ground? built-in one insufficient
# Define the PIO program for blinking LED at 1Hz
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink_twothou():
    # Default: Cycles: 1 + 7 + 32 * (30 + 1) = 1000
    # Cycles: 1 + 7 + 32 * (20 + 1) = 1000 - 10*32 
    set(pins, 1)
    set(x, 31)                  [6]
    label("delay_high")
    nop()                       [29]
    jmp(x_dec, "delay_high")

    # Default: Cycles: 1 + 7 + 32 * (30 + 1) = 1000
    # Cycles: 1 + 7 + 32 * (40 + 1) = = 1000 - 10*32 
    set(pins, 0)
    set(x, 31)                  [6]
    label("delay_low")
    nop()                       [29]
    jmp(x_dec, "delay_low")

# Create and start a StateMachine with blink_..., outputting on Pin(10) - changed from 25 in example
sm = rp2.StateMachine(0, blink_twothou, freq=2000000, set_base=Pin(10))

# Define the button pin
button_pin = Pin(14, Pin.IN, Pin.PULL_UP)  # Assuming the button is connected to pin 14

# Function to start the state machine
def start_state_machine(pin):
    if not pin.value():  # Check if the button is pressed
        sm.active(1)     # Start the state machine

# Attach interrupt handler to the button pin
button_pin.irq(trigger=Pin.IRQ_FALLING, handler=start_state_machine)
# start on falling edge. responds without continuous polling of button
# debounce with 0.1 uF ceramic cap. see RP circuit examples