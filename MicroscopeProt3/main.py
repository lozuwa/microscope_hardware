'''
Author: Rodrigo Loza 
Project: click_hardware
Description: Script to move the 
x,y,z axis of the device.
'''
from z_positioner import z_controller
from nnchk import nnchk
import time, os, sys
import paho.mqtt.client as mqtt

TOPIC_ = '/'
CLIENT_ = 'test.mosquitto.org'

def reset():
  # Restart drivers 
  print('---------------Reset X-----------------------')
  wii.x_reset()
  [wii.x_left() for i in range(50)]
  print('ok')
  print('---------------Reset Y-----------------------')
  wii.y_reset()
  [wii.y_forward() for i in range(50)]
  print('ok') 
  print('---------------Reset Z-----------------------')
  zz.activate_control_loop()
  zz.z_reset()
  zz.deactivate_control_loop()
  print('ok')

def start():
  print('-----------------------------------------')
  print('Starting controllers')
  # Start objects 
  print('-----------------------------------------')
  print('Objects initialization')
  wii = nnchk()
  zz = z_controller()
  # Avoid control loop bug z axis
  print('-----------------------------------------')
  print('Starting device\'s axis')
  zz.activate_control_loop()
  time.sleep(0.1)
  zz.deactivate_control_loop()
  time.sleep(0.1)
  
  print('------------------Control Manual-------------------------')
  while(True):
    '''----------------------------Take picture----------------------------'''
    if False:
      (rc, mid) = client.publish(TOPIC_, '1', qos=2)
    '''-----------------------------Controller---------------------------'''
    data = wii.read()
    if len(data) != 0:
      # Z axis 
      if ((data[5] & 0x01) == 0) and ((data[5] & 0x02) != 0):
        print('Mover abajo')
        zz.activate_control_loop()
        try:
          zz.z_down()
        except:
          print('Failed z down') 
      elif ((data[5] & 0x02) == 0) and ((data[5] & 0x01) != 0):
        print('Mover arriba')
        zz.activate_control_loop()
        try:
          zz.z_up()
        except:
          print('Failed z up')
      elif ((data[5] & 0x02) != 0) and ((data[5] & 0x01) != 0):
        zz.deactivate_control_loop()
        # X axis 
        if data[0] > 215:
          print('Mover derecha')
          wii.x_left()
        elif data[0] < 55:
          print('Mover izquierda')
          wii.x_right()
        # Y axis
        if data[1] > 195:
          print('Mover atras')
          wii.y_forward()
        elif data[1] < 50:
          print('Mover adelante')
          wii.y_backward()

def on_publish(client, userdata, mid):
    print("mid: " + str(mid))

def exit():
  client.loop_stop()
  sys.exit()

if __name__ == '__main__':
  global client
  # Define mqtt client and start background thread  
  print('-----------------------------------------')
  print('Connecting to the client {}'.format(client_))
  client = mqtt.Client()
  client.on_publish = on_publish
  client.connect(CLIENT_, 1883)
  print('-----------------------------------------')
  print('Starting thread ...')
  client.loop_start()
  # Continue with hardware controllers 
  reset()
  start()