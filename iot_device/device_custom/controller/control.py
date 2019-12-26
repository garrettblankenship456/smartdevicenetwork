#!/usr/bin/python3
# This file is the main controller script

# Imports
import os
import sys
import speech_recognition as sr

# Class imports
import screen
sys.path.insert(0, "../..")
import iot # pylint: disable=import-error

# Initialize IOT device
device = iot.IOT("controller", "192.168.1.97", 5623)

# Functions
def lightsOn(cmd):
    # Sends lights on command to rf controller
    device.give("route rfcontrol send_code on")
    return device.take() == "sent"

def lightsOff(cmd):
    # Send lights off command to rf controller
    device.give("route rfcontrol send_code off")
    return device.take() == "sent"

# Main
def main():
    # Start IOT
    device.start()

    # Initializze screen and buttons
    s = screen.Screen(1280, 720)
    s.addButton(screen.Toggle("Lights", lightsOn, lightsOff))

    # Button press loop
    while True:
        s.press()

# Call main function
main()