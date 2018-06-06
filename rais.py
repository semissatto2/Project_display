#!/usr/bin/env python
import Adafruit_BBIO.GPIO as GPIO
import time
import pygame
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
		image = pygame.image.load(directory_shared)
		#print_echo(directory_shared)
	except:
		directory_interno = "/home/debian/Desktop/Project_display/images/" + file_name
		image = pygame.image.load(directory_interno)
		#print_echo(directory_interno)

	screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
	image = pygame.transform.scale(image,screen.get_size())

        print_echo("Inside display_image 4: Offline = "+str(offline))

	screen.blit(image,(0,0))

	if offline == True:
		font = pygame.font.SysFont('Sans',80)
		text = font.render('OFFLINE MODE', True, (255, 0, 0))
		screen.blit(text,(0,0))

	pygame.display.flip()

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
offline = True
browser = 0
if len (sys.argv) != 1:
	if sys.argv[1] == 'browser':
		browser = 1

hostname = "www.google.com.br" #ping host to check connectivity
for i in range(2):
	display_image("connecting.jpg")
	if os.system("ping -c 2 " + hostname + " > /dev/null 2> /dev/null") == 0:
		offline = False
		break
	time.sleep(4)
	display_image("waiting.jpg")
	time.sleep(1)

image_file = "ready.jpg"

if offline == False:
	if browser:
		if sys.argv[-1] =='chromium':
			os.system('su debian -c "/usr/bin/chromium --kiosk --disable-infobars --start-fullscreen --hide-scrollbars https://status.lnls.br &"')
		else:
			os.system('/home/debian/Desktop/Project_display/launcher_browser.sh')
display_image(image_file)
print_echo("Listening CLP")

try:
	#__PERMANENT_LOOP
	while True:
		if (os.system("ping -c 2 " + hostname + " > /dev/null 2> /dev/null")==0) == offline:
			offline = not offline
			print_echo("Connection Status Changed: Offline = "+str(offline))
			display_image(image_file)

		if browser and (not offline):
			pygame.display.quit()
			time.sleep(10)
			pygame.display.init()
			display_image(image_file)

		time.sleep(2)

except KeyboardInterrupt:
	os.system("pkill chromium")
	os.system("pkill midori")
	print_echo("Ending Script")
