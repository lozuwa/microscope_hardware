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
import time
import datetime
# Tensor manipulation
import numpy as np
# Thread
from multiprocessing import Process
from multiprocessing import Pool
# Supporting libraries
from interface import *
from autofocus import *
from utils import *

# Initialize mqtt client
client = mqtt.Client(clean_session = True)

# Subscribe topics
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/automatic")
    client.subscribe("/variance")
    client.subscribe("/autofocus")
    
# Reply messages
def on_message(client, userdata, msg):
    global counter
    print(msg.topic, msg.payload)
    if msg.topic == "/automatic":
        if msg.payload.decode("utf-8") == "start":
            print("Starting autofocus sequence ...")
            time.sleep(1)
            publishMessage("/autofocus", "get")
            counter = 0
        else:
            pass
    elif msg.topic == "/variance":
        if counter <= 10:
            print("Received message: ", msg.payload)
            time.sleep(1)
            print("Publishing get autofocus")
            publishMessage("/autofocus", "get")
            counter += 1
        else:
            print("Finished ", counter)
    else:
        pass
    
def publishMessage(topic,
                    message,
                    qos = 2,
                    retain = False):
    """
    Publishes a mqtt message
    :param topic: input string that defines the target topic
    :param message: input string that denotes the content of the message
    :param qos: input int that defines the type of qos for the mqtt communication
    :param retain: input boolean that defines if the message is set to retained
    """
    # Assert variables
    assert type(topic) == str, VARIABLE_IS_NOT_STR
    assert type(message) == str, VARIABLE_IS_NOT_STR
    assert type(qos) == int, VARIABLE_IS_NOT_INT
    # Publish message
    client.publish(topic, message, qos = qos, retain = retain)

if __name__ == "__main__":
    global counter
    global stateStop
    counter = 0
    stateStop = False
    #client.connect("test.mosquitto.org", 1883, 60)
    client.connect("192.168.0.102", 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
