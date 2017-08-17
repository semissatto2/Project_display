#!/usr/bin/env python
#Este codigo exibe o valor dos 8 GPIOs utilizados
import Adafruit_BBIO.GPIO as GPIO
import time

GPIO.setup("P8_11", GPIO.IN)
GPIO.setup("P8_12", GPIO.IN)
GPIO.setup("P8_13", GPIO.IN)
GPIO.setup("P8_14", GPIO.IN)
GPIO.setup("P8_15", GPIO.IN)
GPIO.setup("P8_16", GPIO.IN)
GPIO.setup("P8_17", GPIO.IN)
GPIO.setup("P8_18", GPIO.IN)


while True:
	if GPIO.input("P8_11"):
		print("P8_11 HIGH")
	else:
		print("P8_11 LOW ")
	
	if GPIO.input("P8_12"):
		print("P8_12 HIGH")
	else:
		print("P8_12 LOW ")
	if GPIO.input("P8_13"):
		print("P8_13 HIGH")
	else:
		print("P8_13 LOW ")	

	if GPIO.input("P8_14"):
		print("P8_14 HIGH")
	else:
		print("P8_14 LOW ")
	if GPIO.input("P8_15"):
		print("P8_15 HIGH")
	else:
		print("P8_15 LOW ")
	if GPIO.input("P8_16"):
		print("P8_16 HIGH")
	else:
		print("P8_16 LOW ")
	if GPIO.input("P8_17"):
		print("P8_17 HIGH")
	else:
		print("P8_17 LOW ")
	if GPIO.input("P8_18"):
		print("P8_18 HIGH")
	else:
		print("P8_18 LOW ")
		print(type(GPIO.input("P8_18")))
	print "-------------------------"
	time.sleep(1)
