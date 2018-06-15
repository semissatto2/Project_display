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

#DEFAULT CONFIG VARIABLES
hostname = "www.google.com.br" 		#host to ping in order to check connectivity
client_name = "BBB_default_"+str(random.randint(0,100))
browser = 0
broker_address = "10.2.105.126"
background_color = (0,0,0)
font_color = (255,255,255)
delay_browser = 10
delay_msg = 4
delay_ping = 2
ip_address = "none"
delay_saver = 5
persist_saver = 5
beamline = "MANACA"

#Print with ECHO - to log when running as service
def print_echo(msg):
	subprocess.Popen("echo " + str(msg),shell=True).communicate()

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    return tuple(int(hex_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb_tuple):
	return '%02x%02x%02x' %rgb_tuple

#READING CONFIG FILE

local_file = '/home/debian/Desktop/config'
if os.path.isfile(local_file):
	config_file = open(local_file,'r')
else:
	config_file = open('/home/debian/Desktop/Project_display/config_default','r')
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
	elif line[0] == "folder_username":
		folder_username = line[-1].strip()
	elif line[0] == "folder_password":
		folder_password = line[-1].strip()
	elif line[0] == "beamline":
		beamline = line[-1].strip()
	elif line[0] == "delay_saver_min":
		delay_saver = int(line[-1].strip())
	elif line[0] == "persist_saver_sec":
		persist_saver = int(line[-1].strip())
config_file.close()

client_name = beamline + "/" + client_name

#create function for message callback
def on_message(client, userdata, message):
	global font_color,background_color,browser,browser_launched
	print_echo("message received = " +str(message.payload.split("\n")) + "\ttopic = " + str(message.topic) + "\tqos = " + str(message.qos))
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
				subprocess.Popen('/home/debian/Desktop/Project_display/launcher_browser.sh',shell=True).communicate()
				#subprocess.Popen('su debian -c "/usr/bin/chromium --kiosk --disable-infobars --start-fullscreen --hide-scrollbars https://status.lnls.br &"',shell=True).communicate()
				browser_launched = 1
			browser = 1
		else:
			if browser_launched:
				subprocess.Popen("pkill midori",shell=True).communicate()
				subprocess.Popen("pkill chromium",shell=True).communicate()
				browser_launched = 0
			browser = 0
	elif str(message.topic) == "RAIS/"+client_name+"/img" or str(message.topic) == "RAIS/global/img":
		display_image(str(message.payload))
	elif str(message.topic) == "RAIS/global/img-update":
		display_text("Loading Images...",(0,0,0),(0,0,255))
		subprocess.Popen(["sudo","/home/debian/Desktop/Project_display/update_images.sh",str(folder_username),str(folder_password)]).communicate()
		display_text("New images have been loaded",(0,0,0),(0,255,0))
	elif str(message.topic) == "RAIS/global/firmware-update":
		display_text("Updating firmware...",(0,0,0),(255,0,0))
		subprocess.Popen(["sudo","/home/debian/Desktop/Project_display/update_fw.sh"]).communicate()
	elif str(message.topic) == "RAIS/"+client_name+"/online" and str(message.payload)=="false":
		client.publish("RAIS/"+client_name+"/online",ip_address,qos=2,retain=True)
		client.will_set("RAIS/"+client_name+"/online", payload="false", qos=2, retain=True)

#create function for connect callback
def on_connect(client, userdata, flags, rc):
	global font_color,background_color,browser,flag_connected

	print_echo("Connected flags: "+str(flags)+" result code: "+str(rc))
	#display_text("MQTT Connected",(0,0,0),(0,255,0))
	flag_connected = 1

	print_echo("Subscribing to topic: "+"RAIS/"+client_name+"/msg")
	client.subscribe("RAIS/"+client_name+"/msg")
	print_echo("Subscribing to topic: "+"RAIS/"+client_name+"/img")
	client.subscribe("RAIS/"+client_name+"/img")
	print_echo("Subscribing to topic: "+"RAIS/"+client_name+"/browser")
	client.subscribe("RAIS/"+client_name+"/browser")
	print_echo("Subscribing to topic: "+"RAIS/"+client_name+"/clp-alive")
	client.subscribe("RAIS/"+client_name+"/clp-alive")
	print_echo("Subscribing to topic: "+"RAIS/"+client_name+"/clp-message")
	client.subscribe("RAIS/"+client_name+"/clp-message")
	print_echo("Subscribing to topic: "+"RAIS/"+client_name+"/config/color")
	client.subscribe("RAIS/"+client_name+"/config/color")
	print_echo("Subscribing to topic: "+"RAIS/"+client_name+"/config/bg")
	client.subscribe("RAIS/"+client_name+"/config/bg")
	print_echo("Subscribing to topic: "+"RAIS/"+client_name+"/online")
	client.subscribe("RAIS/"+client_name+"/online")


	client.publish("RAIS/"+client_name+"/config/color",rgb_to_hex(font_color))
	client.publish("RAIS/"+client_name+"/config/bg",rgb_to_hex(background_color))
	client.publish("RAIS/"+client_name+"/browser","yes" if browser == 1 else "no")

	print_echo("Subscribing to topic: RAIS/global/msg")
	client.subscribe("RAIS/global/msg")
	print_echo("Subscribing to topic: RAIS/global/img")
	client.subscribe("RAIS/global/img")
	print_echo("Subscribing to topic: RAIS/global/browser")
	client.subscribe("RAIS/global/browser")
	print_echo("Subscribing to topic: RAIS/global/firmware-update")
	client.subscribe("RAIS/global/firmware-update")
	print_echo("Subscribing to topic: RAIS/global/img-update")
	client.subscribe("RAIS/global/img-update")
	print_echo("Subscribing to topic: RAIS/global/config/color")
	client.subscribe("RAIS/global/config/color")
	print_echo("Subscribing to topic: RAIS/global/config/bg")
	client.subscribe("RAIS/global/config/bg")

	print_echo("Publishing message to topic: "+"RAIS/"+client_name+"/online :"+ip_address)
	client.publish("RAIS/"+client_name+"/online",ip_address,qos=2,retain=True)
	client.will_set("RAIS/"+client_name+"/online", payload="false", qos=2, retain=True)

#create function for log callback
def on_log(client, userdata, level, buf):
	#print("log: "+str(buf)+"\n")
	return

#create function for publish callback
def on_publish(client,userdata,mid):
	#print("data published: "+str(mid)+"\n")
	return

#create function for subscribe callback
def on_subscribe(client, userdata, mid, granted_qos):
	#print("subscribed: "+str(mid)+"\n")
	return

#create function for unsubscribe callback
def	on_unsubscribe(client, userdata, mid):
	#print("unsubscribed: "+str(mid)+"\n")
	return

#create function for disconnect callback
def	on_disconnect(client, userdata, rc):
	print_echo("Publishing message to topic: "+"RAIS/"+client_name+"/online : false")
	client.publish("RAIS/"+client_name+"/online","false",qos=2,retain=True)

	print_echo("MQTT disconnected: "+str(rc)+"\n")
	#display_text("MQTT Disconnected",(0,0,0),(255,0,0))
	global flag_connected
	flag_connected = 0

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

#load image from file and display
def display_image(file_name):
	if pygame.display.get_init() == False:
		pygame.display.init()
	pygame.mouse.set_visible(0)
	# Tenta carregar a imagem do diretorio compartilhado. Caso nao consiga, carrega do diretorio interno
	directory_shared = "/home/debian/Desktop/shared/" + file_name
	directory_interno = "/home/debian/Desktop/Project_display/images/" + file_name
	if os.path.isfile(directory_shared):
		image = pygame.image.load(directory_shared)
		#print_echo(directory_shared)
	elif os.path.isfile(directory_interno):
		image = pygame.image.load(directory_interno)
		#print_echo(directory_interno)
	else:
		display_text("ERROR: File Not Found",(0,0,0),(255,0,0)) #Erro caso imagem nao seja encontrada
		return
	screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
	image = pygame.transform.scale(image,screen.get_size())
	screen.blit(image,(0,0))

	if offline == True:
		font = pygame.font.SysFont('Sans',80)
		text = font.render('OFFLINE MODE', True, (255, 0, 0))
		screen.blit(text,(0,0))

	pygame.display.flip()

#A partir de uma interrupcao, le IO e carrega imagem na tela
def new_msg():
	x = 8*GPIO.input("P8_18")+4*GPIO.input("P8_16")+2*GPIO.input("P8_14")+GPIO.input("P8_12")
	image_file=str(x)+".png"
	display_image(image_file)
	print_echo("Event P8_11 - new PLC command: " + image_file)
	if flag_connected:
		client.publish("RAIS/"+client_name+"/clp-message",image_file)

def clp_keep_alive():
	status = GPIO.input("P8_17")
	msg = "PLC keep-alive bit: " + str(status)
	print_echo("Event P8_17 - "+msg)
	if flag_connected:
		if status:
			client.publish("RAIS/"+client_name+"/clp-alive","true")
			display_text(msg,(0,0,0),(0,255,0))
		else:
			client.publish("RAIS/"+client_name+"/clp-alive","false")
			display_text(msg,(0,0,0),(255,0,0))

#__SETUP_GPIO
GPIO.setup("P8_11", GPIO.IN)
GPIO.setup("P8_12", GPIO.IN) #BIT 0
GPIO.setup("P8_14", GPIO.IN) #BIT 1
GPIO.setup("P8_16", GPIO.IN) #BIT 2
GPIO.setup("P8_18", GPIO.IN) #BIT 3
GPIO.setup("P8_17", GPIO.IN) #CLP KEEP-ALIVE
GPIO.add_event_detect("P8_11", GPIO.RISING, bouncetime=200)
GPIO.add_event_detect("P8_17",GPIO.BOTH, bouncetime=200)

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

print_echo("Connecting to MQTT broker: "+str(broker_address))
try:
	client.connect(broker_address) #connect to broker
except:
	print_echo("Connection refused")

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

output, error = subprocess.Popen("ifconfig eth0",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
output = output.split(" ")
if "inet" in output:
	ip_address = output[output.index("inet")+1]
image_file = "ready.jpg"
print_echo("IP address: " + ip_address)

if offline == False:
	subprocess.Popen(["sudo","/home/debian/Desktop/Project_display/update_images.sh",str(folder_username),str(folder_password)]).communicate()
	if browser:
		subprocess.Popen('/home/debian/Desktop/Project_display/launcher_browser.sh',shell=True).communicate()
		#subprocess.Popen('su debian -c "/usr/bin/chromium --kiosk --disable-infobars --start-fullscreen --hide-scrollbars https://status.lnls.br &"',shell=True).communicate()
		browser_launched = 1
display_image(image_file)

print_echo("Listening CLP - Keep-alive bit: " + str(GPIO.input("P8_17")))

if flag_connected:
	if GPIO.input("P8_17"):
		client.publish("RAIS/"+client_name+"/clp-alive","true")
	else:
		client.publish("RAIS/"+client_name+"/clp-alive","false")

delay_test = 5
backup = pygame.display.get_surface().copy()
screen_saver = 0
try:
	#__PERMANENT_LOOP
	t_browser = time.time()
	t_ping = time.time()
	t_test = time.time()
	t_msg = time.time()
	t_screen_saver = time.time()
	while True:
		client.loop(timeout=0.2)
		#print_echo("GPIO P8_17: "+str(GPIO.input("P8_17")))
		if GPIO.event_detected("P8_17"):
			clp_keep_alive()
			t_browser = time.time()
			t_msg = t_browser
			t_screen_saver = t_browser
		if GPIO.event_detected("P8_11"):
			new_msg()
			t_browser = time.time()
			t_msg = t_browser
			t_screen_saver = t_browser
		if time.time() - t_ping >= delay_ping:
			t_ping = time.time()

			output, error = subprocess.Popen("ping -c 2 -W 0.2 "+hostname,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()

			if ("0% packet loss" in output)==offline:
				offline = not offline
				if offline == True:
					flag_connected = 0
				print_echo("Connection Status Changed: Offline = "+str(offline))

			if flag_connected == 0:
				#print_echo("Connecting to MQTT broker: "+str(broker_address))
				try:
					client.reconnect()
				except:
					#print_echo("Connection refused")
					pass

		if time.time() - t_browser >= delay_browser+delay_msg:
			t_browser = time.time()
			t_msg = t_browser
			if browser_launched and browser and (not offline):
				t_screen_saver = t_browser
				if pygame.display.get_init() == True:
					backup = pygame.display.get_surface().copy()
					pygame.display.quit()
		if time.time() - t_msg >= delay_browser:
			t_msg = time.time()
			if pygame.display.get_init() == False:
				pygame.display.init()
				pygame.mouse.set_visible(0)
				screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
				screen.blit(backup,(0,0))
				pygame.display.flip()
		if time.time() - t_test >= delay_test:
			t_test = time.time()
		if screen_saver == 0 and time.time() - t_screen_saver >= delay_saver*60:
			if pygame.display.get_init() == True:
				backup = pygame.display.get_surface().copy()
			display_text(beamline,(255,255,255),(0,0,0))
			screen_saver = 1
		if screen_saver == 1 and time.time() - t_screen_saver >= (delay_saver*60+persist_saver):
			if pygame.display.get_init() == False:
				pygame.display.init()
			pygame.mouse.set_visible(0)
			screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
			screen.blit(backup,(0,0))
			pygame.display.flip()
			t_screen_saver = time.time()
			screen_saver=0
			#display_text("Teste linha 1\nLinha 2",(0,0,0),(0,255,0))

except KeyboardInterrupt:
	if flag_connected:
		client.disconnect()
	subprocess.Popen("pkill chromium",shell=True).communicate()
	subprocess.Popen("pkill midori",shell=True).communicate()
	GPIO.cleanup()
	print_echo("Ending Script")
