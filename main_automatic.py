import xy_positioner as xy
import z_positioner as zz
import autofocus as aut

if __name__ == '__main__':
 # Avoid control loop bug 
 aut.zz.deactivate_control_loop()
 aut.zz.activate_control_loop()
 aut.zz.deactivate_control_loop()

 # Restart drivers 
 print('---------------X reset-----------------------')
 xy.x_reset()
 [xy.x_left() for i in range(10)]
 print('---------------Y reset-----------------------')
 xy.y_reset()
 [xy.y_forward() for i in range(8)]
 print('---------------Z reset-----------------------')
 aut.zz.activate_control_loop()
 aut.zz.z_reset()

 # Initial autofocus 
 aut.autofocus_v3_debug(0)

 # Start sequence 
 for i in range(5):
  if i%2==0:
   for i in range(10):
    xy.x_left()
    aut.refocus_v3()
  else:
   for i in range(10):
    xy.x_right()
    refocus_v3()
  [xy.y_forward() for i in range(2)]
  refocus_v3()

 # Restart drivers 
 xy.x_reset()
 xy.y_reset()
 zz.z_reset()
