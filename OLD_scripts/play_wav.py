import time
import pygame
import subprocess

output,error = subprocess.Popen(["flite","-voice","slt","Good morning"]).communicate()

output,error = subprocess.Popen(["flite","-voice","slt","Good morning","file.wav"]).communicate()

pygame.mixer.pre_init(frequency=16000)

pygame.mixer.init()

time.sleep(2)

print("Number of channels: "+str(pygame.mixer.get_num_channels()))

asound = pygame.mixer.Sound("file.wav")
asound.play()
while(pygame.mixer.get_busy()):
	print("Waiting sound")
	time.sleep(0.2)
