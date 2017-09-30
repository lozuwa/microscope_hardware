"""
Author: Rodrigo Loza
Company: pfm 
Description: Main program for microscope's hardware
Documentation:
* /zu -> controls the z axis to move up
* /zd -> controls the z axis to move down
* /led -> turns on the led
* /steps -> controls the number of steps for XY axis
* /home -> resets the motors of the microscope
* /movefieldx -> controls the x axis
* /movefieldy -> controls the y axis
"""
# MQTT
import paho.mqtt.client as mqtt
# General purpose
import os
import sys
import math
import time
import datetime
# Tensor manipulation
import numpy as np
# Supporting libraries
from interface import *
from autofocus import *
from utils import *
from ops import *

# Initialize mqtt client
client = mqtt.Client()

# Subscribe topics
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Microscope hardware
    client.subscribe("/zu")
    client.subscribe("/zd")
    client.subscribe("/led")
    client.subscribe("/steps")
    client.subscribe("/home")
    client.subscribe("/movefieldx")
    client.subscribe("/movefieldy")
    # Autofocus
    client.subscribe("/autofocus")
    client.subscribe("/variance")
    # Microscope
    client.subscribe("/microscope")
    # Automatic
    client.subscribe("/automatic")

# Reply messages
def on_message(client, userdata, msg):
    global counter
    global scanning
    global code
    #print(msg.topic, msg.payload)
    if msg.topic == MOVEFIELDX_TOPIC:
        moveFieldX(msg.payload)
    elif msg.topic == MOVEFIELDY_TOPIC:
        moveFieldY(msg.payload)
    elif msg.topic == HOME_TOPIC:
        home()
    elif msg.topic == STEPS_TOPIC:
        STEPSZ = float(msg.payload)*3
    elif msg.topic == LED_TOPIC:
        led(msg.payload)
    ##################################################################################
    elif msg.topic == AUTOFOCUS_TOPIC:
        if msg.payload.decode("utf-8") == "start":
            print("Starting autofocus sequence ...")
            # 1. Restart z motor to bottom button
            print("Restart Z motor to bottom")
            homeZBottom()
            time.sleep(1)
            # 2. Start scanning
            print("Publishing get variance")
            publishMessage("/variance", "get")
            counter = 0
            scanning = []
        else:
            pass
    ##################################################################################
    elif msg.topic == VARIANCE_TOPIC:
        if msg.payload.decode("utf-8").split(";")[0] == "message":
            # 3. Scanning (20 fields)
            #if counter <= 20:
            if str(code) != "t":
                # Receive and save values
                print("Received message: ", msg.payload, counter)
                scanning.append(float(msg.payload.decode("utf-8").split(";")[1]))
                #time.sleep(0.1)
                # Move motor up
                code = moveZUp()
                # Get another value
                print("Publishing get autofocus ", code)
                publishMessage("/variance", "get")
                counter += 1
            # 4. Search for max value after scanning
            else:
                # Receive and save values
                print("Finished scanning: ", msg.payload, counter)
                localVal = float(msg.payload.decode("utf-8").split(";")[1])
                print("value ", np.abs(localVal - max(scanning)))
                time.sleep(0.1)
                # Compare localVal to max index
                if np.abs(localVal - max(scanning)) < 100:
                    print("Found focus point")
                else:
                    moveZDown()
                    print("Publishing get autofocus ", code)
                    publishMessage("/variance", "get")
        else:
            pass
    ##################################################################################
    elif msg.topic == "/automatic":
        # Led
        led("1")
        time.sleep(1)
        # Home
        homeXY()
        # Put slide in
        for i in range(30):
            moveFieldX(0)
        for i in range(5):
            moveFieldY(0)
        # Direction x
        directionY = True
        # Start at home
        for i in range(1600):
            i+=1
            publishMessage(topic = "/microscope",\
                            message = "pic;sample",\
                            qos = 2)
            time.sleep(1)
            # Move X
            if directionY:
                moveFieldY(0)
                print("Move Y {}".format(i))
            else:
                moveFieldY(1)
                print("Move Y {}".format(i))
            # Move Y
            if (i % 40 == 0):
                print("Move X {}".format(i))
                for j in range(3):
                    moveFieldX(0)
                # Invert X direction
                directionY = not directionY
                # Take picture
                publishMessage(topic = "/microscope",\
                            message = "pic;sample",\
                            qos = 2)
                time.sleep(1)
            elif (i % 75 == 0):
                #publishMessage("/autofocus", "start")
                print("Autofocus sample")
            else:
                pass

    ##################################################################################
    elif msg.topic == ZUP_TOPIC:
        moveFieldZUp(msg.payload)
    elif msg.topic == ZDOWN_TOPIC:
        moveFieldZDown(msg.payload)
    else:
        pass

def publishMessage(topic,
                    message,
                    qos = 2):
    """
    Publishes a mqtt message
    :param topic: input string that defines the target topic
    :param message: input string that denotes the content of the message
    :param qos: input int that defines the type of qos for the mqtt communication
    """
    # Assert variables
    assert type(topic) == str, VARIABLE_IS_NOT_STR
    assert type(message) == str, VARIABLE_IS_NOT_STR
    assert type(qos) == int, VARIABLE_IS_NOT_INT
    # Publish message
    client.publish(topic, message, qos)

if __name__ == "__main__":
    # Variables
    global counter
    global scanning
    global code
    counter = 0
    scanning = []
    code = "-1"
    # Connect to mqtt client
    client.connect(IP, PORT, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
