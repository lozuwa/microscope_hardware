import z_positioner as zz
from nnchk import nn
import time

if __name__ == '__main__':
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
  #time.sleep(0.01)
  print(data)
 
  # Z axis 
  if ((data[5] & 0x01) == 0) and ((data[5] & 0x02) != 0):
   print('Mover arriba')
   zz.activate_control_loop()
   zz.z_up() 
  elif ((data[5] & 0x02) == 0) and ((data[5] & 0x01) != 0):
   print('Mover abajo')
   zz.activate_control_loop()
   zz.z_down()
  elif ((data[5] & 0x02) != 0) and ((data[5] & 0x01) != 0):
   # X axis 
   if data[0] > 215:
    print('Mover derecha')
    wii.x_right()
   elif data[0] < 55:
    print('Mover izquierda')
    wii.x_left()
   else:
    pass 
   # Y axis 
   if data[1] > 195:
    print('Mover adelante')
    wii.y_backward()
   elif data[1] < 50:
    print('Mover atras')
    wii.y_forward()
   else:
    pass
