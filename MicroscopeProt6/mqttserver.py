# MQTT
import paho.mqtt.client as mqtt
# Supporting libraries
import os, time, numpy as np
import datetime
from interface import *
from autofocus import *
# Thread
from multiprocessing import Process

# Constant variables 
AUTOFOCUS_TOPIC = "/autofocus"
VARIANCE_TOPIC = "/variance"
LED_TOPIC = "/led"

# Initialize mqtt client
client = mqtt.Client()

# Instantiate classes
axMov = axisMovement()

# Support functions
def zUp():
    global stepsz
    while(1):
        print('zup ', os.getpid())
        axMov.z(stepsz, 1, time_)
        time.sleep(0.01)

def zDown():
    global stepsz
    while(1):
        print('zdown ', os.getpid())
        axMov.z(stepsz, 0, time_)
        time.sleep(0.01)

def timeStamp():
    now = datetime.datetime
    return str(now.microsecond)

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
    global startAutofocus, countAutofocus, countFrames
    global procZUp, procZDown

    if msg.topic == "/connect":
        if int(msg.payload) == 1:
            enable = True
            print('server enabled')
        elif int(msg.payload) == 0:
            enable = False
            print('server disabled')

    if enable == True:
        if msg.topic == '/movefield':
            if int(msg.payload)==1:
                axMov.moveField(1)
            if int(msg.payload)==0:
                axMov.moveField(0)

        elif msg.topic == "/home":
            axMov.home()

        elif msg.topic == "/steps":
            stepsz = float(msg.payload)
            if stepsz <= 30:
                stepsz = 30
            print(msg.topic, stepsz)

        elif msg.topic == LED_TOPIC:
            if int(msg.payload) == 0 :
                axMov.led.set_state(0)
                ledState = axMov.led.get_state()
                axMov.writeLed(ledState)
            elif int(msg.payload) == 1:
                axMov.led.set_state(1)
                ledState = axMov.led.get_state()
                axMov.writeLed(ledState)
            print(msg.topic, msg.payload)

        elif msg.topic == AUTOFOCUS_TOPIC:
            print(msg.topic, msg.payload)
            if msg.payload.decode('utf-8') == "start":
                startAutofocus = True
                countAutofocus = 0
                countFrames = 0

        elif msg.topic == VARIANCE_TOPIC:
            print(msg.topic, msg.payload)
            # Start autofocus    
            if startAutofocus:
                if countAutofocus < 5:
                    if countFrames < 5:
                        listAutofocus.append((countAutofocus, float(msg.payload)))
                        countFrames += 1
                    else:
                        axMov.zResponse(100, 1, 500)
                        countFrames = 0
                        countAutofocus += 1
                else:
                    startAutofocus = False
                    publishMessage(AUTOFOCUS_TOPIC, "stop")
                    print(listAutofocus)

        elif msg.topic == "/zu":
            if int(msg.payload) == 1:
                print(msg.topic, int(msg.payload))
                procZUp.start()
            elif int(msg.payload) == 2:
                try:
                    print(msg.topic, int(msg.payload))
                    procZUp.terminate()
                    procZUp = Process(target=zUp)
                except:
                    print('There was a problem with zu process')

        elif msg.topic == "/zd":
            if int(msg.payload) == 1:
                print(msg.topic, int(msg.payload))
                procZDown.start()
            elif int(msg.payload) == 2:
                try:
                    print(msg.topic, int(msg.payload))
                    procZDown.terminate()
                    procZDown = Process(target=zDown)
                except:
                    print('There was a problem with zd process')
    else:
        print('server not enabled')

def publishMessage(topic, message):
    client.publish(topic, str(message), 2)

if __name__ == '__main__':
    # Global variables
    global stepsz, time_, enable
    global startAutofocus, countAutofocus, countFrames
    global procZUp, procZDown
    stepsz = 250
    time_ = 500
    enable = False
    startAutofocus = False
    countAutofocus = 0
    countFrames = 0
    listAutofocus = []
    procZUp = Process(target=zUp)
    procZDown = Process(target=zDown)

    #client.connect('test.mosquitto.org', 1883, 60)
    client.connect('192.168.3.174', 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()

