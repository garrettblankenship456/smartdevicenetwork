# IOT RF controller
import sys
sys.path.insert(0, "..")
import iot

rfIOT = iot.IOT("rfcontrol", "iotserver", 5623) # Define the ID, first argument is IP, second argument is the port
rfIOT.start() # Start the connection to the IOT server


print("\n====================== UPDATE ======================")
print("Current version: " + rfIOT.currentVersion)
rfIOT.checkUpdate() # Update the currentVersion to the one the server jas
print("Server version: " + rfIOT.currentVersion)
print("====================================================\n")

rfIOT.takeCommand() # Wait until a command has been sucessfully ran

rfIOT.stop() # Stop the command to the IOT server
