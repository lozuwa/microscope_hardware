#ip 192.168.3.174

# MQTT
import paho.mqtt.client as mqtt
# Supporting libraries
import os, time, numpy as np
from Interface_mic import *
# Thread
from multiprocessing import Process
import eventlet
eventlet.monkey_patch()

# Initialize mqtt client
client = mqtt.Client()

# Global variables
stepsz = 30
stepsxy = 100
time_ = 500
KEEP_ALIVE_TIME = 10

def z_up():
    z_s(stepsz, 1, time_)

def z_down():
    z_s(stepsz, 0, time_)

def x_left():
    x_s(stepsxy, 1, time_)

def x_right():
    x_s(stepsxy, 0, time_)

def y_forward():
    y_s(stepsxy, 1, time_)

def y_backward():
    y_s(stepsxy, 0, time_)

# Subscribe topics
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Microscope hardware
    client.subscribe("/connect")
    client.subscribe("/zu")
    client.subscribe("/zd")
    client.subscribe("/yb")
    client.subscribe("/yf")
    client.subscribe("/xl")
    client.subscribe("/xr")
    client.subscribe('/led')
    client.subscribe('/home')
    client.subscribe('/automatic')
    client.subscribe('/movefield')
    # Camera app
    client.subscribe('/microscope')

# Reply messages
def on_message(client, userdata, msg):
    global enable
    global time_

    #print(msg.topic, msg.payload)
    if msg.topic == "/connect":
        enable = True if int(msg.payload) == 1 else False
        if int(msg.payload) == 1:
            print('server enabled')

    if enable == True:
        if msg.topic == '/microscope':
            #print(msg.topic, msg.payload)
            time.sleep(1)

        elif msg.topic == '/movefield':
            if int(msg.payload)==1:
                change(1)
            if int(msg.payload)==0:
                change(0)

        elif msg.topic == "/automatic":
            if int(msg.payload) == 0:
                auto(6000)

        elif msg.topic == "/home":
            home()

        elif msg.topic == "/led":
            stepsz = int(msg.payload)
            brigthness(100)
            print(msg.topic, msg.payload)

        elif msg.topic == "/zu":
            if int(msg.payload) == 1:
                z_up()

        elif msg.topic == "/zd":
            if int(msg.payload) == 1:
                z_down()

        elif msg.topic == "/xl":
            if int(msg.payload) == 1:
                x_left()

        elif msg.topic == "/xr":
            if int(msg.payload) == 1:
                x_right()

        elif msg.topic == "/yf":
            if int(msg.payload) == 1:
                y_forward()

        elif msg.topic == "/yb":
            if int(msg.payload) == 1:
                y_backward()
    else:
        print('server not enabled')

def keep_smartphone_alive():
    client.publish('/microscope', 'keep alive', 2)
    time.sleep(KEEP_ALIVE_TIME)

# Initialize thread
#eventlet.spawn(keep_smartphone_alive)

if __name__ == '__main__':
    # Initialize enable variable
    global enable
    enable = False

    #client.connect('test.mosquitto.org', 1883, 60)
    #client.connect('10.42.0.1', 1883, 60)
    client.connect('192.168.3.174', 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()

    while True:
        keep_smartphone_alive()
