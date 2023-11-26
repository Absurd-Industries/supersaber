import time
import random
import board
import neopixel
import digitalio
from adafruit_debouncer import Button

# Initialize the digital input pin connected to the button
pin = digitalio.DigitalInOut(board.D4)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP

# Set up the button with debouncing (to avoid misreads)
switch = Button(pin, 1000, 3000, False)

# Initialize the NeoPixel LED strip with 94 LEDs on pin D10
dots = neopixel.NeoPixel(board.D10, 94, brightness=0.65, auto_write=False)

# Global variables to manage the state of the lightsaber
POWER = False  # Lightsaber power status (Off by default)
NUMPIXELS = len(dots)  # Total number of LEDs on the strip
HUE = 0  # Current color index in the COLORS tuple
PULSATING = False  # Pulsating effect status; not used yet

# Define a tuple with RGB color codes for different hues
COLORS = (
    (0, 0, 255), #Blue 
    (255, 25, 25),  #Pink Red
    (255, 15, 0), #Blood Orange
    (255, 180, 0), #Gold
    (70, 255, 0), #Lime
    (0, 255, 60), #Mint Green
    (0, 140, 255), #Sky Blue
    (220, 0, 255), #Magenta
    (255, 0, 0) #Red
)

def power_on():
    """Function to turn on the lightsaber and light up the LEDs."""
    global HUE, POWER, NUMPIXELS
    for dot in range(NUMPIXELS):
        dots[dot] = COLORS[HUE]  # Set each LED to the current color
        dots.show()  # Update the LED strip
        time.sleep(0.008)  # Short delay for the power-on effect
    POWER = True
    print('Powering On!')

def power_off():
    """Function to turn off the lightsaber and turn off the LEDs."""
    global NUMPIXELS, POWER
    if POWER:  # Only run if the lightsaber is currently on
        for dot in range(NUMPIXELS - 1, -1, -1):
            dots[dot] = (0, 0, 0)  # Set each LED to off (black)
            dots.show()  # Update the LED strip
            time.sleep(0.008)  # Short delay for the power-off effect
        POWER = False
    else:
        return


def change_color():
    global HUE
    if (HUE + 1) == len(COLORS):
        HUE = 0
    else: 
        HUE += 1

# Not used for the moment
def pulsate():
    global HUE, NUMPIXELS, PULSATING
    if PULSATING == True:
        return

    window = 5
    PULSATING = True
    for i in range(NUMPIXELS):
        for w in range(1, window + 1):
            if (i + w) < NUMPIXELS:
                dots[i - w] = (50, 0, 0)
    
        for w in range(1, window + 1):
            if (i + w) < NUMPIXELS:
                if w < window:
                    color = random.randint(w * 15, w * 45)
                    dots[i + w] = (0, 0, color)
                elif w == window:
                    dots[i + w] = (0, 0, 255)
                else:
                    color = random.randint(w * 15, w * 45)
                    dots[i + w] = (0, 0, color)
    PULSATING = False


power_on() # Start with the lightsaber powered on

# TEST CODE
# rainbow = Rainbow(dots, speed=0.0001, period=1)
# TEST CODE

# Main loop to continuously check the button status
while True:
    switch.update() # Check the status of the button
    # rainbow.animate() 
    
    if switch.long_press:
        # Handle long press
        print('Long Pressed!')
        if POWER: 
            power_off()
        else:
            power_on()
            
    if switch.short_count == 2:
        # Handle double press
        print('Double Pressed!')
    
    if switch.pressed:
        # Handle single press
        print('Pressed!')
        change_color()
        power_on()