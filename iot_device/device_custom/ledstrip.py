# Script to control LCD commands
import sys
import os
from neopixel import *
from time import sleep
sys.path.insert(0, "..")
import iot

# Setup variables for pins
LED_COUNT = 58
LED_PIN = 21
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

# Initialize LED strip
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Define functions
def colorWipe(args):
    print("LEDs clearing")
    color = Color(int(args[0]), int(args[1]), int(args[2]))
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        sleep(0.1)
def ledOn(args):
    print("Turning on LEDS")
    color = Color(int(args[0]), int(args[1]), int(args[2]))
    for i in args[3:]:
        strip.setPixelColor(int(i), color)
	strip.show()
def clear(args):
    print("LEDs clearing")
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
	strip.show()

# Setup device
device = iot.IOT("iot_script_test", "10.0.0.191", 5623) # Define the ID, first argument is IP, second argument is the port
device.start() # Start the connection to the IOT server

# Define functions with the device
device.defineCommand("led", ledOn)
device.defineCommand("color", colorWipe)
device.defineCommand("clear", clear)

# Keep looping the take command so it doesnt quit
try: # Make sure to cleanly exit
    while True:
        device.takeCommand() # Wait until a command has been sucessfully ran
except KeyboardInterrupt:
    print("Clean exit!")


device.stop() # Stop the command to the IOT server
