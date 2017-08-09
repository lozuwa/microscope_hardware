# MQTT
import paho.mqtt.client as mqtt
# Supporting libraries
import os, time, numpy as np
import datetime
from interface import *
from autofocus import *
# Thread
from multiprocessing import Process

# Initialize mqtt client
client = mqtt.Client()

# Support functions
def z_up():
    global stepsz
    while(1):
        print('zup ', os.getpid())
        z(stepsz, 1, time_)
        time.sleep(0.01)

def z_down():
    global stepsz
    while(1):
        print('zdown ', os.getpid())
        z(stepsz, 0, time_)
        time.sleep(0.01)

def timestamp():
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
    global start_autofocus, count_autofocus
    global proc_z_up, proc_z_down

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
                change(1)
            if int(msg.payload)==0:
                change(0)

        elif msg.topic == "/home":
            home()

        elif msg.topic == "/steps":
            stepsz = float(msg.payload)
            if stepsz <= 30:
                stepsz = 30
            print(msg.topic, stepsz)

        elif msg.topic == "/led":
            if int(msg.payload) == 0 :
                brigthness(0)
            elif int(msg.payload) == 1:
                brigthness(1)
            print(msg.topic, msg.payload)

        elif msg.topic == "/autofocus":
            print(msg.topic, msg.payload)
            if msg.payload.decode('utf-8') == "start":
                # Start sequence
                start_autofocus = True
                publish_message("/autofocus", "get")

        elif msg.topic == "/variance":
            print(msg.topic, msg.payload)
            if start_autofocus == True:
                # Save position and focus coefficient
                list_autofocus.append((count_autofocus, float(msg.payload)))
                # Move the microscope and get another value
                z(100,1,300)
                time.sleep(0.01)
                publish_message("/autofocus", "get")
                # Count the amount of positions plus values
                count_autofocus += 1
                # Ten positions are enough
                if count_autofocus == 10:
                    start_autofocus = False
                    count_autofocus = 0
                    print(list_autofocus)
                    # Focus the microscope
                    #aut = autofocus(list_autofocus)
                    #aut.focus()

        elif msg.topic == "/zu":
            if int(msg.payload) == 1:
                print(msg.topic, int(msg.payload))
                proc_z_up.start()
            elif int(msg.payload) == 2:
                try:
                    print(msg.topic, int(msg.payload))
                    proc_z_up.terminate()
                    proc_z_up = Process(target=z_up)
                except:
                    print('There was a problem with zu process')

        elif msg.topic == "/zd":
            if int(msg.payload) == 1:
                print(msg.topic, int(msg.payload))
                proc_z_down.start()
            elif int(msg.payload) == 2:
                try:
                    print(msg.topic, int(msg.payload))
                    proc_z_down.terminate()
                    proc_z_down = Process(target=z_down)
                except:
                    print('There was a problem with zd process')
    else:
        print('server not enabled')

def publish_message(topic, message):
    client.publish(topic, str(message), 2)

if __name__ == '__main__':
    # Global variables
    global stepsz, time_, enable
    global start_autofocus, count_autofocus
    global proc_z_up, proc_z_down
    stepsz = 250
    time_ = 500
    enable = False
    start_autofocus = False
    count_autofocus = 0
    list_autofocus = []
    proc_z_up = Process(target=z_up)
    proc_z_down = Process(target=z_down)

    #client.connect('test.mosquitto.org', 1883, 60)
    client.connect('192.168.3.174', 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()

