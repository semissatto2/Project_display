
import time
import pygame

pygame.mixer.init()

print("Number of channels: "+str(pygame.mixer.get_num_channels()))

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
