#!/usr/bin/python3
# This file is the main controller script

# Imports
import os
import sys
import json
import speech_recognition as sr
from graphics import *

# Class imports
import screen
sys.path.insert(0, "../..")
import iot # pylint: disable=import-error

# Initialize IOT device
device = iot.IOT("controller", "192.168.1.97", 5623)

# Functions
def getCodes():
    # Returns all the codes in the json
    dataFile = open("codes.json", "r")
    data = dataFile.read()
    data = json.loads(data)

    dataFile.close()

    return data

def writeCodes(data:dict):
    # Writes the data to the json file
    dataFile = open("codes.json", "w")
    data = json.dumps(data)
    
    dataFile.write(data)
    dataFile.close()

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

    # Get the id of the code, which is what the command will be stored as
    codeID = codeName.getText().replace(" ", "_")
    
    # Tell device to listen
    device.give("route rfcontrol add_code " + codeID)
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
            # Tell device to save the code
            device.give("route rfcontrol accepted")
            device.take()

            # Save the code on the controller
            codes = getCodes()
            codes[codeID] = "Toggle"
            writeCodes(codes) 
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

def keypress(cmd):
    # Send the id to the controller
    device.give("route rfcontrol send_code " + cmd.replace(" ", "_"))
    return device.take() == "sent"

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

    # Function buttons
    addCodeButton = screen.Push("Add", sendAdd, False)
    addCodeButton.setPos(s.window.getWidth() - 180, 10)
    s.addButton(addCodeButton)
    
    addCodeButton = screen.Push("Shutdown", shutdown, False)
    addCodeButton.setPos(s.window.getWidth() - 90, 10)
    s.addButton(addCodeButton)

    # Buttons
    # Read data from codes file
    codes = getCodes()

    # Loop over each code and make a button
    for key in codes:
        if codes[key] == "Toggle":
            s.addButton(screen.Toggle(key, keypress, keypress))
        elif codes[key] == "Push":
            s.addButton(screen.Push(key, keypress))

    # Button press loop
    while True:
        s.press()

# Call main function
main()