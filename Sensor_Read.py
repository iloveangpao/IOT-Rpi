#####################################################
# Author: Donal D'silva
# Desc  : Class to abstract sensor readings
#####################################################

import RPi.GPIO as GPIO
import Freenove_DHT as DHT
import time


class SensorDD():
	def __init__(self):
		humidity = 0
		temperature = 0
		distance = 0
		# Setup for Ultrasonic detector
		
		
	# Gets DHT module Temperature & Humidity Reading	
	# Code adapted from 
	# https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/blob/master/Code/Python_Code/21.1.1_DHT11/DHT11.py	
	def get_temp_humidity(self, DHTPin):
		dht = DHT.DHT(DHTPin)   						# Create a DHT object passing in pin number
		check = dht.readDHT11()
		
		if (check is dht.DHTLIB_OK):
			print("DHT11, OK!")
		elif (check is dht.DHTLIB_ERROR_CHECKSUM):
			print("DHTLIB_ERROR_CHECKSUM!!")
		elif (check is dht.DHTLIB_ERROR_TIMEOUT):
			print("DHTLIB_ERROR_TIMEOUT!")
		else:
			print("Unaccounted error!")
		
		[temp, humidity] = dht.temperature, dht.humidity
		
		return [temp, humidity]
			
	# Gets Ultrasonic readings	
	# Code  adapted from 
	# https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/tree/master/Code/Python_Code/24.1.1_UltrasonicRanging
	def get_ultrasonic_range(self, trigPin, echoPin, MaxDist, timeOut):
		# Setup
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(trigPin, GPIO.OUT)						
		GPIO.setup(echoPin, GPIO.IN)						
		
		GPIO.setup(11, GPIO.IN)
		
		# Get measurement of ultrasonic module in cm
		GPIO.output(trigPin, GPIO.HIGH)      			#make trigPin send 10us high level
		time.sleep(0.00001)   						    #10us
		GPIO.output(trigPin,GPIO.LOW)
		pingTime = self.pulseIn(echoPin,GPIO.HIGH,timeOut)   #read plus time of echoPin
		distance = pingTime * 340.0 / 2.0 / 10000.0     # the sound speed is 340m/s, and calculate distance
		return distance

	
	# Ultrasonic detector helper functions
	# Get pluse timing
	def pulseIn(self, pin,level,timeOut):					# function pulseIn: obtain pulse time of a pin
		t0 = time.time()
		while(GPIO.input(pin) != level):
			if((time.time() - t0) > timeOut*0.000001):
				return 0;
		
		t0 = time.time()
		while(GPIO.input(pin) == level):
			if((time.time() - t0) > timeOut*0.000001):
				return 0;
		
		pulseTime = (time.time() - t0)*1000000
		return pulseTime
