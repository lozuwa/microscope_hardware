from z_positioner as z_controller
from nnchk import nn
import time 

def restart():
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

def start():
  # Start wii driver
  wii = nn()
  zz = z_controller()
  # Avoid control loop bug z axis
  zz.init()
  zz.activate_control_loop()
  zz.deactivate_control_loop()

  k = cv2.waitKey(1)
  
  print('------------------Control Manual-------------------------')
  while(True):
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
