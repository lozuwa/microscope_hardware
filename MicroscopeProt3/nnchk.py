''' 
Author: Rodrigo Loza 
Project: click_hardware 
Description: Multi-purpose script
* Library for reading a wii's nunchuck data values. 
* 2-dimensional controller with I2C communication (MASTER). 
  Requires an arduino script to work with. Bidirectional 
  communication with a slave.
'''
from smbus import SMBus
import RPi.GPIO as gpio
import time, os, sys 

# ----------------------------General configurations----------------------------- #
gpio.se tmode(gpio.BCM)
gpio.setwarnings(False)

class nnchk:
  def __init__(self, delay = 0.01):
    # Init variables 
    self.delay = delay
    # Init GPIO 
    try:
      gpio.setup(23, gpio.IN, gpio.PUD_UP) # y positioner 
      gpio.setup(24, gpio.IN, gpio.PUD_UP) # x positioner 
    except:
      print('Failed GPIO initialization')
    # Init I2C 1
    self.arduino_address = 0x04
    self.wii_address = 0x52
    self.bus = SMBus(1)
    # Start the wii nunchuck 
    self.bus.write_byte_data(self.wii_address, 0x40, 0x00)
    time.sleep(self.delay)

  def wait(self):
    while(self.bus.read_byte(self.arduino_address) != 3):
      #r_ = self.bus_read_byte(self.arduino_address)
      continue

  def x_right(self):
    if gpio.input(24) == gpio.LOW:
      pass
    else:
      try:
        self.bus.write_byte(self.arduino_address, 0x07)
        self.wait()
      except:
        pass

  def x_left(self):
    try:
      self.bus.write_byte(self.arduino_address, 0x04)
      self.wait()
    except: 
      pass 

  def x_reset(self):
    while(gpio.input(24) != gpio.LOW):
      self.x_right()
    for i in range(50):
      self.x_left()
    while(gpio.input(24) != gpio.LOW):
      self.x_right()

  def y_forward(self):
    try:
      self.bus.write_byte(self.arduino_address, 0x08)
      self.wait()
    except:
      pass

  def y_backward(self):
    if gpio.input(23) == gpio.LOW:
      pass
    else: 
      try:
        self.bus.write_byte(self.arduino_address, 0x05)
        self.wait()
      except:
        pass 

  def y_reset(self):
    while(gpio.input(23) != gpio.LOW):
      self.y_backward()
    for i in range(50):
      self.y_forward()
    while(gpio.input(23) != gpio.LOW):
      self.y_backward()

  def read(self):
    ''' Write into the nnchk's register
        and extract the data. '''
    temp = []
    try:
      # Write register to init nunchuck 
      self.bus.write_byte_data(self.wii_address, 0x40, 0x00)
      time.sleep(self.delay)
      # Write nunchuck's register and ask for data
      self.bus.write_byte(self.wii_address, 0x00)
      time.sleep(self.delay)
      # Read register 
      temp = [(0x17 + (0x17 ^ self.bus.read_byte(0x52))) for i in range(6)]
      # Append button values 
      temp.append(gpio.input(23))
      temp.append(gpio.input(24))
    except:
      print('Failed nunchuck communication')
    return temp

  def accelerometer(self):
    ''' Accelerometer data values extracted from reading stream '''
    data = self.read()
    return data[2],data[3],data[4]

  def exit(self):
    sys.exit()