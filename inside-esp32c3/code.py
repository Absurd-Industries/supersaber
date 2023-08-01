import time
import random
import board
import adafruit_dotstar as dotstar
import digitalio
from adafruit_debouncer import Debouncer

pin = digitalio.DigitalInOut(board.D3)
switch = Debouncer(pin)

# Using a DotStar Digital LED Strip with 30 LEDs connected to hardware SPI
dots = dotstar.DotStar(board.MOSI, board.SCK, 107, brightness=0.015)

NUMPIXELS = len(dots)
HUE = 0
PULSATING = False

colors = (
    (255, 0, 0), #Red
    (255, 150, 0), #YELLOW
    (255, 40, 0), #ORANGE
    (0, 255, 0), #GREEN
    (0, 255, 120), #TEAL
    (0, 255, 255), #CYAN
    (0, 0, 255), #BLUE
    (180, 0, 255), #PURPLE
    (255, 0, 20), #MAGENTA
    (255, 255, 255) #WHITE
)

def power_on():
    global HUE, NUMPIXELS
    # dots.fill((0, 0, 0))
    # dots.show()
    for dot in range(NUMPIXELS):
        dots[dot] = colors[HUE]
        dots.show()
        time.sleep(0.008)

def change_color():
    global HUE
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
    if switch.fell:
        change_color()
        power_on()
        print('pressed')
    else:
        NUMPIXELS = NUMPIXELS
        # print('not pressed')
    






