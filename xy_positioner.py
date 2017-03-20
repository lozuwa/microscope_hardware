import serial 
import numpy as np
import math 
import time 
import RPi.GPIO as GPIO
import smbus

# -------------------- GPIO ----------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# -------------------- I2C -----------------------
bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x04 # 7 bit address (will be left shifted to add the read write bit)

try:
 GPIO.setup(23, GPIO.IN, GPIO.PUD_UP) # x positioner 
 GPIO.setup(24, GPIO.IN, GPIO.PUD_UP) # y positioner 
except:
 print('Failed GPIO initialization')

# bus.write_byte(int addr, char val)
# bus.read_byte(int addr)

def wait():
 r_ = 'm'
 while(r_ != 3):
  r_ = bus.read_byte(DEVICE_ADDRESS)
  #print(r_)

def x_right():
 if GPIO.input(23) == GPIO.LOW:
  pass 
 else:
  bus.write_byte(DEVICE_ADDRESS, 0x07)
  wait()

def x_left():
 bus.write_byte(DEVICE_ADDRESS, 0x04)
 wait()

def x_reset():
 while(GPIO.input(23) != GPIO.LOW):
  x_right()
 for i in range(5):
  x_left()
 while(GPIO.input(23) != GPIO.LOW):
  x_right()

def y_forward():
 bus.write_byte(DEVICE_ADDRESS, 0x08)
 wait()

def y_backward():
 if GPIO.input(24) == GPIO.LOW:
  pass 
 else:
  bus.write_byte(DEVICE_ADDRESS, 0x05)
  wait()

def y_reset():
 while(GPIO.input(24) != GPIO.LOW):
  y_backward()
 for i in range(3):
  y_forward()
 while(GPIO.input(24) != GPIO.LOW):
  y_backward()
