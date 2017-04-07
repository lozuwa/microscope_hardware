import xy_positioner as xy 
import z_positioner as zz
import os, sys 
import time 

def z_init():
 zz.init()
 zz.activate_control_loop()
 time.sleep(0.5)
 zz.deactivate_control_loop()
 time.sleep(0.5)

def up(x, ch):
 zz.activate_control_loop()
 if ch == 0:
  [zz.z_up() for i in range(int(x))]
 elif ch == 1:
  [zz.z_mid_up() for i in range(int(x))]
 else:
  pass
 zz.deactivate_control_loop()

def down(x, ch):
 zz.activate_control_loop()
 if ch == 0:
  [zz.z_down() for i in range(int(x))]
 elif ch == 1:
  [zz.z_mid_down() for i in range(int(x))]
 else:
  pass 
 zz.deactivate_control_loop()

def forw(x):
 [xy.y_forward() for i in range(int(x))]

def back(x):
 [xy.y_backward() for i in range(int(x))]

def right(x):
 [xy.x_right() for i in range(int(x))]

def left(x):
 [xy.x_left() for i in range(int(x))]

def z_restart():
 zz.activate_control_loop()
 zz.z_reset()
 zz.deactivate_control_loop()

def xy_restart():
 xy.x_reset()
 xy.y_reset()

def sweep():
 xy_restart()
 z_restart()
 left(10)
 forw(8)
 for i in range(10):
  if i%2 == 0:
   for j in range(25):
    left(1)
  else:
   for k in range(25):
    right(1)
  forw(1)

def exit():
 zz.ser.close()
 sys.exit()
