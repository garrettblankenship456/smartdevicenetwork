# IOT RF controller
import sys
import time
from rpi_rf import RFDevice # pylint: disable=import-error
import json
import threading
sys.path.insert(0, "..")
import iot # pylint: disable=import-error

# Initialize RF devices
rfRecv = RFDevice(27)
rfTrans = RFDevice(17)
rfRecv.enable_rx()
rfTrans.enable_tx()

# Receiving variables
recvTime = None
lastCodeReceived = None
lastPulseLength = None
lastProtocol = None

# Data functions
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

# Create receive thread
def receiveData():
    # Open globals
    global recvTime
    global lastCodeReceived
    global lastPulseLength
    global lastProtocol

    # Receive the code with given parameters
    print("Listening")
    while rfRecv.rx_enabled:
        # Check if code changed
        if rfRecv.rx_code_timestamp != recvTime:
            recvTime = rfRecv.rx_code_timestamp
            lastPulseLength = rfRecv.rx_pulselength
            lastProtocol = rfRecv.rx_proto

            lastCodeReceived = rfRecv.rx_code
            print("Received code:", lastCodeReceived)

        time.sleep(0.01) # Stall program until received a transmission

dataThread = threading.Thread(target=receiveData, args=())
dataThread.start()

# Define command functions
def transmitDecimal(args, sender):
    # Transmits the code with given parameters
    print("Transmitting code!")
    rfTrans.tx_code(int(args[0]), int(args[1]), int(args[2]))

def addCode(args, sender):
    # Define data
    name = args[0]

    # Wait until button pressed
    print("Listening to keypress")
    startTime = (time.perf_counter() * 1000000)
    
    while recvTime == None or recvTime < startTime:
        time.sleep(0.1)

    # Acknowledge the code and test it, let the sender know
    rfIOT.give("route " + sender + " testing_code " + str(lastCodeReceived) + " " + str(lastPulseLength) + " " + str(lastProtocol))
    rfIOT.take()

    # Adds a code to a database
    print("Code test")
    codes = getCodes()
    codes[name] = {
        "code": lastCodeReceived,
        "pulse": lastPulseLength,
        "proto": lastProtocol
    }

    # Wait 5 seconds, then send the code
    time.sleep(5)
    transmitDecimal([lastCodeReceived, lastProtocol, lastPulseLength], sender)

    # Wait for response
    res = rfIOT.take()
    if res != sender + " accepted":
        print("Code not correct, end execution before saving")
        return

    # Write the codes to file if successful
    print("Code written")
    writeCodes(codes)

def sendCode(args, sender):
    # Get code list
    codes = getCodes()

    codeData = codes[args[0]] # Get data from name

    # Only continue if data exists
    if codeData == None: return

    # Send pulse
    print("Transmitting code:", codeData)
    transmitDecimal([codeData["code"], codeData["proto"], codeData["pulse"]], sender)

def sendLastCode(args, sender):
    # Skip if no last code
    if lastCodeReceived == None:
        print("No valid code.")
        return

    # Send the TX of the last code
    print("Transmitting code:", lastCodeReceived)
    transmitDecimal([lastCodeReceived, lastProtocol, lastPulseLength], sender)

# Initialize IOT
rfIOT = iot.IOT("rfcontrol", "iotserver", 5623) # Define the ID, first argument is IP, second argument is the port
rfIOT.start() # Start the connection to the IOT server

print("\n====================== UPDATE ======================")
print("Current version: " + rfIOT.currentVersion)
rfIOT.checkUpdate() # Update the currentVersion to the one the server jas
print("Server version: " + rfIOT.currentVersion)
print("====================================================\n")

# Define commands
rfIOT.defineCommand("transmit", transmitDecimal)
rfIOT.defineCommand("add_code", addCode)
rfIOT.defineCommand("send_code", sendCode)
rfIOT.defineCommand("send_last", sendLastCode)

# Accept commands
try:
    while True:
        rfIOT.takeCommand()
except KeyboardInterrupt:
    print("Clean exit!")

# Cleanup IOT
rfIOT.stop() # Stop the command to the IOT server

# Cleanup RF
rfRecv.cleanup()
rfTrans.cleanup()
dataThread.join()
