''' 
Author: Rodrigo Loza 
Project: click_hardware
Description: Script dedicated to build a serial communication 
with a mechaduino. 
'''
import serial as ses 
import math, time 
import RPi.gpio as gpio 
import os, sys 

# ----------------------------General configurations----------------------------- #
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

class z_controller: 
  def __init__(self, delay=0.01):
    # Init variables 
    self.delay = delay
    # Init serial port 
    try:
      ser = serial.Serial('/dev/ttyACM0', 115200, timeout=2)
    except:
      print('Failed connection with device: ', ser)
      sys.exit()
    # Init GPIO 
    gpio.setup(16, gpio.IN, gpio.PUD_UP) 
    # Start mechaduino in control-loop
    ser.write('x')
    time.sleep(self.delay)

  def activate_control_loop(self):
    ser.write('y')
    time.sleep(self.delay)

  def deactivate_control_loop(self):
    ser.write('n')
    time.sleep(self.delay)

  def z_up(self):
    ser.write('B')
    self.wait()

  def z_down(self):
    if gpio.input(16) == gpio.LOW:
      pass
    else:
      ser.write('B')
      self.wait()

  def wait(self):
    counter = 0
    while (ser.read() != 'o'):
      counter += 1
      if counter == 100:
        print('broken point')
        break
      continue

  def exit(self):
    ser.close()
    sys.exit()