import RPi.GPIO as GPIO
import Freenove_DHT as DHT
import Sensor_Read as SenseD

import struct
import paho.mqtt.client as mqtt
import time



########################################################
## Sensor & other configuration area
########################################################
# DHT Temperature & Humidity Sensor config
DHTPin = 11 # Maps to GPIO 17

# Ultrasonic sensor settings
trigPin = 16
echoPin = 18
MAX_DISTANCE = 220 				# Max range to detect
timeOut = MAX_DISTANCE * 60 	# Max * 60 seconds

#################################################################
# Create instance of Sensor_Read class to access helper methods
#################################################################
SensorReads = SenseD.SensorDD() 


while True:
	temp, humidity = SensorReads.get_temp_humidity(DHTPin)
	distance = SensorReads.get_ultrasonic_range(trigPin, echoPin, MAX_DISTANCE, timeOut)
	try:
		print(distance)
		client=mqtt.Client()
		client.username_pw_set("pidee","") # remove credentials before committing code
		client.connect("m24.cloudmqtt.com",15247,60)
		client.publish("pi", temp, qos=0) #pi is topic
		time.sleep(1)
	except KeyboardInterrupt:
		print("end")
		client.disconnect()
