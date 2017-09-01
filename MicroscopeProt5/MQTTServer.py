#ip 192.168.3.174

# General purpose
import os
import sys 
import time
# MQTT
import paho.mqtt.client as mqtt
# Support libraries
from Interface import *
# Thread
from multiprocessing import Process

# Initialize mqtt client
client = mqtt.Client()

# Global variables
stepsz = 5
stepsxy = 1
time_ = 500
KEEP_ALIVE_TIME = 120

def z_up():
    global stepsz
    while(1):
        z(stepsz, 1, time_)
        time.sleep(0.01)

def z_down():
    while(1):
        #print('z', os.getpid())
        z(stepsz, 0, time_)
        time.sleep(0.01)

def x_left():
    while(1):
        #print('x', os.getpid())
        x(stepsxy, 1, time_)
        time.sleep(0.01)

def x_right():
    while(1):
        #print('x', os.getpid())
        x(stepsxy, 0, time_)
        time.sleep(0.01)

def y_forward():
    while(1):
        #print('y', os.getpid())
        y(stepsxy, 1, time_)
        time.sleep(0.01)

def y_backward():
    while(1):
        #print('y', os.getpid())
        y(stepsxy, 0, time_)
        time.sleep(0.01)

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
    client.subscribe('/steps')
    client.subscribe('/home')
    client.subscribe('/automatic')
    client.subscribe('/movefield')
    # Camera app
    client.subscribe('/microscope')
    # Autofocus
    client.subscribe('/variance')

# Reply messages
def on_message(client, userdata, msg):
    global enable
    global time_
    global proc_z_up
    global proc_z_down
    global proc_y_forw
    global proc_y_back
    global proc_x_left
    global proc_x_right
    global stepsz

    #print(msg.topic, msg.payload)
    if msg.topic == "/connect":
        enable = True if int(msg.payload) == 1 else False
        if int(msg.payload) == 1:
            print('server enabled')
    if enable == True:
        if msg.topic == '/variance':
            print(msg.topic, float(msg.payload))
        elif msg.topic == '/microscope':
            pass
            #print(msg.topic, msg.payload)
            #time.sleep(1)
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
        elif msg.topic == "/steps":
            stepsz = float(msg.payload)*10
            print(msg.topic, stepsz)
        elif msg.topic == "/led":
            if int(msg.payload) == 0 :
                brigthness(0)
            elif int(msg.payload) == 1:
                brigthness(1)
            print(msg.topic, msg.payload)
        elif msg.topic == "/zu":
            if int(msg.payload) == 0:
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 1:
                proc_z_up.start()
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 2:
                try:
                    proc_z_up.terminate()
                    proc_z_up = Process(target=z_up)
                    print(msg.topic, int(msg.payload))
                except:
                    print('There was a problem')
            else:
                pass
        elif msg.topic == "/zd":
            if int(msg.payload) == 0:
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 1:
                print(msg.topic, int(msg.payload))
                proc_z_down.start()
            elif int(msg.payload) == 2:
                try:
                    print(msg.topic, int(msg.payload))
                    proc_z_down.terminate()
                    proc_z_down = Process(target=z_down)
                except:
                    print('There was a problem')
            else:
                pass
        elif msg.topic == "/xl":
            if int(msg.payload) == 0:
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 1:
                proc_x_left.start()
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 2:
                try:
                    proc_x_left.terminate()
                    proc_x_left = Process(target=x_left)
                    print(msg.topic, int(msg.payload))
                except:
                    print('There was a problem')
            else:
                pass
        elif msg.topic == "/xr":
            if int(msg.payload) == 0:
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 1:
                proc_x_right.start()
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 2:
                try:
                    proc_x_right.terminate()
                    proc_x_right = Process(target=x_right)
                    print(msg.topic, int(msg.payload))
                except:
                    print('There was a problem')
            else:
                pass
        elif msg.topic == "/yf":
            if int(msg.payload) == 0:
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 1:
                proc_y_forw.start()
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 2:
                try:
                    proc_y_forw.terminate()
                    proc_y_forw = Process(target=y_forward)
                    print(msg.topic, int(msg.payload))
                except:
                    print('There was a problem')
            else:
                pass
        elif msg.topic == "/yb":
            if int(msg.payload) == 0:
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 1:
                proc_y_back.start()
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 2:
                try:
                    proc_y_back.terminate()
                    proc_y_back = Process(target=y_backward)
                    print(msg.topic, int(msg.payload))
                except:
                    print('There was a problem')
            else:
                pass
        else:
            pass
    else:
        print('server not enabled')

def keep_smartphone_alive():
    client.publish('/microscope', 'keep alive', qos = 2, retain = False)
    time.sleep(KEEP_ALIVE_TIME)

# Initialize thread
#eventlet.spawn(keep_smartphone_alive)

if __name__ == '__main__':
    # Initialize enable variable
    global enable
    enable = False

    if sys.argv[1] == 1:
        ID = "pfm'S pc"
        BROKER = "192.168.3.193"
        PORT = 1883
    elif sys.argv[1] == 2:
        ID = "rodrigo's pc"
        BROKER = "192.168.3.213"
        PORT = 1883
    else:
        ID = "Cloud server"
        BROKER = "test.mosquitto.org"
        PORT = 1883

    print("Connecting to {} through {}. ID: {}".format(BROKER, PORT, ID))

    # Background processes
    proc_z_up = Process(target=z_up)
    proc_z_down = Process(target=z_down)
    proc_y_forw = Process(target=y_forward)
    proc_y_back = Process(target=y_backward)
    proc_x_left = Process(target=x_left)
    proc_x_right = Process(target=x_right)

    #client.connect('test.mosquitto.org', 1883, 60)
    client.connect(BROKER, PORT, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()

    while True:
        keep_smartphone_alive()
