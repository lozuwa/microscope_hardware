import z_positioner as zz
from nnchk import nn
import time
import cv2
import numpy as np

# Variables 
cont_x_left = 0
cont_y_back = 0

cv2.namedWindow('animation')
xsize = 350
ysize = 150
img = np.zeros([ysize, xsize], np.uint8)

xis = 1
yis = 1
xes = 349
yes = 149

xir = 110
yir = 100
xer = 130
yer = 120

def nothing():
 return None 

def nothinga():
 return 0

def contx(op):
 global cont_x_left
 if op == False:
  cont_x_left -= 1
 else:
  cont_x_left += 1

def conty(op):
 global cont_y_back
 if op == False:
  cont_y_back -= 1
 else:
  cont_y_back += 1

if __name__ == '__main__':
 global cont_x_left
 global cont_y_back

 # Avoid control loop bug
 zz.init()
 zz.activate_control_loop()
 zz.deactivate_control_loop()
 
 # Start wii driver
 wii = nn()
 
 # Restart drivers 
 print('---------------Reset X-----------------------')
 wii.x_reset()
 [[wii.x_left(), contx(True)] for i in range(10)]
 print('ok')
 print('---------------Reset Y-----------------------')
 wii.y_reset()
 [[wii.y_forward(), conty(False)] for i in range(8)]
 print('ok')
 print('---------------Reset Z-----------------------')
 zz.activate_control_loop()
 zz.z_reset()
 zz.deactivate_control_loop()
 print('ok')

 print('------------------Control Manual-------------------------')
 while(True):
  ####-------------------------animation---------------------
  img = np.zeros([ysize, xsize, 3], np.uint8)
  # Slide animation 
  cv2.rectangle(img, (xis,yis), (xes,yes), (255,255,255), 4)
  cv2.line(img, (80, 1), (80, 149), (255,255,255), 3)
  cv2.rectangle(img, (100,20), (330,130), (0,255,0), 4)
  # ROI animation 
  cv2.rectangle(img, (xir,yir), (xer,yer), (255,0,0), 2)
  # Show image
  cv2.imshow('animation', img)
  cv2.waitKey(1)
  
  ####-------------------------wii---------------------
  data = wii.read()
  if len(data) != 0:
   #print(data)
   #print('x left', cont_x_left)
   #print('y back', cont_y_back)
 
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
     contx(True) if cont_x_left < 38 else nothing()
     #wii.x_left() if cont_x_left < 38 else nothing()
     xir += 11 if xir < 310 else nothinga()
     xer += 11 if xer < 330 else nothinga()
     if True:#xir < 310 and xer < 330:
      wii.x_left()
    elif data[0] < 55:
     print('Mover izquierda')
     contx(False) if data[7] == 1 else nothing()
     #wii.x_right()
     xir -= 11 if xir > 100 else nothinga()
     xer -= 11 if xer > 120 else nothinga()
     if True:#xir > 100 and xer > 120:
      wii.x_right()
    else:
     pass 
    # Y axis
    if data[1] > 195:
     print('Mover atras')
     conty(True) if cont_y_back < 12 else nothing()
     #wii.y_forward() if cont_y_back < 12 else nothing()
     yir -= 10 if yir > 20 else nothinga()
     yer -= 10 if yer > 40 else nothinga()
     if True: #yir > 20 and yer > 40:
      wii.y_forward()
    elif data[1] < 50:
     print('Mover adelante')
     conty(False) if data[6] == 1 else nothing()
     #wii.y_backward()
     yir += 10 if yir < 105 else nothinga()
     yer += 10 if yer < 125 else nothinga()
     if True: #yir < 105 and yer < 125 :
      wii.y_backward()
    else:
     pass
