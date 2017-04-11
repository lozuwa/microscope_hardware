import z_positioner as zz
from nnchk import nn
import time

# Variables 
cont_x_left = 0
cont_y_back = 0

def nothing():
 pass 

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
 [wii.x_left() for i in range(10)]
 print('ok')
 print('---------------Reset Y-----------------------')
 wii.y_reset()
 [wii.y_forward() for i in range(8)]
 print('ok')
 print('---------------Reset Z-----------------------')
 zz.activate_control_loop()
 zz.z_reset()
 zz.deactivate_control_loop()
 print('ok')

 print('------------------Control Manual-------------------------')
 while(True):
  data = wii.read()
  if len(data) != 0:
   #print(data)
   #print('x left', cont_x_left)
   #print('y back', cont_y_back)
 
   # Z axis 
   if ((data[5] & 0x01) == 0) and ((data[5] & 0x02) != 0):
    print('Mover abajo')
    zz.activate_control_loop()
    zz.z_down() 
   elif ((data[5] & 0x02) == 0) and ((data[5] & 0x01) != 0):
    print('Mover arriba')
    zz.activate_control_loop()
    zz.z_up()
   elif ((data[5] & 0x02) != 0) and ((data[5] & 0x01) != 0):
    zz.deactivate_control_loop()
    # X axis 
    if data[0] > 215:
     print('Mover derecha')
     contx(False) if data[7] == 1 else nothing()
     wii.x_right()
    elif data[0] < 55:
     print('Mover izquierda')
     contx(True) if cont_x_left < 30 else nothing()
     wii.x_left() if cont_x_left < 30 else nothing()
     #wii.x_left()
    else:
     pass 
    # Y axis 
    if data[1] > 195:
     print('Mover adelante')
     conty(False) if data[6] == 1 else nothing()
     wii.y_backward()
    elif data[1] < 50:
     print('Mover atras')
     conty(True) if cont_y_back < 12 else nothing()
     wii.y_forward() if cont_y_back < 12 else nothing()
     #wii.y_forward()
    else:
     pass
