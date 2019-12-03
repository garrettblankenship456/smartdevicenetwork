#!/bin/bash

# This script will build everything with g++
# It is useful for when updating the devices to just git pull and execute the script then restart
# the services then redownloading each file and then sys calls for each file to build it

# Make the directory
mkdir ../compiled

# User utilities
g++ ../user_utils/sources/socket_utility.cpp ../user_utils/sources/socket.cpp -o ../compiled/socket_utility