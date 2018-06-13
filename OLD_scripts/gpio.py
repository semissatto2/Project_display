#!/usr/bin/env python
import Adafruit_BBIO.GPIO as GPIO
import time
import sys
import os

def event_17():
	print("Event P8_17")
	
def event_11():
	print("Event P8_11")

#__SETUP_GPIO
GPIO.setup("P8_11", GPIO.IN)
GPIO.setup("P8_12", GPIO.IN) #BIT 0
GPIO.setup("P8_14", GPIO.IN) #BIT 1
GPIO.setup("P8_16", GPIO.IN) #BIT 2
GPIO.setup("P8_18", GPIO.IN) #BIT 3
GPIO.setup("P8_17", GPIO.IN) #CLP KEEP-ALIVE
GPIO.add_event_detect("P8_11", GPIO.RISING, bouncetime=200)
GPIO.add_event_detect("P8_17",GPIO.BOTH, bouncetime=200)

while True:
	print("GPIO P8_17: "+str(GPIO.input("P8_17"))+"\tGPIO P8_11: "+str(GPIO.input("P8_11")))
	if GPIO.event_detected("P8_17"):
		print("Event P8_17 detected")
		event_17()
	if GPIO.event_detected("P8_11"):
		event_11()
		print("Event P8_11 detected")
	time.sleep(1)