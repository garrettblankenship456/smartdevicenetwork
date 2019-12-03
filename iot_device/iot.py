# This file will be imported to allow for easy creating custom IOT devices

# Requirements
import socket
from time import sleep
import sys
import os

# Different default commands
def echoFunc(args):
    message = " ".join(args)
    print(message)

def stop(args):
    sys.exit(0)

# Classes
class IOT:
    # Constructor
    def __init__(self, id, hostname, port):
        self.hostname = hostname # Set hostname
        self.port = port # Set port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
        self.currentVersion = "0" # Check for version
        self.id = id

        # Dictionary to hold all the commands avaialble to the device
        self.commands = {
            "echo": echoFunc,
            "stop_device": stop
        }

    # Connecting functions
    def start(self):
        print("Connecting to IOT server")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Check if it connected or not
        try:
            self.sock.connect((self.hostname, self.port))
            self.sock.recv(4096)
        except ConnectionRefusedError:
            print("Could not connect to server... Retrying in 10 seconds")
            sleep(10)
            self.start()
            return False

        # Return true once connected
        print("Connected to server")
        self.sock.send(self.id.encode("utf8"))
        self.sock.recv(4096)
        return True

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
            while self.start() != True:
                print("Trying")

            self.give(data.decode("utf8"))
            print("Reconnected!")

    def take(self):
        # Receive data and return it
        # Convert bytes to data
        try:
            data = self.sock.recv(4096)

            if data == b'':
                print("Server disconnection!")
                if self.start() == True:
                    data = self.sock.recv(4096)
        except OSError:
            print("Server not available")
            while self.start() != True:
                print("Trying")

            data = self.take()
            print("Reconnected!")


        data = data.decode("utf8")

        return data

    # Update function
    def update(self):
        # Git fetch and pull
        os.system("git fetch && git pull")

    # IOT specific functions (Make specific server calls easier)
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
