import paho.mqtt.client as mqtt
import numpy as np
import os, time 
from multiprocessing import Process

enable = False

def z_up(steps):
    while(1):
        print('z', os.getpid())
        #ser.write('1')

def z_down(steps):
    while(1):
        print('z', os.getpid())
        #ser.write('1') 

def x_left(steps):
    while(1):
        print('x', os.getpid())
        #ser.write('1')

def x_right(steps):
    while(1):
        print('x', os.getpid())
        #ser.write('1')

def y_forward(steps):
    while(1):
        print('y', os.getpid())
        #ser.write('1')

def y_backward(steps):
    while(1):
        print('y', os.getpid())
        #ser.write('1')

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

# Reply messages
def on_message(client, userdata, msg):
    global enable
    global proc_z_up
    global proc_z_down
    global proc_y_forw
    global proc_y_back
    global proc_x_left
    global proc_x_right
    #print(msg.topic, int(msg.payload))
    if msg.topic == "/connect":
        enable = True if int(msg.payload) == 1 else False
        if int(msg.payload) == 1:
            print('server enabled')
    if enable == True:
        if msg.topic == "/zu":
            if int(msg.payload) == 0:
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 1:
                proc_z_up.start()
                print(msg.topic, int(msg.payload))                
            elif int(msg.payload) == 2:
                proc_z_up.terminate()
                proc_z_up = Process(target=z_up, args=(5,))
                print(msg.topic, int(msg.payload))
            else:
                pass 
        elif msg.topic == "/zd":
            if int(msg.payload) == 0:
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 1:
                print(msg.topic, int(msg.payload))
                proc_z_down.start()
            elif int(msg.payload) == 2:
                print(msg.topic, int(msg.payload))
                proc_z_down.terminate()
                proc_z_down = Process(target=z_down, args=(5,))
            else:
                pass 
        elif msg.topic == "/xl":
            if int(msg.payload) == 0:
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 1:
                proc_x_left.start()
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 2:
                proc_x_left.terminate()
                proc_x_left = Process(target=x_left, args=(5,))
                print(msg.topic, int(msg.payload))
            else:
                pass    
        elif msg.topic == "/xr":
            if int(msg.payload) == 0:
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 1:
                proc_x_right.start()
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 2:
                proc_x_right.terminate()
                proc_x_right = Process(target=x_right, args=(5,))
                print(msg.topic, int(msg.payload))
            else:
                pass
        elif msg.topic == "/yf":
            if int(msg.payload) == 0:
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 1:
                proc_y_forw.start()
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 2:
                proc_y_forw.terminate()
                proc_y_forw = Process(target=y_forward, args=(5,))
                print(msg.topic, int(msg.payload))
            else:
                pass 
        elif msg.topic == "/yb":
            if int(msg.payload) == 0:
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 1:
                proc_y_back.start()
                print(msg.topic, int(msg.payload))
            elif int(msg.payload) == 2:
                proc_y_back.terminate()
                proc_y_back = Process(target=y_backward, args=(5,))
                print(msg.topic, int(msg.payload))
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
