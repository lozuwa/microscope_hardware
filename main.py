import z_positioner as zz
import xy_positioner as xy
import vision as vis 
import autofocus as autfoc
import time, os, sys

if __name__ == '__main__':
 # Restart the xy positioner 
 xy.x_reset()
 xy.y_reset()

 # Set xy positioner to starting point 
 for i in range(10):
  xy.x_left()
 for i in range(5):
  xy.y_forward()
 
 # Restart z positioner 
 #zz.z_reset()

 # --------------- Autofocus ----------------
 #autfoc.autofocus_v0()

 #---------------- Sequence of analysis ------------------------
 for j in range(10):
  if j%2 == 0:
   for i in range(30):
    f_ = take_picture()
    show_image(f_)
    xy.right()
  else:
   for i in range(30):
    f_ = take_picture()
    show_image(f_)
    xy.left()
  xy.backward()
