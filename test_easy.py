import xy_positioner as xy 
import z_positioner as zz
import os, sys 

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

def restart():
 xy.x_reset()
 xy.y_reset()

def exit():
 zz.ser.close()
 sys.exit()

