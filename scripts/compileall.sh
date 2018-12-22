#!/bin/bash

# This script compiles all the specialty functions like the default len on/off

# Make directory
mkdir ../compiled

# Led controller
g++ ../iot_device/device_custom/led_functions.cpp ../iot_device/sources/socket.cpp -o ../compiled/led_service
