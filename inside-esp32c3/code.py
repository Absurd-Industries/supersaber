import time
import random
import board
import adafruit_dotstar as dotstar
import digitalio
from adafruit_debouncer import Debouncer, Button

pin = digitalio.DigitalInOut(board.D3)
switch = Button(pin, 1000, 2000, True)

# Using a DotStar Digital LED Strip with 30 LEDs connected to hardware SPI
dots = dotstar.DotStar(board.MOSI, board.SCK, 107, brightness=0.25)

POWER = False
NUMPIXELS = len(dots)
HUE = 0
PULSATING = False

COLORS = (
    (255, 25, 25),  #Pink Red
    (255, 15, 0), #Blood Orange
    (255, 180, 0), #Gold
    (70, 255, 0), #Lime
    (0, 255, 60), #Mint Green
    (0, 140, 255), #Sky Blue
    (0, 0, 255), #Blue 
    (220, 0, 255), #Magenta
    (255, 0, 0) #Red
)

def power_on():
    global HUE, POWER, NUMPIXELS
    for dot in range(NUMPIXELS):
        dots[dot] = COLORS[HUE]
        dots.show()
        time.sleep(0.006)
    POWER = True

def power_off():
    global NUMPIXELS, POWER
    if POWER:
        for dot in range(NUMPIXELS - 1, -1, -1):
            dots[dot] = (0, 0, 0)
            dots.show()
            time.sleep(0.006)
        POWER = False
    else:
        return

def change_color():
    global HUE
    if (HUE + 1) == len(COLORS):
        HUE = 0
    else: 
        HUE += 1

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


power_on()
while True:
    switch.update()
    if switch.long_press:
        print('Long Pressed!')
        if POWER: 
            power_off()
        else:
            power_on()
            
    if switch.short_count == 2:
        print('Double Pressed!')
        change_color()
        power_on()
    
    if switch.pressed:
        print('Pressed!')
    






