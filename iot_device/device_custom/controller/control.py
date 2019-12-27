#!/usr/bin/python3
# This file is the main controller script

# Imports
import os
import sys
import speech_recognition as sr
from graphics import *

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

def sendAdd(cmd):
    # Opens new window to ask the user for input about the new code
    codeWindow = GraphWin("Add button", 500, 375)
    
    # Add entry points
    codeName = Entry(Point(250, 15), 53)
    codeName.setText("Button name")
    codeName.draw(codeWindow)

    # Add record button
    codeRecord = Rectangle(Point(15, 35), Point(470, 55))
    codeRecord.setFill("white")
    codeRecordText = Text(codeRecord.getCenter(), "Record button")
    codeRecord.draw(codeWindow)
    codeRecordText.draw(codeWindow)

    # Wait for button press
    while True:
        # Get position
        cPos = codeWindow.getMouse()
        x = cPos.getX()
        y = cPos.getY()

        # Check for button press
        xPos1 = codeRecord.getP1().getX()
        yPos1 = codeRecord.getP1().getY()
        xPos2 = codeRecord.getP2().getX()
        yPos2 = codeRecord.getP2().getY()

        # Compare data
        if x > xPos1 and x < xPos2:
            if y > yPos1 and y < yPos2:
                # Its been pressed
                break

    # Tell device to listen
    device.give("route rfcontrol add_code " + codeName.getText().replace(" ", "_"))
    res = device.take()

    # End if it doesnt work
    if res != "sent": return

    # Notify the user
    codeName.undraw()
    codeRecord.move(0, -20)
    codeRecordText.move(0, -20)
    codeRecordText.setText("Press the button you with to clone")

    # Wait for the testing code
    device.take()
    codeRecordText.setText("Code found! Button will be resent in 5 seconds. Did it work?")

    # Accept function
    def buttonAccept(cmd):
        if cmd == "Yes":
            device.give("route rfcontrol accepted")
            device.take()
        else:
            device.give("route rfcontrol denied")
            device.take()

    # Add yes or no button
    yesButton = screen.Push("Yes", buttonAccept, False)
    noButton = screen.Push("No", buttonAccept, False)
    yesButton.setPos(15, 45)
    noButton.setPos(15, 100)
    yesButton.draw(codeWindow)
    noButton.draw(codeWindow)

    # Check the button press
    while True:
        # Get position
        cPos = codeWindow.getMouse()
        x = cPos.getX()
        y = cPos.getY()

        # Check for button press
        xPos1 = yesButton.shape.getP1().getX()
        yPos1 = yesButton.shape.getP1().getY()
        xPos2 = yesButton.shape.getP2().getX()
        yPos2 = yesButton.shape.getP2().getY()

        # Compare data
        if x > xPos1 and x < xPos2:
            if y > yPos1 and y < yPos2:
                # Its been pressed
                yesButton.use()
                break

        # Check for button press
        xPos1 = noButton.shape.getP1().getX()
        yPos1 = noButton.shape.getP1().getY()
        xPos2 = noButton.shape.getP2().getX()
        yPos2 = noButton.shape.getP2().getY()

        # Compare data
        if x > xPos1 and x < xPos2:
            if y > yPos1 and y < yPos2:
                # Its been pressed
                noButton.use()
                break

    # Close window
    codeWindow.close()

def shutdown(cmd):
    # Closes program and turns off computer
    device.stop()
    sys.exit(0)

# Main
def main():
    # Start IOT
    device.start()

    # Initializze screen and buttons
    s = screen.Screen(1280, 720)
    sendAdd("X")

    # Function buttons
    addCodeButton = screen.Push("Add", sendAdd, False)
    addCodeButton.setPos(s.window.getWidth() - 180, 10)
    s.addButton(addCodeButton)
    
    addCodeButton = screen.Push("Shutdown", shutdown, False)
    addCodeButton.setPos(s.window.getWidth() - 90, 10)
    s.addButton(addCodeButton)

    # Buttons
    s.addButton(screen.Toggle("Lights", lightsOn, lightsOff))

    # Button press loop
    while True:
        s.press()

# Call main function
main()