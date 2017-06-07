import paho.mqtt.client as mqtt
import numpy as np
import os, time
from multiprocessing import Process
from Interface_mic import *

enable = False
stepsz = 5
stepsxy = 5
time_ = 500

def z_up(s):
    while(1):
        print('z', os.getpid())
        z_s(stepsz, 1, time_)

def z_down(s):
    while(1):
        print('z', os.getpid())
        z_s(stepsz, 0, time_)

def x_left(s):
    while(1):
        print('x', os.getpid())
        x_f(stepsxy, 1, time_)

def x_right(s):
    while(1):
        print('x', os.getpid())
        x_f(stepsxy, 0, time_)

def y_forward(s):
    while(1):
        print('y', os.getpid())
        y_s(stepsxy, 1, time_)

def y_backward(s):
    while(1):
        print('y', os.getpid())
        y_s(stepsxy, 0, time_)

# Subscribe topics
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/connect")
    client.subscribe("/zu")
    client.subscribe("/zd")
    client.subscribe("/yb")
    client.subscribe("/yf")
    client.subscribe("/xl")
    client.subscribe("/xr")
    client.subscribe('/led')
    client.subscribe('/stepsmicro')
    client.subscribe('/timemicro')

# Reply messages
def on_message(client, userdata, msg):
    global enable
    global stepsxy
    global stepsz
    global time_
    global proc_z_up
    global proc_z_down
    global proc_y_forw
    global proc_y_back
    global proc_x_left
    global proc_x_right

    #print(msg.topic, msg.payload)
    if msg.topic == "/connect":
        enable = True if int(msg.payload) == 1 else False
        if int(msg.payload) == 1:
            print('server enabled')
    if enable == True:
        if msg.topic == "/stepsmicro":
            t = float(msg.payload) #int((float(msg.payload) / 100) * 20)
            print(msg.topic, t)
            stepsz = t
        elif msg.topic == "/timemicro":
            tt = float(msg.payload) #int((float(msg.payload) / 100) * 1000)
            print(msg.topic, tt)
            time_ = tt
        elif msg.topic == "/led":
            print(msg.topic, msg.payload, type(int(msg.payload)))
            brigthness(int(msg.payload))
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

if __name__ == '__main__':
    proc_z_up = Process(target=z_up, args=(5,))
    proc_z_down = Process(target=z_down, args=(5,))
    proc_y_forw = Process(target=y_forward, args=(5,))
    proc_y_back = Process(target=y_backward, args=(5,))
    proc_x_left = Process(target=x_left, args=(5,))
    proc_x_right = Process(target=x_right, args=(5,))

    client = mqtt.Client()
    client.connect('test.mosquitto.org', 1883, 60)
    #client.connect('10.42.0.1', 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
