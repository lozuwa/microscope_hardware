''' 
Author: Rodrigo Loza 
Project: click_hardware
Description: Script dedicated to build a serial communication 
with a mechaduino. 
'''
import serial as ses 
import sys, os, time 
import RPi.GPIO as gpio 

# ----------------------------General configurations----------------------------- #
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

class z_controller: 
  def __init__(self, delay=0.01):
    # Init variables 
    self.delay = delay
    # Init serial port 
    try:
      self.ser = ses.Serial('/dev/ttyACM0', 115200, timeout=1)
    except:
      print('Failed connection with device: ', ser)
      sys.exit()
    # Init GPIO 
    gpio.setup(16, gpio.IN, gpio.PUD_UP) 
    # Start mechaduino in control-loop
    self.ser.write('x')
    time.sleep(self.delay)

  def wait(self):
    counter = 0
    while (ser.read() != 'o'):
      counter += 1
      if counter > 100:
        print('broken point')
        #break
        self.recover_serial_port()
      continue

  def recover_serial_port(self):
    print('Trying to restart serial port')
    self.ser.port = '/dev/ttyACM1' 
    time.sleep(1)
    
  def activate_control_loop(self):
    self.ser.write('y')
    time.sleep(self.delay)

  def deactivate_control_loop(self):
    self.ser.write('n')
    time.sleep(self.delay)

  def z_up(self):
    self.ser.write('Z')
    self.wait()

  def z_down(self):
    if gpio.input(16) == gpio.LOW:
      pass
    else:
      self.ser.write('B')
      self.wait()

  def z_reset(self):
    while( gpio.input(16) != gpio.LOW ):
      self.z_down()
    for i in range(50):
      self.z_up()

  def exit(self):
    self.ser.close()
    sys.exit()