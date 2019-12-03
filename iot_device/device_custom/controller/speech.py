#!/usr/bin/python3
# Runs the speech commands

# Imports
import os
import speech_recognition as sr
import iot

# Initialize IOT
device = iot.IOT("controller", "192.168.1.97", 5623)
device.start()

def shutdown():
	os.system("sudo init 0")

device.defineCommand("shutdown", shutdown)

# Initialize the speech recognizer
r = sr.Recognizer()
mic = sr.Microphone()

# Listen
try:
	while True:
		with mic as source:
			print("Listening!")
			r.adjust_for_ambient_noise(source)
			audio = r.listen(source)

		# Process data
		try:
			text = r.recognize_google(audio)
			print("Heard:", text)

			# Check as command
			if True:
				print("Sending data")
				device.give(text)
				reply = device.take()

				if reply == "end":
					device.stop()
					break
		except sr.UnknownValueError:
			print("Couldnt be understood")
		except sr.RequestError as e:
			print(e)

except KeyboardInterrupt:
	print("Cleanning up...")
	device.stop()
