# MQTT
import paho.mqtt.client as mqtt
# Supporting libraries
import os, time, numpy as np
import datetime
from interface import *
from autofocus import *
# Thread
from multiprocessing import Process
from multiprocessing import Pool

# Constant variables
AUTOFOCUS_TOPIC = "/autofocus"
VARIANCE_TOPIC = "/variance"
LED_TOPIC = "/led"
MOVEFIELDX_TOPIC = "/movefieldx"
MOVEFIELDY_TOPIC = "/movefieldy"
STEPS_TOPIC = "/steps"
HOME_TOPIC = "/home"
ZDOWN_TOPIC = "/zd"
ZUP_TOPIC = "/zu"

# Initialize mqtt client
client = mqtt.Client()

# Instantiate classes
axMov = axisMovement(port = int(sys.argv[1]))

# Support functions
def zUp():
    global stepsz
    while(1):
        #print("zup ", os.getpid())
        axMov.zResponse(stepsz, 1, time_)
        time.sleep(0.01)

def zDown():
    global stepsz
    while(1):
        #print("zdown ", os.getpid())
        axMov.zResponse(stepsz, 0, time_)
        time.sleep(0.01)

def moveZ():
    hardwareCode = "i"
    # Move motor
    while(True):
        hardwareCode = axMov.zResponse(250,1,250)
        if hardwareCode == "u":
            Process(target = publishMessage, args = (AUTOFOCUS_TOPIC, "stop")).start()
            break
        time.sleep(0.01)
    return "done"

def keepAlive():
    pass
    time.sleep(10)

def timestamp():
    now = datetime.datetime
    return str(now.minute) + str(now.second) + str(now.microsecond)

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

# Reply messages
def on_message(client, userdata, msg):
    global stepsz, time_
    global procZUp, procZDown
    global autofocusState, hardwareCode, countFrames
    global countPositions, saveAutofocusCoef
    print(msg.topic, msg.payload)
    # Movement field
    if msg.topic == MOVEFIELDX_TOPIC:
        if int(msg.payload) == 1:
            axMov.moveFieldX(1)
        elif int(msg.payload) == 0:
            axMov.moveFieldX(0)
        else:
            pass
    elif msg.topic == MOVEFIELDY_TOPIC:
        if int(msg.payload) == 1:
            axMov.moveFieldY(1)
        elif int(msg.payload) == 0:
            axMov.moveFieldY(0)
        else:
            pass
    elif msg.topic == HOME_TOPIC:
        axMov.home()
    elif msg.topic == STEPS_TOPIC:
        stepsz = float(msg.payload)*3
        if stepsz <= 30:
            stepsz = 30
        else:
            pass
        print(msg.topic, stepsz)
    elif msg.topic == LED_TOPIC:
        if int(msg.payload) == 0:
            axMov.led.set_state(0)
            ledState = axMov.led.get_state()
            axMov.writeLed(ledState)
        elif int(msg.payload) == 1:
            axMov.led.set_state(1)
            ledState = axMov.led.get_state()
            axMov.writeLed(ledState)
        else:
            pass
        print(msg.topic, msg.payload)
    ##################################################################################
    elif msg.topic == AUTOFOCUS_TOPIC:
        print(msg.topic, msg.payload)
        if msg.payload.decode("utf-8") == "start":
            print("****************************Autofocus sequence****************************")
            axMov.homeZ()
            time.sleep(0.01)
            autofocusState = True
            countFrames = 0
            publishMessage(AUTOFOCUS_TOPIC, "get")
        elif msg.payload.decode("utf-8") == "stop":
            print("***", saveAutofocusCoef)
            aut = autofocus(saveAutofocusCoef)
            goBack = aut.focus()
            print("Go back ", goBack)
            time.sleep(1)
            for i in range(goBack):
                time.sleep(0.2)
                axMov.zResponse(350, 0, 250)
            countPositions = 0
            saveAutofocusCoef = []
            print("****************************End autofocus sequence****************************")
        else:
            pass
    ##################################################################################
    elif msg.topic == VARIANCE_TOPIC:
        if autofocusState:
            if hardwareCode != "u":
                if countFrames < 1:
                    print(msg.payload)
                    saveAutofocusCoef.append((countPositions, float(msg.payload)))
                    countFrames += 1
                else:
                    hardwareCode = axMov.zResponse(250, 1, 250)
                    publishMessage(AUTOFOCUS_TOPIC, "get")
                    print("Hardware (mqtt) code: {}".format(hardwareCode))
                    countPositions += 1
                    countFrames = 0
            else:
                autofocusState = False
                hardwareCode = "o"
                publishMessage(AUTOFOCUS_TOPIC, "stop")
    ##################################################################################
    elif msg.topic == ZUP_TOPIC:
        if int(msg.payload) == 1:
            print(msg.topic, int(msg.payload))
            procZUp.start()
        elif int(msg.payload) == 2:
            try:
                print(msg.topic, int(msg.payload))
                procZUp.terminate()
                procZUp = Process(target=zUp)
            except:
                print("There was a problem with zu process")
    elif msg.topic == ZDOWN_TOPIC:
        if int(msg.payload) == 1:
            print(msg.topic, int(msg.payload))
            procZDown.start()
        elif int(msg.payload) == 2:
            try:
                print(msg.topic, int(msg.payload))
                procZDown.terminate()
                procZDown = Process(target=zDown)
            except:
                print("There was a problem with zd process")
    else:
        pass

def publishMessage(topic, message, qos = 2):
    client.publish(topic, str(message), qos)

if __name__ == "__main__":
    # Global variables
    global stepsz
    global time_
    global procZUp
    global procZDown
    stepsz = 5
    time_ = 2000
    procZUp = Process(target = zUp)
    procZDown = Process(target = zDown)
    # Autofocus variables
    global autofocusState
    global hardwareCode
    global countFrames
    global countPositions
    global saveAutofocusCoef
    autofocusState = False
    hardwareCode = "o"
    countFrames = 0
    countPositions = 0
    saveAutofocusCoef = []
    #client.connect("test.mosquitto.org", 1883, 60)
    client.connect("192.168.0.104", 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
