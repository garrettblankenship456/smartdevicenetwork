#!/usr/bin/python3
# Runs the speech commands

# Imports
import os
import sys
import speech_recognition as sr
sys.path.insert(0, "../..")
import iot # pylint: disable=import-error

# Initialize IOT
device = iot.IOT("controller", "192.168.1.97", 5623)
device.start()

def shutdown():
	pass
	#os.system("sudo init 0")

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
			text = str(r.recognize_google(audio)).lower()
			print("Heard:", repr(text))

			# Check as command
			if "turn on lights" in text:
				print("Sending data")
				device.give("route rfcontrol send_code on")
				reply = device.take()

				if reply == "end":
					device.stop()
					break
			elif "turn off lights" in text:
				print("Sending off command")
				device.give("route rfcontrol send_code off")
				reply = device.take()

				if reply == "end":
					device.stop()
					break
			else:
				print("Doesnt match any")

		except sr.UnknownValueError:
			print("Couldnt be understood")
		except sr.RequestError as e:
			print(e)

except KeyboardInterrupt:
	print("Cleanning up...")
	device.stop()
