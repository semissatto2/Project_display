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
	pygame.mouse.set_visible(0)
	screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
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

#os.system("export DISPLAY=:0.0")
#os.system("export XAUTHORITY=~/.Xauthority")

'''
found = False
for driver in drivers:
	# Make sure that SDL_VIDEODRIVER is set
	if not os.getenv('SDL_VIDEODRIVER'):
		os.putenv('SDL_VIDEODRIVER', driver)
	try:
		pygame.display.init()
	except pygame.error:
		print 'Driver: {0} failed.'.format(driver)
		continue
	found = True
	break
'''
pygame.init()
time.sleep(1)
print("test")

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
	os.system('su debian -c "/usr/bin/chromium --kiosk --disable-infobars --start-fullscreen --hide-scrollbars https://status.lnls.br &"')
else:
	display_image("ready_offline.png")

print_echo("Listening CLP")

try:
	time.sleep(20)
	#__PERMANENT_LOOP

	while True:
		if (os.system("ping -c 2 -W 1 " + hostname)==0) == offline:
			offline = not offline;
		pygame.display.quit()
		time.sleep(10)
		pygame.display.init()
		screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		if offline == 0:
			display_image("ready.png")
		else:
			display_image("ready_offline.png")	
		time.sleep(2)
		#Se apertar ESC ou 'Xzinho da janela', fecha a tela
		
except KeyboardInterrupt:
	os.system("pkill chromium")
	print_echo("Ending Script")
