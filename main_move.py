import z_positioner as zz
from nunchuck import nn 

if __name__ == '__main__':
 # Avoid control loop bug 
 zz.deactivate_control_loop()
 zz.activate_control_loop()
 zz.deactivate_control_loop()

 # Start all the necessary drivers 
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
 print('ok')

 print('------------------Control Manuela-------------------------')
 while(True):
  data = wii.raw()
  print(data)
  # X axis 
  if data[0] > 215:
   print('Mover derecha')
   wii.x_right()
  elif data[0] < 55:
   print('Mover izquierda')
   wii.x_left()
  else:
   pass 
 
  # Z axis (z button)
  if (data[5] & 0x01) == False:
   if data[1] > 195:
    print('Mover arriba')
    zz.z_up()
   elif data[1] < 50:
    print('Mover abajo')
    zz.z_down()
   else:
    pass 
  # Y axis 
  elif (data[5] & 0x01) == True:
   if data[1] > 195:
    print('Mover adelante')
    wii.y_forward()
   elif data[1] < 50:
    print('Mover atras')
    wii.y_backward()
   else:
    pass
  else:
   pass

  if (data[5] & 0x02) == False:
   print('Tomar fotografia')
  else:
   pass 
 
 # Restart drivers 
 wii.x_reset() 
 wii.y_reset()
 zz.z_reset()
