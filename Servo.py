##################################################################################
# Author: Donal D'silva
# Desc  : Servo Controller Class
#
# Code adapted from:
# https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/
# tree/master/Code/Python_Code/15.1.1_Sweep
##################################################################################

import RPi.GPIO as GPIO
import time

class ServoDD():
	def __init__(self):
		print(self, "no intialisation")
		
	global p
	# Servo settings
	OFFSET_DUTY = 0.5        				# Pulse offset of servo
	SERVO_MIN_DUTY = 2.5 + OFFSET_DUTY  	# Pulse duty cycle for min servo angle
	SERVO_MAX_DUTY = 12.5 + OFFSET_DUTY 	# Pulse duty cycle for max servo angle
	servoPin = 12
	
	# Identify GPIO by physical location on board
	# Set Servo mode to output and starting state
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(servoPin, GPIO.OUT)
	GPIO.output(servoPin, GPIO.LOW)
		
	# Servo frequency and duty cycle
	p = GPIO.PWM(servoPin, 50)
	p.start(0)
	
	def map(self, value, fromLow, fromHigh, toLow, toHigh):
		return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow
		
	def servoWrite(self, angle):      # make the servo rotate to specific angle (0-180 degrees)
		if(angle < 0):
			angle = 0
		elif(angle > 180):
			angle = 180
		p.ChangeDutyCycle(self.map(angle, 0, 180, self.SERVO_MIN_DUTY, self.SERVO_MAX_DUTY))#map the angle to duty cycle and output it
		
	def loop(self, reading, manualOverride):
		UltraSonicRange = 0
		
		if (manualOverride == "OFF"):
			UltraSonicRange = reading * 7.2
		else:
			UltraSonicRange = reading
			
		if (reading > 0 and reading < 181):
			self.servoWrite(UltraSonicRange)

		
	def destroy():
		p.stop()
		GPIO.cleanup()
	
