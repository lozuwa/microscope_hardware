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

  def __init__(self,delay = 0.05):
    self.delay = delay
    
    # Addresses 
    self.wii_address = 0x52
    self.arduino_address = 0x04

    # Wii start 
    self.bus = SMBus(1)
    self.bus.write_byte_data(0x52,0x40,0x00)
    time.sleep(0.1)
  
  def wait(self):
   r_ = 0
   while(r_ != 3):
    r_ = self.bus.read_byte(self.arduino_address)

  def x_right(self):
   if gpio.input(24) == gpio.LOW:
    pass
   else:
    self.bus.write_byte(self.arduino_address, 0x07)
    self.wait()
  
  def x_left(self):
   self.bus.write_byte(self.arduino_address, 0x04)
   self.wait()

  def x_reset(self):
   while(gpio.input(24) != gpio.LOW):
    self.x_right()
   for i in range(5):
    self.x_left()
   while(gpio.input(24) != gpio.LOW):
    self.x_right()

  def y_forward(self):
   self.bus.write_byte(self.arduino_address, 0x08)
   self.wait()

  def y_backward(self):
   if gpio.input(23) == gpio.LOW:
    pass 
   else:
    self.bus.write_byte(self.arduino_address, 0x05)
    self.wait()

  def y_reset(self):
   while(gpio.input(23) != gpio.LOW):
    self.y_backward()
   for i in range(5):
    self.y_forward()
   while(gpio.input(23) != gpio.LOW):
    self.y_backward()  
   
  def read(self):
    self.bus.write_byte(0x52,0x00)
    time.sleep(0.01)
    temp = [(0x17 + (0x17 ^ self.bus.read_byte(0x52))) for i in range(6)]
    return temp

  def raw(self):
    self.bus.write_byte_data(0x52,0x40,0x00)
    time.sleep(0.01)
    data = self.read()
    return data

  def joystick(self):
    data = self.read()
    return data[0],data[1]

  def accelerometer(self):
    data = self.read()
    return data[2],data[3],data[4]

  def button_c(self):
    data = self.read()
    butc = (data[5] & 0x02)

    return butc == 0

  def button_z(self):
    data = self.read()
    butc = (data[5] & 0x01)
    return butc == 0

  def joystick_x(self):
    data = self.read()
    return data[0]

  def joystick_y(self):
    data = self.read()
    return data[1]

  def accelerometer_x(self):
    data = self.read()
    return data[2]

  def accelerometer_y(self):
    data = self.read()
    return data[3]

  def accelerometer_z(self):
    data = self.read()
    return data[4]
    
  def setdelay(self,delay):
    self.delay = delay

  def scale(self,value,_min,_max,_omin,_omax):
    return (value - _min) * (_omax - _omin) // (_max - _min) + _omin

