from smbus import SMBus
import RPi.GPIO as gpio
import time

# ----------------------------General configurations----------------------------- #
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

class nn:
  def __init__(self,delay = 0.01):
    # Initialize GPIO 
    try:
      gpio.setup(23, gpio.IN, gpio.PUD_UP) # y positioner 
      gpio.setup(24, gpio.IN, gpio.PUD_UP) # x positioner 
    except:
      print('Failed GPIO initialization')
    # Init I2C 
    self.delay = delay
    self.arduino_address = 0x04
    self.wii_address = 0x52
    self.bus = SMBus(1)
    self.bus.write_byte_data(self.wii_address, 0x40, 0x00)
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
