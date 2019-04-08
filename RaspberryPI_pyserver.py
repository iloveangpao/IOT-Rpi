import pyrebase
import firebase_admin
from firebase_admin import credentials

import RPi.GPIO as GPIO
import Sensor_Read as SenseD
import Servo as ServoD

import struct
import paho.mqtt.client as mqtt
import time


########################################################
## Pyrebase config 
## Code has been adapated from previous assignment
########################################################
config = {
  "apiKey": "",
  "authDomain": "iotproject-6f8af.firebaseapp.com",
  "databaseURL": "https://iotproject-6f8af.firebaseio.com",
  "projectId": "iotproject-6f8af",
  "storageBucket": "iotproject-6f8af.appspot.com",
  "messagingSenderId": "218911790933",
  "serviceAccount": "/home/pi/GPIO/Project/iotproject-6f8af-cce568f9a281.json"
}

firebase = pyrebase.initialize_app(config)

cred = credentials.Certificate('/home/pi/GPIO/Project/iotproject-6f8af-cce568f9a281.json')

# Get reference to auth service and sign user in
auth = firebase.auth()

# User authorisation and refresh
user = auth.sign_in_with_email_and_password("", "") ### REMOVE CREDENTIAL INFORMATION BEFORE COMMITING CODE
# before the 1 hour expiry:
user = auth.refresh(user['refreshToken'])
# now we have a fresh token
user['idToken']


# Get database service reference
db = firebase.database()
#db.child("ManualOverride").set("ON")
#db.child("ServoAngle").set("90")
#db.child("sensor_data").child("all_readings")

########################################################
## Sensor & other configuration area
########################################################
# DHT Temperature & Humidity Sensor config
DHTPin = 11 # Maps to GPIO 17

# Ultrasonic sensor settings
trigPin = 16
echoPin = 18
MAX_DISTANCE = 220		 				# Max range to detect
timeOut = MAX_DISTANCE * 60				# Max * 60 seconds



#################################################################
# Create instances of:
# Sensor_Read & Servo classes to access helper methods
#################################################################
SensorReads = SenseD.SensorDD() 
Servo = ServoD.ServoDD()


while True:
	temp, humidity = SensorReads.get_temp_humidity(DHTPin)
	distance = round(SensorReads.get_ultrasonic_range(trigPin, echoPin, MAX_DISTANCE, timeOut), 2)
	dataLoad = struct.pack('hhl', temp, humidity, distance)
	
	# Manual Override for Servo
	manualOverride = db.child("ManualOverride").get().val()
	servoAngle = db.child("ServoAngle").get().val()
		
	dataDict = {
	'temperature': str(temp),
	'humidity': str(humidity),
	'distance': str(distance)
	}
	print(dataDict)


	if (manualOverride == "ON"):
		Servo.loop(servoAngle, manualOverride)		
	elif (manualOverride == "OFF"):
		# Call to check and adjust servo based on reading
		Servo.loop(distance, manualOverride)
		print("Ultrasensor " + str(distance))


	
	# Push to firebase db
	db.child("sensor_data").set(dataDict)
	
	try:
		client=mqtt.Client()
		client.username_pw_set("","") # remove credentials before committing code
		client.connect("m24.cloudmqtt.com",15247,60)
		client.publish("pi", dataLoad, qos=0) #pi is topic
		time.sleep(1)
	except KeyboardInterrupt:
		print("end")
		servo.destroy()
		client.disconnect()
