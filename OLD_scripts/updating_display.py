#!/usr/bin/env python

import time
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.mouse.set_visible(0)
image = pygame.image.load("/home/debian/Desktop/Project_display/images/updating.jpg")
image = pygame.transform.scale(image, (screen.get_size()[0], screen.get_size()[1]))
back = pygame.Surface(screen.get_size())
back = back.convert()
back.blit(image,(0,0))
screen.blit(back,(0,0))
while True:
                pygame.display.flip()
        	time.sleep(0.5)
