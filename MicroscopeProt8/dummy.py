"""
Author: Rodrigo Loza
Company: pfm 
Description: Dummy for autofocus control
Algorithm:
1. Send start to /autofocus
2. Script starts a process that sends a /variance get to the smartphone 
   retrieving the current variance of the laplace transform of the image 
3. Once each message is received, the motor is moved
4. Stream ends when counter is reached
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
    if msg.topic == "/automatic":
        if msg.payload.decode("utf-8") == "start":
            print("Starting autofocus sequence ...")
            time.sleep(1)
            publishMessage("/variance", "get")
            counter = 0
        else:
            pass
    elif msg.topic == "/variance":
        if msg.payload.decode("utf-8").split(";")[0] == "message":
            if counter <= 20:
                print("Received message: ", msg.payload, counter)
                time.sleep(0.1)
                print("Publishing get autofocus")
                publishMessage("/variance", "get")
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
    client.connect("192.168.0.104", 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
