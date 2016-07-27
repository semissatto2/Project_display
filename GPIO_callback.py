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
	time.sleep(0.05)
	global a
	a = a + 1
	if a == 11:
		a = 1
	elif a % 2 == 0:
		print "varrendo..."
	#Varre mensagem 0
		if GPIO.input("P8_12")==0:
			if GPIO.input("P8_14")==0:
				if GPIO.input("P8_16")==0:
					if GPIO.input("P8_18")==0:
						funcao_5()
	#Varre mensagem 1
		if  GPIO.input("P8_12")==1:
                	if GPIO.input("P8_14") == 0:
                        	if GPIO.input("P8_16") == 0:
                                	if GPIO.input("P8_18") == 0:
                                        	funcao_1()
						                                        	
	#Varre mensagem 2
        	if  GPIO.input("P8_14")==1:
                	if GPIO.input("P8_12") == 0:
                        	if GPIO.input("P8_16") == 0:
                                	if GPIO.input("P8_18") == 0:
                                        	funcao_2()
	                                        
	#Varre mensagem 3
	        if  GPIO.input("P8_12")==1:
	                if GPIO.input("P8_14")==1:
	                        if GPIO.input("P8_16") == 0:
	                                if GPIO.input("P8_18") == 0:
	                                        funcao_3()
	                                        
	#Varre mensagem 4
		if  GPIO.input("P8_16")==1:
                	if GPIO.input("P8_14")== 0:
                        	if GPIO.input("P8_12") == 0:
                                	if GPIO.input("P8_18") == 0:
                                        	funcao_4()
	                                          

def funcao_1():
	print "funcao_1"
	screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
	pygame.mouse.set_visible(0)
	image1 = pygame.image.load("/home/debian/Desktop/Project_display/beamon.jpg")
	image1 = pygame.transform.scale(image1, (screen.get_size()[0], screen.get_size()[1]))
	back1 = pygame.Surface(screen.get_size())
	back1 = back1.convert()
	back1.blit(image1,(0,0))
	screen.blit(back1,(0,0))
	while GPIO.input("P8_11"):
		pygame.display.flip()
	pygame.quit()
        
def funcao_2():
	print "funcao_2"
    	screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
	pygame.mouse.set_visible(0)
	image2 = pygame.image.load("/home/debian/Desktop/Project_display/beamoff.jpg")
	image2 = pygame.transform.scale(image2, (screen.get_size()[0], screen.get_size()[1]))
	back2 = pygame.Surface(screen.get_size())
	back2 = back2.convert()
	back2.blit(image2,(0,0))
	screen.blit(back2,(0,0))
	while GPIO.input("P8_11"):
		pygame.display.flip()
	pygame.quit()
        
def funcao_3():
	print "funcao_3"
	screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
	pygame.mouse.set_visible(0)
	image3 = pygame.image.load("/home/debian/Desktop/Project_display/imminent.jpg")
	image3 = pygame.transform.scale(image3, (screen.get_size()[0], screen.get_size()[1]))
	back3 = pygame.Surface(screen.get_size())
	back3 = back3.convert()
	back3.blit(image3,(0,0))
	screen.blit(back3,(0,0))
	while GPIO.input("P8_11"):
		pygame.display.flip()
	pygame.quit()
        
def funcao_4():
       	print "funcao_4"
	screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
	pygame.mouse.set_visible(0)
	image4 = pygame.image.load("/home/debian/Desktop/Project_display/falha.jpg")
	image4 = pygame.transform.scale(image4, (screen.get_size()[0], screen.get_size()[1]))
	back4 = pygame.Surface(screen.get_size())
	back4 = back4.convert()
	back4.blit(image4,(0,0))
	screen.blit(back4,(0,0))
	while GPIO.input("P8_11"):
		pygame.display.flip()
	pygame.quit()
	
def funcao_5():
       	print "funcao_5"
        screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        pygame.mouse.set_visible(0)
        image5 = pygame.image.load("/home/debian/Desktop/Project_display/off.jpg")
        image5 = pygame.transform.scale(image5, (screen.get_size()[0], screen.get_size()[1]))
        back5 = pygame.Surface(screen.get_size())
        back5 = back5.convert()
        back5.blit(image5,(0,0))
        screen.blit(back5,(0,0))
        while GPIO.input("P8_11"):
                pygame.display.flip()
        pygame.quit()
	
#__SETUP
#Configura os GPIOs da Beaglebone
#Ate o momento (25/Julho/2016 ) apenas os GPIOs 11, 12, 14, 16 estao sendo utilizados. Para este caso, tem-se 1 bit de controle e 3 bits de identificacao de mensagens

GPIO.setup("P8_11", GPIO.IN)							#bit de controle de borda
GPIO.add_event_detect("P8_11", GPIO.BOTH, callback=funcao_0, bouncetime=100)
GPIO.setup("P8_12", GPIO.IN)							#bit 0 de identificacao de mensagem
GPIO.setup("P8_13", GPIO.IN)
GPIO.setup("P8_14", GPIO.IN)							#bit 1 de identificacao de mensagem
GPIO.setup("P8_15", GPIO.IN)
GPIO.setup("P8_16", GPIO.IN)							#bit 2 de identificacao de mensagem
GPIO.setup("P8_17", GPIO.IN)
GPIO.setup("P8_18", GPIO.IN)

print "Setup"
pygame.init()

#__PERMANENT_LOOP

while True:

	time.sleep(1)
	
