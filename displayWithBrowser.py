#!/usr/bin/env python
import Adafruit_BBIO.GPIO as GPIO
import time
import pygame
from pygame.locals import *
from sys import exit
import os

def print_echo(msg):
	os.system("echo " + str(msg))

#__FUNCTIONS
def new_msg():
	print_echo("new CLP command")
	time.sleep(0.05)

	screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)	
	pygame.mouse.set_visible(0)
	x = 8*GPIO.input("P8_18")+4*GPIO.input("P8_16")+2*GPIO.input("P8_14")+GPIO.input("P8_12")
	directory_shared = "/home/debian/Desktop/shared/" + str(x) + ".png"
	directory_interno = "/home/debian/Desktop/Project_display/images/" + str(x) + ".png"

	# Tenta carregar a imagem do diretorio compartilhado. Caso nao consiga, carrega do diretorio interno
	try:
		print_echo(directory_shared)
		image = pygame.image.load(directory_shared)
	except:
		print_echo(directory_interno)
		image = pygame.image.load(directory_interno)

	image = pygame.transform.scale(image, (screen.get_size()[0], screen.get_size()[1]))
	back = pygame.Surface(screen.get_size())
	back = back.convert()
	back.blit(image,(0,0))
	screen.blit(back,(0,0))
	while GPIO.input("P8_11"):
		pygame.display.flip()
	#time.sleep(0.5)
	print_echo("end of command")
	pygame.quit()

#__SETUP
GPIO.setup("P8_11", GPIO.IN)
GPIO.add_event_detect("P8_11", GPIO.RISING, callback=new_msg, bouncetime=100)
GPIO.setup("P8_12", GPIO.IN)
GPIO.setup("P8_14", GPIO.IN)
GPIO.setup("P8_16", GPIO.IN)
GPIO.setup("P8_17", GPIO.IN)
GPIO.setup("P8_18", GPIO.IN)
pygame.init()

os.system("echo 'Listening CLP'")

#__PERMANENT_LOOP
while True:

	time.sleep(1)
	#for event in pygame.event.get():
        #        if event.type == QUIT:
        #                exit()
        #        elif event.type == KEYDOWN:
        #                if event.key == K_ESCAPE:
        #                       exit()
