# MQTT
import paho.mqtt.client as mqtt
# Supporting libraries
import os, time, numpy as np
from interface import *
from autofocus import *
# Thread
from multiprocessing import Process

# Initialize mqtt client
client = mqtt.Client()

# Subscribe topics
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Microscope hardware
    client.subscribe("/connect")
    client.subscribe("/zu")
    client.subscribe("/zd")
    client.subscribe('/led')
    client.subscribe('/steps')
    client.subscribe('/home')
    client.subscribe('/movefield')
    # Autofocus
    client.subscribe('/autofocus')
    client.subscribe('/variance')

# Reply messages
def on_message(client, userdata, msg):
    global enable, stepsz, time_
    global start_autofocus, count_autofocus

    if msg.topic == "/connect":
        if int(msg.payload) == 1:
            enable = True
            print('server enabled')

    if enable == True:
        if msg.topic == '/movefield':
            if int(msg.payload)==1:
                change(1)
            if int(msg.payload)==0:
                change(0)

        elif msg.topic == "/home":
            home()

        elif msg.topic == "/steps":
            stepsz = float(msg.payload)*50
            print(msg.topic, stepsz)

        elif msg.topic == "/led":
            if int(msg.payload) == 0 :
                brigthness(0)
            elif int(msg.payload) == 1:
                brigthness(1)
            print(msg.topic, msg.payload)

        elif msg.topic == "/autofocus":
            if msg.payload == "start":
	        # Start sequence
		start_autofocus = True
		publish_message("/autofocus", "get")
	    print(msg.topic, msg.payload)

        elif msg.topic == "/variance":
	    if start_autofocus == True:
	        # Save position and focus coefficient
	        list_autofocus.append((0, msg.payload))
		# Move the microscope and get another value 
		z(stepsz, 1, 500)
                pulish_message("/autofocus", "get")
		# Count the amount of positions plus values 
		count_autofocus += 1
		# Ten positions are enough
		if count_autofocus == 10:
		    start_autofocus = False
		    count_autofocus = 0
                    print(list_autofocus)
                    # Focus the microscope
		    aut = autofocus(list_autofocus)
		    aut.focus()
        
	elif msg.topic == "/zu":
            z(stepsz, 1, 500)
	    
        elif msg.topic == "/zd":
            z(stepsz, 0, 500)
            
    else:
        print('server not enabled')

def publish_message(topic, message):
    client.publish(topic, str(message), 2)

if __name__ == '__main__':
    # Global variables
    global stepsz, time_, enable 
    global start_autofocus, count_autofocus
    stepsz = 250
    time_ = 500
    enable = False
    start_autofocus = False
    count_autofocus = 0
    list_autofocus = []
    
    #client.connect('test.mosquitto.org', 1883, 60)
    client.connect('test.mosquitto.org', 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
