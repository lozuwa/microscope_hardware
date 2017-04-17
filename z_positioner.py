import serial 
import numpy as np
import math, time 
import RPi.GPIO as GPIO 
import os, sys 

try:
  ser = serial.Serial('/dev/ttyACM0', 115200, timeout=2)
except:
  try:
    ser = serial.Serial('/dev/ttyACM1', 115200, timeout=2)
  except:
    print('Failed connection with device: ', ser)
    sys.exit()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN, GPIO.PUD_UP) # z positioner

class z_controller():
  def __init__(self):
    ser.write('x')
    time.sleep(0.01)

  def deactivate_control_loop(self):
    ser.write('n')
    time.sleep(0.01)

  def activate_control_loop(self):
    ser.write('y')
    time.sleep(0.01)

  def z_up(self):
    ser.write('b')
    wait()

  def z_down(self):
    if GPIO.input(16) == GPIO.LOW:
      pass
    else:
      ser.write('z')
      wait()

  def z_mid_up(self):
    ser.write('B')
    wait()

  def z_mid_down(self):
    if GPIO.input(16) == GPIO.LOW:
      pass 
    else:
      ser.write('Z')
      wait()

  def wait(self):
    counter = 0
    while (ser.read() != 'o'):
      counter += 1
      if counter == 100:
        print('broken point')
        break
      continue

  def z_reset(self):
    while(GPIO.input(16) != GPIO.LOW):
      self.z_down()
    for i in range(25):
      self.z_up()
    #while(GPIO.input(18) != GPIO.LOW):
    #  z_down()

  def exit(self):
    ser.close()
    sys.exit()
