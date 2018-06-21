import time
import pygame
import subprocess

output,error = subprocess.Popen(["flite","-voice","slt","Good morning"]).communicate()

output,error = subprocess.Popen(["flite","-voice","slt","Good morning","/home/debian/Desktop/audio/file.wav"]).communicate()

pygame.mixer.pre_init(frequency=16000)

pygame.mixer.init()

time.sleep(2)

print("Number of channels: "+str(pygame.mixer.get_num_channels()))

asound = pygame.mixer.Sound("/home/debian/Desktop/audio/file.wav")
asound.play()
while(pygame.mixer.get_busy()):
	print("Waiting sound")
	time.sleep(0.2)
quit()

pygame.mixer.music.load("/home/debian/Desktop/audio/instrumental.mp3")

try:
	pygame.mixer.music.play()
	print("Playing music....")
	time.sleep(5)
	pygame.mixer.music.stop()
	print("Stopping music")
except KeyboardInterrupt:
	print("Aborting")
	pygame.mixer.music.stop()
