#!/usr/bin/env python
import Adafruit_BBIO.GPIO as GPIO
import time
import pygame
#from pygame.locals import *
import sys
import os

def print_echo(msg):
	os.system("echo " + str(msg))

#__FUNCTIONS
def display_image(file_name):
        
	# Tenta carregar a imagem do diretorio compartilhado. Caso nao consiga, carrega do diretorio interno
        try:
            directory_shared = "/home/debian/Desktop/shared/" + file_name
            image = pygame.image.load(directory_shared)
            print_echo(directory_shared)
        except:
            directory_interno = "/home/debian/Desktop/Project_display/images/" + file_name
            image = pygame.image.load(directory_interno)
            print_echo(directory_interno)
        image = pygame.transform.scale(image, (screen.get_size()[0], screen.get_size()[1]))
        back = pygame.Surface(screen.get_size())
        back = back.convert()
        back.blit(image,(0,0))
        screen.blit(back,(0,0))
        pygame.display.flip()

#A partir de uma interrupcao, le IO e carrega imagem na tela
def new_msg():
        print_echo("new CLP command")
        x = 8*GPIO.input("P8_18")+4*GPIO.input("P8_16")+2*GPIO.input("P8_14")+GPIO.input("P8_12")
        display_image(str(x)+".png")
        print_echo("end of command")

def clp_dead():
    print_echo("CLP dead")

#__SETUP_GPIO
GPIO.setup("P8_11", GPIO.IN)
GPIO.add_event_detect("P8_11", GPIO.RISING, callback=new_msg, bouncetime=100)
GPIO.setup("P8_12", GPIO.IN) #BIT 0
GPIO.setup("P8_14", GPIO.IN) #BIT 1
GPIO.setup("P8_16", GPIO.IN) #BIT 2
GPIO.setup("P8_18", GPIO.IN) #BIT 3
GPIO.setup("P8_17", GPIO.IN) #CLP KEEP-ALIVE
GPIO.add_event_detect("P8_17",GPIO.FALLING, callback=clp_dead, bouncetime=100)

print_echo("Starting RAIS")

#__SETUP_PYGAME
pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)   
pygame.mouse.set_visible(0)

offline = 1
hostname = "www.google.com" #ping host to check connectivity
for i in range(2):
	display_image("connecting.png")
	if os.system("ping -c 2 -W 1 " + hostname) == 0:
		offline = 0
		break
	time.sleep(4)
	display_image("waiting.jpg")
	time.sleep(1)

if offline == 0:
	display_image("ready.png")
else:
	display_image("ready_offline.png")

print_echo("Listening CLP")

#__PERMANENT_LOOP
while True:
	if (os.system("ping -c 2 -W 1 " + hostname)==0) == offline:
		offline = not offline;
		if offline == 0:
			display_image("ready.png")
		else:
			display_image("ready_offline.png")
	time.sleep(10)

	#Se apertar ESC ou 'Xzinho da janela', fecha a tela
    	'''
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				sys.exit()
    	'''
