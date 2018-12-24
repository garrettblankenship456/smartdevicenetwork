#!/usr/bin/python3
# Script to control LED commands
import sys
import os
sys.path.insert(0, "..")
import iot

# Setup GPIO for output
os.system("gpio -g mode 18 out")

# Define functions
def led_on(args):
    print("LED on")
    os.system("gpio -g write 18 1")

def led_off(args):
    print("LED off")
    os.system("gpio -g write 18 0")

def led(args):
    print("LED control")

    if args[0] == "1":
        os.system("gpio -g write 18 1")
    elif args[0] == "0":
        os.system("gpio -g write 18 0")

# Setup device
device = iot.IOT("led_diode", "10.0.0.191", 5623) # Define the ID, first argument is IP, second argument is the port
device.start() # Start the connection to the IOT server

# Define functions with the device
device.defineCommand("led_on", led_on)
device.defineCommand("led_off", led_off)
device.defineCommand("led", led)

# Keep looping the take command so it doesnt quit
try: # Make sure to cleanly exit
    while True:
        device.takeCommand() # Wait until a command has been sucessfully ran
except KeyboardInterrupt:
    print("Clean exit!")

os.system("gpio -g write 18 0") # Turn off LED after exitting
device.stop() # Stop the command to the IOT server
