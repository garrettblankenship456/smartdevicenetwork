# Script to control LCD commands
import sys
import os
import Adafruit_CharLCD as LCD
sys.path.insert(0, "..")
import iot

# Setup variables for pins
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 4
lcd_columns = 16
lcd_rows = 2

# Initialize LCD
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
lcd.message("Initializing!")

# Define functions
def display(args):
    print("LCD command: ", args)
    msg = " ".join(args)
    lcd.clear()
    lcd.message(msg)
def clear(args):
    print("LCD clearing")
    lcd.clear()
def move(args):
    print("LCD shifting")
    if len(args) < "1":
        return False
    if args[0] != "-1" or args[0] != "1":
        return False

    if args[0] == "1":
        lcd.move_right()
    else:
        lcd.move_left()
def backlight(args):
    print("LCD backlight command")
    lcd.set_backlight(int(args[0]))

# Setup device
device = iot.IOT("10.0.0.191", 5623) # Define the ID, first argument is IP, second argument is the port
device.start() # Start the connection to the IOT server
device.setID("lcd_device") # Set the ID of the IOT device

# Define functions with the device
device.defineCommand("display", display)
device.defineCommand("clear", clear)
device.defineCommand("move", move)
device.defineCommand("backlight", backlight)

# Keep looping the take command so it doesnt quit
try: # Make sure to cleanly exit
    while True:
        device.takeCommand() # Wait until a command has been sucessfully ran
except KeyboardInterrupt:
    print("Clean exit!")

lcd.clear() # Clean LCD
lcd.set_backlight(1)
device.stop() # Stop the command to the IOT server
