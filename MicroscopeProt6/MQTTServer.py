# MQTT
import paho.mqtt.client as mqtt
# Supporting libraries
import os, time, numpy as np
from Interface import *
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
    global enable
    global time_
    global stepsz

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
            print(msg.topic, msg.payload)
            start_autofocus = True

        elif msg.topic == "/variance":
            print(msg.topic, msg.payload)

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
    global start_autofocus
    stepsz = 250
    time_ = 500
    enable = False
    start_autofocus = False
    
    #client.connect('test.mosquitto.org', 1883, 60)
    client.connect('test.mosquitto.org', 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
