import paho.mqtt.client as mqtt #import the client1
import time
import sys

config_file = open('config','r')
for line in config_file:
	line = line.split(" ")
	if line[0] == "client_name":
		client_name = line[-1].strip()
	if line[0] == "broker_address":
		broker_address = line[-1].strip()
config_file.close()

#client_name = "BBB1"
#broker_address="10.2.105.113"
#broker_address="gae-epics"
#broker_address="192.168.1.1"

flag_connected = 0

#create function for message callback
def on_message(client, userdata, message):
	print("message received " +str(message.payload.decode("utf-8")))
	print("message topic = " + str(message.topic))
	print("message qos = " + str(message.qos))
	print("message retain flag = "+str(message.retain)+"\n")

#create function for connect callback
def on_connect(client, userdata, flags, rc):
	print("Connected flags"+str(flags)+"result code "+str(rc)+"client_id \n")
	global flag_connected
	flag_connected = 1
	
	client.loop_start() #start the loop
	
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
	
	print("Publishing message to topic: "+"RAIS/"+client_name+"/online - TRUE\n")
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
	print("disconnected: "+str(rc)+"\n")

print("creating new instance: "+client_name+"\n")
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
client.loop_start() #start the loop
	
try:
	while 1:	
		msg = "YES"
		if flag_connected:
			print("Publishing message to topic: "+"RAIS/"+client_name+"/clp-alive - "+msg+"\n")
			client.publish("RAIS/"+client_name+"/clp-alive",msg)
			time.sleep(2) # wait
		else:
			print("connecting to broker\n")
			client.connect_async(broker_address) #connect to broker
			client.loop_start() #start the loop
		time.sleep(2)

except KeyboardInterrupt:
	if flag_connected:
		client.loop_stop() #stop the loop
		client.disconnect()
