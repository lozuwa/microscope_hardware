#ip 192.168.3.174

# MQTT
import paho.mqtt.client as mqtt
# Supporting libraries
import os, time, numpy as np
from Interface import *
# Thread
from multiprocessing import Process
import eventlet
eventlet.monkey_patch()

# Initialize mqtt client
client = mqtt.Client()

# Global variables
stepsz = 5
stepsxy = 5
time_ = 500
KEEP_ALIVE_TIME = 120

state = False

def z_up(s):
    global stepsz
    if state == True:
        z_s(stepsz, 1, time_)
        time.sleep(0.01)
    else:
        while(1):
            #print('z', os.getpid())
            z_s(stepsz, 1, time_)
            time.sleep(0.01)

def z_down(s):
    if state == True:
        z_s(stepsz, 0, time_)
        time.sleep(0.01)
    else:
        while(1):
            #print('z', os.getpid())
            z_s(stepsz, 0, time_)
            time.sleep(0.01)

def x_left(s):
    while(1):
        #print('x', os.getpid())
        x_s(stepsxy, 1, time_)
        time.sleep(0.01)

def x_right(s):
    while(1):
        #print('x', os.getpid())
        x_s(stepsxy, 0, time_)
        time.sleep(0.01)

def y_forward(s):
    while(1):
        #print('y', os.getpid())
        y_s(stepsxy, 1, time_)
        time.sleep(0.01)

def y_backward(s):
    while(1):
        #print('y', os.getpid())
        y_s(stepsxy, 0, time_)
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
    client.subscribe('/timemicro')
    client.subscribe('/home')
    client.subscribe('/automatic')
    client.subscribe('/movefield')
    # Camera app
    client.subscribe('/microscope')

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
        if msg.topic == '/microscope':
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
        elif msg.topic == "/timemicro":
            stepsz = float(msg.payload)*50
            print(msg.topic, stepsz)
        elif msg.topic == "/led":
            b = int(msg.payload)
            if b >= 0 and b < 50:
                b = 0
            elif b >= 50 and b <= 100:
                b = 255
            brigthness(b)
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
                    proc_z_up = Process(target=z_up, args=(5,))
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
                    proc_z_down = Process(target=z_down, args=(5,))
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
                    proc_x_left = Process(target=x_left, args=(5,))
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
                    proc_x_right = Process(target=x_right, args=(5,))
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
                    proc_y_forw = Process(target=y_forward, args=(5,))
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
                    proc_y_back = Process(target=y_backward, args=(5,))
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
    client.publish('/microscope', 'keep alive', 2)
    time.sleep(KEEP_ALIVE_TIME)

# Initialize thread
#eventlet.spawn(keep_smartphone_alive)

if __name__ == '__main__':
    # Initialize enable variable
    global enable
    enable = False

    # Background processes
    proc_z_up = Process(target=z_up, args=(5,))
    proc_z_down = Process(target=z_down, args=(5,))
    proc_y_forw = Process(target=y_forward, args=(5,))
    proc_y_back = Process(target=y_backward, args=(5,))
    proc_x_left = Process(target=x_left, args=(5,))
    proc_x_right = Process(target=x_right, args=(5,))

    #client.connect('test.mosquitto.org', 1883, 60)
    #client.connect('10.42.0.1', 1883, 60)
    client.connect('192.168.3.174', 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()

    while True:
        keep_smartphone_alive()
