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
	        #Varre mensagem 0
                if  GPIO.input("P8_16")==0:
                        if GPIO.input("P8_14")== 0:
                                if GPIO.input("P8_12") == 0:
                                        if GPIO.input("P8_18") == 0:
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
	#Varre mensagem 5
		if  GPIO.input("P8_12")==1:
                	if GPIO.input("P8_14") == 0:
                        	if GPIO.input("P8_16") == 1:
                                	if GPIO.input("P8_18") == 0:
                                        	funcao_6()                                        
	#Varre mensagem 6
		if  GPIO.input("P8_12")==0:
                	if GPIO.input("P8_14") == 1:
                        	if GPIO.input("P8_16") == 1:
                                	if GPIO.input("P8_18") == 0:
                                        	funcao_7()                                        	
	#Varre mensagem 7
		if  GPIO.input("P8_12")==1:
                	if GPIO.input("P8_14") == 1:
                        	if GPIO.input("P8_16") == 1:
                                	if GPIO.input("P8_18") == 0:
                                        	funcao_8()		

def funcao_1():
	image1 = pygame.image.load("/home/debian/Desktop/shared/beamon.png")
	image1 = pygame.transform.scale(image1, (screen.get_size()[0], screen.get_size()[1]))
	back1 = pygame.Surface(screen.get_size())
	back1 = back1.convert()
	back1.blit(image1,(0,0))
	screen.blit(back1,(0,0))
	#while GPIO.input("P8_11"):
	pygame.display.flip()
	
	        
def funcao_2():
        image2 = pygame.image.load("/home/debian/Desktop/shared/beamoff.png")
	image2 = pygame.transform.scale(image2, (screen.get_size()[0], screen.get_size()[1]))
	back2 = pygame.Surface(screen.get_size())
	back2 = back2.convert()
	back2.blit(image2,(0,0))
	screen.blit(back2,(0,0))
	#while GPIO.input("P8_11"):
	pygame.display.flip()
        
	
        
def funcao_3():
	image3 = pygame.image.load("/home/debian/Desktop/shared/imminent.png")
	image3 = pygame.transform.scale(image3, (screen.get_size()[0], screen.get_size()[1]))
	back3 = pygame.Surface(screen.get_size())
	back3 = back3.convert()
	back3.blit(image3,(0,0))
	screen.blit(back3,(0,0))
	#while GPIO.input("P8_11"):
	pygame.display.flip()
		
        
def funcao_4():
       	image4 = pygame.image.load("/home/debian/Desktop/shared/falha.png.png")
	image4 = pygame.transform.scale(image4, (screen.get_size()[0], screen.get_size()[1]))
	back4 = pygame.Surface(screen.get_size())
	back4 = back4.convert()
	back4.blit(image4,(0,0))
	screen.blit(back4,(0,0))
	#while GPIO.input("P8_11"):
	pygame.display.flip()
		
def funcao_5():
        image5 = pygame.image.load("/home/debian/Desktop/shared/off.png")
        image5 = pygame.transform.scale(image5, (screen.get_size()[0], screen.get_size()[1]))
        back5 = pygame.Surface(screen.get_size())
        back5 = back5.convert()
        back5.blit(image5,(0,0))
        screen.blit(back5,(0,0))
	#while GPIO.input("P8_11"):
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
pygame.mouse.set_visible(0)
image0 = pygame.image.load("/home/debian/Desktop/shared/off.png")
image0 = pygame.transform.scale(image0, (screen.get_size()[0], screen.get_size()[1]))
back0 = pygame.Surface(screen.get_size())
back0 = back0.convert()
back0.blit(image0,(0,0))
screen.blit(back0,(0,0))
pygame.display.flip()


#__PERMANENT_LOOP
while True:
	time.sleep(1)
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				exit()


