# IOT RF controller
import sys
import time
from rpi_rf import RFDevice
sys.path.insert(0, "..")
import iot

# Initialize RF devices
rfRecv = RFDevice(27)
rfTrans = RFDevice(17)
rfRecv.enable_rx()
rfTrans.enable_tx()

# Receiving variables
recvTime = None
lastCodeReceived = None

# Define command functions
def transmitDecimal(args):
    # Transmits the code with given parameters
    print("Transmitting code!")
    rfTrans.tx_code(int(args[0]), int(args[1]), int(args[2]))

def receiveDecimal(args):
    # Receive the code with given parameters
    while True:
        # Check if code changed
        if rfRecv.rx_code_timestamp != recvTime:
            lastCodeReceived = rfRecv.rx_code
            print("Received code:", lastCodeReceived)

            # End loop
            break

        time.sleep(0.01) # Stall program until received a transmission

def sendLastCode(args):
    # Skip if no last code
    if lastCodeReceived == None: return

    # Send the TX of the last code
    transmitDecimal([lastCodeReceived, 1, 180])

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
rfIOT.defineCommand("receive", receiveDecimal)
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