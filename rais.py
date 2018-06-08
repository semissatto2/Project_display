#!/usr/bin/env python
import Adafruit_BBIO.GPIO as GPIO
import time
import pygame
import sys
import os
import paho.mqtt.client as mqtt
import random
import subprocess

#GLOBAL VARIABLES INITIALISATION
global font_color,background_color,browser,browser_launched,offline,flag_connected
flag_connected = 0
offline = True
browser_launched = 0
delay_browser = 10
delay_msg = 4
delay_ping = 2

#DEFAULT CONFIG VARIABLES
hostname = "www.google.com.br" 		#host to ping in order to check connectivity
client_name = "BBB_default_"+str(random.randint(0,100))
browser = 0
broker_address = "10.2.105.113"
background_color = (0,0,0)
font_color = (255,255,255)

#Print with ECHO - to log when running as service
def print_echo(msg):
	os.system("echo " + str(msg))

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    return tuple(int(hex_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb_tuple):
	return '%02x%02x%02x' %rgb_tuple

#READING CONFIG FILE
config_file = open('/home/debian/Desktop/Project_display/config','r')
for line in config_file:
	line = line.split(" ")
	if line[0] == "client_name":
		client_name = line[-1].strip()
	elif line[0] == "broker_address":
		broker_address = line[-1].strip()
	elif line[0] == "ping_host":
		hostname = line[-1].strip()
	elif line[0] == "browser":
		if "yes" in line[-1]:
			browser = 1  
	elif line[0] == "background_color":
		background_color = hex_to_rgb(line[-1].strip())
	elif line[0] == "font_color":
		font_color = hex_to_rgb(line[-1].strip())
	elif line[0] == "delay_browser":
		delay_browser = int(line[-1].strip())
	elif line[0] == "delay_message":
		delay_msg = int(line[-1].strip())
	elif line[0] == "delay_ping":
		delay_ping = int(line[-1].strip())
config_file.close()

#create function for message callback
def on_message(client, userdata, message):
	global font_color,background_color,browser,browser_launched
	print_echo("message received = " +str(message.payload) + "\ttopic = " + str(message.topic)+ "\tqos = " + str(message.qos))
	#print("message retain flag = "+str(message.retain)+"\n")
	if str(message.topic) == "RAIS/"+client_name+"/msg" or str(message.topic) == "RAIS/global/msg":
		display_text(str(message.payload),font_color,background_color)
	elif str(message.topic) == "RAIS/"+client_name+"/config/color" or str(message.topic) == "RAIS/global/config/color":
		font_color = hex_to_rgb(str(message.payload))
	elif str(message.topic) == "RAIS/"+client_name+"/config/bg" or str(message.topic) == "RAIS/global/config/bg":
		background_color = hex_to_rgb(str(message.payload))
	elif str(message.topic) == "RAIS/"+client_name+"/browser" or str(message.topic) == "RAIS/global/browser":
		if str(message.payload) == 'yes':
			if browser_launched == 0:
				os.system('/home/debian/Desktop/Project_display/launcher_browser.sh')
				browser_launched = 1	
			browser = 1
		else:
			if browser_launched:
				os.system("pkill midori")
				browser_launched = 0	
			browser = 0
			
		
	

#create function for connect callback
def on_connect(client, userdata, flags, rc):
	print("Connected flags"+str(flags)+"result code "+str(rc)+"client_id \n")
	#display_text("MQTT Connected",(0,0,0),(0,255,0))
	global font_color,background_color,browser,flag_connected
	flag_connected = 1
	
	print("Subscribing to topic: "+"RAIS/"+client_name+"/msg\n")
	client.subscribe("RAIS/"+client_name+"/msg")
	print("Subscribing to topic: "+"RAIS/"+client_name+"/img\n")
	client.subscribe("RAIS/"+client_name+"/img")
	print("Subscribing to topic: "+"RAIS/"+client_name+"/browser\n")
	client.subscribe("RAIS/"+client_name+"/browser")
	print("Subscribing to topic: "+"RAIS/"+client_name+"/clp-alive\n")
	client.subscribe("RAIS/"+client_name+"/clp-alive")
	print("Subscribing to topic: "+"RAIS/"+client_name+"/clp-message\n")
	client.subscribe("RAIS/"+client_name+"/clp-message")
	print("Subscribing to topic: "+"RAIS/"+client_name+"/config/color\n")
	client.subscribe("RAIS/"+client_name+"/config/color")
	print("Subscribing to topic: "+"RAIS/"+client_name+"/config/bg\n")
	client.subscribe("RAIS/"+client_name+"/config/bg")
	
	client.publish("RAIS/"+client_name+"/config/color",rgb_to_hex(font_color))
	client.publish("RAIS/"+client_name+"/config/bg",rgb_to_hex(background_color))
	client.publish("RAIS/"+client_name+"/browser","yes" if browser == 1 else "no")
	
	print("Subscribing to topic: RAIS/global/msg\n")
	client.subscribe("RAIS/global/msg")
	print("Subscribing to topic: RAIS/global/img\n")
	client.subscribe("RAIS/global/img")
	print("Subscribing to topic: RAIS/global/browser\n")
	client.subscribe("RAIS/global/browser")
	print("Subscribing to topic: RAIS/global/firmware-update\n")
	client.subscribe("RAIS/global/firmware-update")
	print("Subscribing to topic: RAIS/global/img-update\n")
	client.subscribe("RAIS/global/img-update")
	print("Subscribing to topic: RAIS/global/config/color\n")
	client.subscribe("RAIS/global/config/color")
	print("Subscribing to topic: RAIS/global/config/bg\n")
	client.subscribe("RAIS/global/config/bg")
	
	print_echo("Publishing message to topic: "+"RAIS/"+client_name+"/online - true")
	client.publish("RAIS/"+client_name+"/online","true")

#create function for log callback
def on_log(client, userdata, level, buf):
	print("log: "+str(buf)+"\n")

#create function for publish callback
def on_publish(client,userdata,mid):             					
	print("data published: "+str(mid)+"\n")

#create function for subscribe callback
def on_subscribe(client, userdata, mid, granted_qos):             	
	print("subscribed: "+str(mid)+"\n")

#create function for unsubscribe callback
def	on_unsubscribe(client, userdata, mid):
	print("unsubscribed: "+str(mid)+"\n")
	
#create function for disconnect callback
def	on_disconnect(client, userdata, rc):
	print_echo("MQTT disconnected: "+str(rc)+"\n")
	display_text("MQTT Disconnected",(0,0,0),(255,0,0))
	#global flag_connected
	#flag_connected = 0

#load image from file and display
def display_image(file_name):
	if pygame.display.get_init() == False:
		pygame.display.init()
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
	screen.blit(image,(0,0))

	if offline == True:
		font = pygame.font.SysFont('Sans',80)
		text = font.render('OFFLINE MODE', True, (255, 0, 0))
		screen.blit(text,(0,0))

	pygame.display.flip()
	
#load image from file and display
def display_text(text_msg,text_color,background):
	if pygame.display.get_init() == False:
		pygame.display.init()
	pygame.mouse.set_visible(0)
	screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
	screen.fill(background)
	
	text_msg = text_msg.split("\n")
	if len(text_msg) > 0:
		if len(text_msg)>2:
			text_msg = text_msg[:2]
		font_size = []
		lines = []
		for i in range(len(text_msg)):
			lines.append(str(text_msg[i]).decode("utf-8", "ignore"))
			if len(lines[i])==0:
				lines[i] = " "
			font_size.append(int(1.5*screen.get_width()/len(lines[i])))
			font = pygame.font.SysFont('Sans',font_size[i])
			w,h = font.size(lines[i])
			font_size[i] = int(0.8*font_size[i]*screen.get_width()/w)
			font = pygame.font.SysFont('Sans',font_size[i])
			w,h = font.size(lines[i])
			if h > 0.9*screen.get_height()/len(text_msg):
				font_size[i] = int(0.9*font_size[i]*screen.get_height()/h/len(text_msg))
		font = pygame.font.SysFont('Sans',min(font_size))
		msg = []
		for i in range(len(text_msg)):
			msg.append(font.render(lines[i],True,text_color))
			screen.blit(msg[i],((screen.get_width()-msg[i].get_width())/2,(screen.get_height()*(1.0/len(text_msg)+i)-msg[i].get_height())/2 ))
		
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
	display_image(image_file)
        print_echo("end of command")

def clp_dead():
	print_echo("CLP dead")
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

print_echo("Creating new MQTT instance: "+client_name+"\n")
client = mqtt.Client(client_name) #create new instance
client.on_message = on_message #attach function to callback
client.on_log = on_log
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_connect = on_connect
client.on_unsubscribe = on_unsubscribe
client.on_disconnect = on_disconnect

print_echo("Connecting to MQTT broker: "+str(broker_address)+"\n")
client.connect_async(broker_address) #connect to broker
client.loop_start() #stop the loop

print_echo("Starting Pygame\n")	
pygame.init()

for i in range(2):
	display_image("connecting.jpg")
	output, error = subprocess.Popen("ping -c 2 -W 0.2 "+hostname,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
	if "0% packet loss" in output:
		offline = False
		break
	time.sleep(4)
	display_image("waiting.jpg")
	time.sleep(1)
image_file = "ready.jpg"

if offline == False:
	if browser:
		os.system('/home/debian/Desktop/Project_display/launcher_browser.sh')
		browser_launched = 1

display_image(image_file)
print_echo("Listening CLP")

try:
	#__PERMANENT_LOOP
	while True:
		#client.loop()
		output, error = subprocess.Popen("ping -c 2 -W 0.2 "+hostname,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
		if ("0% packet loss" in output)==offline:
			offline = not offline
			print_echo("Connection Status Changed: Offline = "+str(offline))			
		if browser_launched and browser and (not offline):
			backup = pygame.display.get_surface().copy()
			pygame.display.quit()
			time.sleep(delay_browser)
			if pygame.display.get_init() == False:
				pygame.display.init()
				pygame.mouse.set_visible(0)
				screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
				screen.blit(backup,(0,0))
				pygame.display.flip()
			
		#if flag_connected:
			#print_echo("MQTT Connected")
			#print_echo("Publishing MQTT message to topic: "+"RAIS/"+client_name+"/clp-alive - YES\n")
			#client.publish("RAIS/"+client_name+"/clp-alive","YES")
		if flag_connected == 0:
			print_echo("Connecting to MQTT broker: "+str(broker_address))
			client.loop_stop()
			client.connect_async(broker_address) #connect to broker
			client.loop_start()
		time.sleep(delay_msg)
		display_text("Teste linha 1\nLinha 2",(0,0,0),(0,255,0))
		time.sleep(delay_msg)
		display_text("Oi\naaaaaaaaaaaa",(255,255,255),(0,0,255))


except KeyboardInterrupt:
	if flag_connected:
		client.loop_stop()
		client.disconnect()
	os.system("pkill chromium")
	os.system("pkill midori")
	print_echo("Ending Script")
