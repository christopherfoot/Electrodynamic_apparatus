# Python method - NOT accurate = see jitter (interrupts?) on scope. Less precise freq. than StateMachine
# Tested on scope with period = 500 us -> 980 Hz +/- 10 cf. StateMachine = +/- 0.1 Hz
# Maybe why prog wants to start a separate thread - that doesn't fix the issue  
import machine
import time
import _thread

# Define pin numbers
# button_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
output_pin = machine.Pin(10, machine.Pin.OUT)

# Define square wave parameters
# frequency = 1000  # Adjust as needed
# period = 1 / frequency
# period = 500

# Function to generate square wave
def generate_square_wave():
     period = 5000
     while True:
        output_pin.on()
        time.sleep_us(period)
        output_pin.off()
        time.sleep_us(period)

# Start square wave generation in a separate thread
# square_wave_thread = _thread(target=generate_square_wave)
square_wave_thread = _thread.start_new_thread(generate_square_wave, ())
# square_wave_thread.start()

# Check button state and stop square wave if pressed
# while True:
 #   if button_pin.value() == 1:
  #       square_wave_thread.terminate()  # Terminate square wave generation thread
    #   break  # Exit loop
    #time.sleep(0.1)  # Add a small delay to avoid busy waiting