#!/bin/bash

# This script will build everything with g++
# It is useful for when updating the devices to just git pull and execute the script then restart
# the services then redownloading each file and then sys calls for each file to build it

# Make the directory
mkdir ../compiled

# User utilities
g++ ../user_utils/server_test.cpp ../user_utils/sources/socket.cpp -o ../compiled/server_test
g++ ../user_utils/iot_util.cpp ../user_utils/sources/socket.cpp -o ../compiled/utility

# IOT services
g++ ../iot_device/iot_functions.cpp ../iot_device/sources/socket.cpp -o ../compiled/function_service
g++ ../iot_device/iot_update_service.cpp ../iot_device/sources/socket.cpp -o ../compiled/update_service

# Compile all specialty
../scripts/compileall.sh
