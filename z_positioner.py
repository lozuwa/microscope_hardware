import serial 
import numpy as np
import math
import time 
import RPi.GPIO as GPIO 
import os, sys 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

try:
 ser = serial.Serial('/dev/ttyACM0', 115200, timeout=5)
except:
 try:
  ser = serial.Serial('/dev/ttyACM1', 115200, timeout=5)
 except:
  try:
   ser = serial.Serial('/dev/ttyACM2', 115200, timeout=5)
  except:
   try:
    ser = serial.Serial('/dev/ttyACM3', 115200, timeout=5)
   except:
    print('Failed connection with device: ', ser)
    sys.exit()

GPIO.setup(16, GPIO.IN, GPIO.PUD_UP) # z positioner 

def deactivate_control_loop():
 ser.write('n')
 time.sleep(0.01)

def activate_control_loop():
 ser.write('y')
 time.sleep(0.01)

def z_up():
 ser.write('b')
 wait()

def z_down():
 if GPIO.input(16) == GPIO.LOW:
  pass 
 else:
  ser.write('z')
  wait()

def z_mid_up():
 ser.write('B')
 wait()

def z_mid_down():
 if GPIO.input(16) == GPIO.LOW:
  pass 
 else:
  ser.write('Z')
  wait()

def z_fine_up():
 ser.write('6')
 wait()

def z_fine_down():
 if GPIO.input(16) == GPIO.LOW:
  pass 
 else:
  ser.write('9')
  wait()

def wait():
 while (ser.read() != 'o'):
  continue

def z_reset():
 while(GPIO.input(16) != GPIO.LOW):
  z_down()
 for i in range(25):
  z_up()
 #while(GPIO.input(18) != GPIO.LOW):
 # z_down()

def exit():
 ser.close()
 sys.exit()
