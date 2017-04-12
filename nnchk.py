##########################################
## Python module to read a Wii nunchuck ##
##                                      ##
## Written by Jason - @Boeeerb          ##
##  jase@boeeerb.co.uk                  ##
##########################################
##
## v0.1 03/05/14 - Initital release
## v0.2 21/06/14 - Retrieve one byte at a time [Simon Walters - @cymplecy]
## v0.3 22/06/14 - Minor Refactoring [Jack Wearden - @JackWeirdy]
## v0.32 25/6/14 - XOR each data byte with 0x17 and then add 0x17 to produce corrent values - Simon Walters @cymplecy
## v0.4 26/6/14 - Change method of XOR and add delay parameter - Simon Walters @cymplecy
## v0.41 30/3/15 - Adding support for RPI_REVISION 3 - John Lumley @Jelby-John

from smbus import SMBus
import RPi.GPIO as gpio
import time as time

bus = 0

# ----------------------------GPIO-----------------------------
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
try:
 gpio.setup(23, gpio.IN, gpio.PUD_UP) # y positioner 
 gpio.setup(24, gpio.IN, gpio.PUD_UP) # x positioner 
except:
 print('Failed GPIO initialization')

class nn:

 def __init__(self,delay = 0.01):
  self.delay = delay
  self.arduino_address = 0x04
  self.bus = SMBus(1)
  self.bus.write_byte_data(0x52,0x40,0x00)
  time.sleep(0.1)

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

 def x_move_center(self):
  try:
   [self.bus.write_byte(self.arduino_address, 0x04) for i in range(10)]
  except:
   pass 

 def y_move_ceter(self):
  try:
   [self.bus.write_byte(self.arduino_address, 0x05) for i in range(10)]
  except:
   pass 

 def x_reset(self):
  while(gpio.input(24) != gpio.LOW):
   self.x_right()
  for i in range(5):
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
  for i in range(5):
   self.y_forward()
  while(gpio.input(23) != gpio.LOW):
   self.y_backward()

 def read(self):
  temp = []
  try:
   self.bus.write_byte_data(0x52,0x40,0x00)
   time.sleep(self.delay)
   self.bus.write_byte(0x52,0x00)
   time.sleep(self.delay)
   temp = [(0x17 + (0x17 ^ self.bus.read_byte(0x52))) for i in range(6)]
   temp.append(gpio.input(23))
   temp.append(gpio.input(24))
  except:
   pass
  return temp

 def raw(self):
  data = self.read()
  return data

 def accelerometer(self):
  data = self.read()
  return data[2],data[3],data[4]

 def setdelay(self,delay):
  self.delay = delay
