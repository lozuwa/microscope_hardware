import xy_positioner as xy
import z_positioner as zz
import os, sys, time 
import RPi.GPIO as gpio 
import vision as vis
import autofocus as aut 

# GLOBAL VARIABLES 
EPOCHS = 150
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(16, gpio.IN, gpio.PUD_UP) # z
gpio.setup(23, gpio.IN, gpio.PUD_UP) # x 
gpio.setup(24, gpio.IN, gpio.PUD_UP) # y

def autof():
 put_slide()
 aut.autofocus_v1()

def buttons():
 while(1):
  print('x: ', gpio.input(24))
  print('y: ', gpio.input(23))
  print('z: ', gpio.input(16))
  time.sleep(0.5)

def exit():
 zz.ser.close()

def pic():
 vis.show_picture( vis.take_picture() )

def seq():
 count = 0
 # Restart axis 
 print('reset axis')
 xy.x_reset()
 xy.y_reset()
 
 # Start sequence
 print('start sequence')
 for i in range(8):
  if i%2 == 0:
   for i in range(25):
    aut.autofocus_v3_debug(count)
    count += 1
    xy.x_left()
  else:
   for i in range(25):
    aut.autofocus_v3_debug(count)
    count += 1
    xy.x_right()
  xy.y_forward()
  aut.autofocus_v3_debug(count)
  count += 1
                          
def test_xy_positioner():
 for i in range(EPOCHS):
  print('epoch : ', i)
  xy.x_right()
  time.sleep(0.01)
  xy.x_left() 
  time.sleep(0.01)
  xy.y_forward()
  time.sleep(0.01)
  xy.y_backward()
  time.sleep(0.01)

def test_z_positioner():
 zz.activate_control_loop()
 for i in range(10):
  [zz.z_up() for i in range(20)]
  [zz.z_down() for i in range(20)]
   
 zz.deactivate_control_loop()
    
def test_squares():
 xy.x_reset()
 xy.y_reset()
 #for i in range(50):
  #zz.z_up()
 for i in range(EPOCHS):
  print('Epoch: ', i)
  #for i in range(15):
   #zz.z_down()
  [xy.y_forward() for i in range(9)]
  [xy.x_left() for i in range(40)]
  [xy.y_backward() for i in range(9)]
  [xy.x_right() for i in range(40)]
  #for i in range(15):
   #zz.z_up()

while(1):
 inpt = raw_input("Options: button, x, z, s, q, a, exit: ")
 if inpt == "x":
  test_xy_positioner()
 elif inpt == "z":
  test_z_positioner()
 elif inpt == "s":
  test_squares()
 elif inpt == "q":
  seq()
 elif inpt == "button":
  buttons()
 elif inpt == "a":
  autof()
 elif inpt == "exit":
  exit()
 else:
  continue
