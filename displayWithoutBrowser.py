#!/usr/bin/env python
import Adafruit_BBIO.GPIO as GPIO
import time
import pygame
from pygame.locals import *
from sys import exit



#__GLOBAL_VARIABLES_CONTROL
a = 1

#__FUNCTIONS
def funcao_0(channel):
        time.sleep(0.03)
        global a
        a = a + 1
        if a == 1001:
                a = 1
        if a % 2 == 0:
            x = 8*GPIO.input("P8_18")+4*GPIO.input("P8_16")+2*GPIO.input("P8_14")+GPIO.input("P8_12")
            print x
            directory = "/home/debian/Desktop/Project_display/images/" + str(x) + ".png"
            print directory
            image = pygame.image.load(directory)
            image = pygame.transform.scale(image, (screen.get_size()[0], screen.get_size()[1]))
	        back = pygame.Surface(screen.get_size())
	        back = back1.convert()
	        back.blit(image,(0,0))
	        screen.blit(back,(0,0))
	        pygame.display.flip()

#__SETUP_GPIO
GPIO.setup("P8_11", GPIO.IN)
GPIO.add_event_detect("P8_11", GPIO.BOTH, callback=funcao_0, bouncetime=150)
GPIO.setup("P8_12", GPIO.IN)
GPIO.setup("P8_14", GPIO.IN)
GPIO.setup("P8_16", GPIO.IN)
GPIO.setup("P8_17", GPIO.IN)
GPIO.setup("P8_18", GPIO.IN)

#__SETUP_PYGAME
pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

#__PERMANENT_LOOP
while True:
	time.sleep(1)
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				exit()
