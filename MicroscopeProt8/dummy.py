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
client = mqtt.Client()

# Instantiate classes
PORT = sys.argv[1]
axMov = axisMovement(port = int(PORT))

# Support functions
def zUp():
    """
    """
    global stepsz
    while(1):
        #print("zup ", os.getpid())
        axMov.zResponse(stepsz, 1, time_)
        time.sleep(0.01)

def zDown():
    """

    """
    global stepsz
    while(1):
        #print("zdown ", os.getpid())
        axMov.zResponse(stepsz, 0, time_)
        time.sleep(0.01)

# Subscribe topics
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/variance")
    client.subscribe("/autofocus")
    
# Reply messages
def on_message(client, userdata, msg):
    if msg.topic == "/autofocus":
        publishMessage("/autofocus",
                        "get",
                        qos = 2)
    elif msg.topic == "/variance":
        print(msg.topic, msg.payload)
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
    #client.connect("test.mosquitto.org", 1883, 60)
    client.connect("192.168.0.102", 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
