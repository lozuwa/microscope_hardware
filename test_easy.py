import xy_positioner as xy 
import z_positioner as zz
import os, sys 

def up(x, ch):
 zz.activate_control_loop()
 if ch == 0:
  [zz.z_up() for i in range(int(x))] 
 elif ch == 1:
  [zz.z_mid_up() for i in range(int(x))]
 elif ch == 2:
  [zz.z_fine_up() for i in range(int(x))]
 else:
  pass
 #zz.deactivate_control_loop()

def down(x, ch):
 zz.activate_control_loop()
 if ch == 0:
  [zz.z_down() for i in range(int(x))]
 elif ch == 1:
  [zz.z_mid_down() for i in range(int(x))]
 elif ch == 2:
  [zz.z_fine_down() for i in range(int(x))]
 else:
  pass 
 #zz.deactivate_control_loop()

def right(x):
 [xy.x_right() for i in range(int(x))]

def left(x):
 [xy.x_left() for i in range(int(x))]

def seq(x):
 for i in range(int(x)):
  up()
  left()
  down()
  right()

def exit():
 zz.ser.close()
 sys.exit()

