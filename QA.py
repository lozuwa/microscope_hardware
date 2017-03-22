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

gpio.setup(18, gpio.IN, gpio.PUD_UP) # z
gpio.setup(23, gpio.IN, gpio.PUD_UP) # x 
gpio.setup(24, gpio.IN, gpio.PUD_UP) # y

def autof():
 put_slide()
 aut.autofocus_v1()

def buttons():
 while(1):
  print('z: ', gpio.input(18))
  print('x: ', gpio.input(23))
  print('y: ', gpio.input(24))
  time.sleep(0.5)

def exit():
 zz.ser.close()

def pic():
 vis.show_picture( vis.take_picture() )

def seq():
 count = 0

 xy.y_reset()
 xy.x_reset()
 # Starting point 
 print('start point')
 [xy.y_forward() for i in range(1)]
 [xy.x_left() for i in range(15)]
 time.sleep(0.5)

 # sequence
 print('sequence')
 for i in range(6):
  if i%2==0:
   for i in range(35):
    aut.autofocus_v1(count)
    count += 1
    #pic()
    xy.x_left()
   #[xy.x_left() for i in range(35)]
  else:
   for i in range(35):
    aut.autofocus_v1(count)
    count += 1
    #pic()
    xy.x_right()
   #[xy.x_right() for i in range(35)]
  [xy.y_forward() for i in range(2)]
  [xy.y_backward() for i in range(1)]
  aut.autofocus_v1(count)
  count += 1
  #pic()

 # Reset again 
 xy.y_reset()
 xy.x_reset()
                          
 vis.exit()
                          
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

def center_slide():
 #xy.y_reset()
 #xy.x_reset()
 [xy.y_forward() for i in range(6)]
 [xy.x_left() for i in range(15)]

def put_slide():
 xy.y_reset()   
 xy.x_reset()   
 [xy.y_forward() for i in range(6)]  
 [xy.x_left() for i in range(25)]   

while(1):
 inpt = raw_input("Options: x, z, s, c, p, q, a, exit: ")
 if inpt == "x":
  test_xy_positioner()
 elif inpt == "z":
  test_z_positioner()
 elif inpt == "s":
  test_squares()
 elif inpt == "c":
  center_slide()
 elif inpt == 'p':
  put_slide()
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
