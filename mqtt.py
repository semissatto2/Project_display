import paho.mqtt.client as mqtt #import the client1
import time
import sys

flag_connected = 0

############
def on_message(client, userdata, message):
	print("message received " +str(message.payload.decode("utf-8")))
	print("message topic = " + str(message.topic))
	print("message qos = " + str(message.qos))
	print("message retain flag = "+str(message.retain)+"\n")
########################################

def on_connect(client, userdata, flags, rc):
	print("Connected flags"+str(flags)+"result code "+str(rc)+"client_id \n")
	global flag_connected
	flag_connected = 1
	
	client.loop_start() #start the loop
	
	print("Subscribing to topic: "+client_name+"/msg\n")
	client.subscribe(client_name+"/msg")
	print("Subscribing to topic: "+client_name+"/img\n")
	client.subscribe(client_name+"/img")
	print("Subscribing to topic: "+client_name+"/browser\n")
	client.subscribe(client_name+"/browser")
	print("Subscribing to topic: "+client_name+"/clp-alive\n")
	client.subscribe(client_name+"/clp-alive")
	print("Subscribing to topic: "+client_name+"/clp-message\n")
	client.subscribe(client_name+"/clp-message")
	
	print("Subscribing to topic: global/msg\n")
	client.subscribe("global/msg")
	print("Subscribing to topic: global/img\n")
	client.subscribe("global/img")
	print("Subscribing to topic: global/browser\n")
	client.subscribe("global/browser")
	print("Subscribing to topic: global/firmware-update\n")
	client.subscribe("global/firmware")
	print("Subscribing to topic: global/img-update\n")
	client.subscribe("global/img_update")

def on_log(client, userdata, level, buf):
	print("log: "+str(buf)+"\n")

def on_publish(client,userdata,mid):             					#create function for callback
	print("data published: "+str(mid)+"\n")
	
def on_subscribe(client, userdata, mid, granted_qos):             	#create function for callback
	print("subscribed: "+str(mid)+"\n")
	
def	on_unsubscribe(client, userdata, mid):
	print("unsubscribed: "+str(mid)+"\n")
	
def	on_disconnect(client, userdata, rc):
	print("disconnected: "+str(rc)+"\n")

client_name = "BBB1"
broker_address="10.2.105.113"
#broker_address="gae-epics"
#broker_address="192.168.1.1"


print("creating new instance\n")
client = mqtt.Client(client_name) #create new instance
client.on_message = on_message #attach function to callback
client.on_log = on_log
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_connect = on_connect
client.on_unsubscribe = on_unsubscribe
client.on_disconnect = on_disconnect


print("connecting to broker\n")
client.connect_async(broker_address) #connect to broker
	
try:
	while 1:	
		msg = "YES"
		if flag_connected:
			print("Publishing message to topic: "+client_name+"/clp-alive - "+msg+"\n")
			client.publish(client_name+"/clp-alive",msg)
			time.sleep(2) # wait
		else:
			print("connecting to broker\n")
			client.connect_async(broker_address) #connect to broker
			#client.loop_start() #start the loop]
		time.sleep(2)

except KeyboardInterrupt:
	client.loop_stop() #stop the loop
	client.disconnect()
