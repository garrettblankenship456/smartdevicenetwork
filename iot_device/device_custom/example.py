#EXAMPLE USAGE FOR IOT CLASS:
import sys
sys.path.insert(0, "..")
import iot

test = iot.IOT("10.0.0.191", 5623) # Define the ID, first argument is IP, second argument is the port
test.start() # Start the connection to the IOT server

# Setup ID after handshake
test.setID("iot_script_test") # Set the ID of the IOT device

print("\n====================== UPDATE ======================")
print("Current version: " + test.currentVersion)
test.checkUpdate() # Update the currentVersion to the one the server jas
print("Server version: " + test.currentVersion)
print("====================================================\n")

#test.defineCommand("echo2", echoFunc) # Setup command to be used
test.takeCommand() # Wait until a command has been sucessfully ran

test.stop() # Stop the command to the IOT server
