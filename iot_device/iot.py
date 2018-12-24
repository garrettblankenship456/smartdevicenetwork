# This file will be imported to allow for easy creating custom IOT devices

# Requirements
import socket
from time import sleep
import sys

# Different default commands
def echoFunc(args):
    message = " ".join(args)
    print(message)

def stop(args):
    sys.exit(0)

# Classes
class IOT:
    # Constructor
    def __init__(self, hostname, port):
        self.hostname = hostname # Set hostname
        self.port = port # Set port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
        self.idSet = False # If the ID has ever been set
        self.currentVersion = "0" # Check for version

        # Dictionary to hold all the commands avaialble to the device
        self.commands = {
            "echo": echoFunc,
            "stop_device": stop
        }

    # Connecting functions
    def start(self):
        print("Connecting to IOT server")

        # Check if it connected or not
        try:
            self.sock.connect((self.hostname, self.port))
            self.sock.recv(4096)
            print("Connected to server")
            return True
        except ConnectionRefusedError:
            print("Could not connect to server... Retrying in 10 seconds");
            sleep(10)
            self.start()

    # Disconnecting functions
    def stop(self):
        print("Disconnecting from IOT server")
        self.sock.close()

    # Send/receive functions
    def give(self, data):
        # Convert to bytes
        data = data.encode("utf8")
        # Send data, if the server is down try reconnecting
        try:
            self.sock.send(data)
        except BrokenPipeError:
            print("Server not available")
            if self.start() == True:
                self.give(data.decode("utf8"))

    def take(self):
        # Receive data and return it
        # Convert bytes to data
        try:
            data = self.sock.recv(4096)
        except OSError:
            print("Server not available")
            if self.start() == True:
                data = self.take()


        data = data.decode("utf8")

        return data

    # Update function
    def update(self):
        pass

    # IOT specific functions (Make specific server calls easier)
    def setID(self, id):
        # Check if the ID has already been set
        if self.idSet == False:
            self.give(id) # Send ID
            self.take() # Wait for handshake
            return True
        else:
            return False

    def checkUpdate(self):
        # Send server check update request
        self.give("check_update")
        update = self.take()

        # Check if update is new
        if update > self.currentVersion:
            self.update()
            self.currentVersion = update
            return True
        else:
            return False

    def takeCommand(self):
        # Loop until successful command
        success = False
        while success == False:
            # Get command data
            cmd = self.take()
            cmd = cmd.split(" ")
            args = cmd[1:]
            cmd = cmd[0]

            # Check if you have the command
            for c in self.commands:
                if c == cmd:
                    self.commands[c](args)
                    success = True

    def defineCommand(self, commandName, commandFunction):
        print("Defined new command: " + commandName)
        self.commands[commandName] = commandFunction

    def undefineCommand(self, commandName):
        print("Removed command: ", commandName)
        del self.commands[commandName]
