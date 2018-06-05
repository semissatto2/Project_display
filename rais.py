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

	pygame.mouse.set_visible(0)
	# Tenta carregar a imagem do diretorio compartilhado. Caso nao consiga, carrega do diretorio interno
	try:
		directory_shared = "/home/debian/Desktop/shared/" + file_name
		image = pygame.image.load(directory_shared).convert()
		#print_echo(directory_shared)
	except:
		directory_interno = "/home/debian/Desktop/Project_display/images/" + file_name
		image = pygame.image.load(directory_interno).convert()
		#print_echo(directory_interno)
	screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
	image = pygame.transform.scale(image, (screen.get_size()[0], screen.get_size()[1]))

	sprite = pygame.sprite.Sprite()
	sprite.image = image
	sprite.rect = image.get_rect()

	if offline:
		font = pygame.font.SysFont('Sans', 50)
		text = font.render('OFFLINE MODE', True, (255, 0, 0))
		sprite.image.blit(text, sprite.rect)

	group = pygame.sprite.Group()
	group.add(sprite)
	group.draw(screen)

	pygame.display.flip()
	#back = pygame.Surface(screen.get_size())
	#back = back.convert()
	#back.blit(image,(0,0))
	#screen.blit(back,(0,0))
	#pygame.display.flip()

#A partir de uma interrupcao, le IO e carrega imagem na tela
def new_msg():
        print_echo("new CLP command")
        x = 8*GPIO.input("P8_18")+4*GPIO.input("P8_16")+2*GPIO.input("P8_14")+GPIO.input("P8_12")
        image_file=str(x)+".png"
	pygame.display.init()
	display_image(image_file)
        print_echo("end of command")

def clp_dead():
	print_echo("CLP dead")
	pygame.display.init()
	image_file="plc_failure.jpg"
	display_image(image_file)

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

pygame.init()

browser = 0
if len (sys.argv) != 1:
	if sys.argv[1] == 'browser':
		browser = 1

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
	image_file = "ready.jpg"
	if browser:
		if sys.argv[-1] =='chromium':
			os.system('su debian -c "/usr/bin/chromium --kiosk --disable-infobars --start-fullscreen --hide-scrollbars https://status.lnls.br &"')
		else:
			os.system('/home/debian/Desktop/Project_display/launcher_browser.sh')
else:
	image_file = "ready_offline.png"

display_image(image_file)
print_echo("Listening CLP")

try:
	#__PERMANENT_LOOP
	while True:
		if (os.system("ping -c 2 -W 1 " + hostname + " >> /dev/null")==0) == offline:
			offline = not offline;
			if offline == 0:
				image_file = "ready.jpg"
			else:
				image_file = "ready_offline.png"
			display_image(image_file)
		if browser and (not offline):
			pygame.display.quit()
			time.sleep(10)
			pygame.display.init()
			display_image(image_file)
		time.sleep(2)
		#Se apertar ESC ou 'Xzinho da janela', fecha a tela

except KeyboardInterrupt:
	os.system("pkill chromium")
	os.system("pkill midori")
	print_echo("Ending Script")
