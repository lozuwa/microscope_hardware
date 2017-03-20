import z_positioner as zz
import vision as vis 
import algorithms as alg
import numpy as np
import time, os, sys 

def autofocus_v0():
 zz.activate_control_loop()

 # Z positioner has been already reseted?
 print('Reset z')
 zz.z_reset() 

 # ---------------------------AUTOFOCUS SEQUENCE----------------------------
 # Store fields for analysis
 print('Analysis')
 mic_fields = []
 img = []
 for i in range(50):
  frame = vis.take_picture()
  vis.show_picture(frame)
  
  img.append(frame)
  frame, frame_var = vis.laplacian(frame, debug=True, gaussian=False)
  mic_fields.append((frame_var, i))
  
  zz.activate_control_loop()
  zz.z_up()
  zz.deactivate_control_loop()
  
  print(i, frame_var)
 
 # Analyse fields 
 r_ = alg.get_max(mic_fields) #alg.get_max([(1,1),(2,2),(1,3)])
 print('Focus point at: ', 50-r_[1], 'Coordinates: ', r_[0], ',' ,r_[1])
 for i in range((50-r_[1]) + 15):
  frame = vis.take_picture()
  vis.show_picture(frame)

  print('Focusing ...', i)
  zz.activate_control_loop()
  zz.z_down()
  zz.deactivate_control_loop()

 zz.deactivate_control_loop()

 print('Focused point ')
 while(1):
  frame = vis.take_picture()
  vis.show_picture(frame)
  vis.debug('Stored_image', img[r_[1]])

def autofocus_v1():
 zz.activate_control_loop()

 # Z positioner has been already reseted?
 print('Reset')
 zz.z_reset()

 # --------------------- Macroscopic focus ------------------------
 print('Macroscopic focus')
 chunks = [20, 8, 4]
 biases = [4, 2, 1]
 for c, b in zip(chunks, biases):
  # Store data
  mic_fields = []
  for i in range(int(c)):

   frame = vis.take_picture()
   vis.show_picture(frame)

   frame, frame_var = vis.laplacian(frame, debug=True, gaussian=False)
   mic_fields.append((frame_var, i))
   print(i, frame_var)
        
   zz.activate_control_loop()
   zz.z_up()
   zz.deactivate_control_loop()

  # Analyse data
  r_ = alg.get_max(mic_fields)
  zeroed_position = (c - r_[1])
  for i in range(zeroed_position + b):
   zz.activate_control_loop()
   zz.z_down()
   zz.deactivate_control_loop()
 
 # ------------------------ Fine focus ---------------------------
 print('Fine focus')
 zz.activate_control_loop()
 chunks = [10, 4, 2]
 biases = [2, 1, 0]
 for c, b in zip(chunks, biases):
  # Store data
  mic_fields = []
  for i in range(int(c)):
   frame = vis.take_picture()
   vis.show_picture(frame)
   
   frame, frame_var = vis.laplacian(frame, debug=True, gaussian=False)
   mic_fields.append((frame_var, i))
   
   #zz.activate_control_loop()
   zz.z_fine_up()
   #zz.deactivate_control_loop()

  # Analyse data
  r_ = alg.get_max(mic_fields)
  zeroed_positioner = (c - r_[1])
  for i in range(zeroed_position + b):
   #zz.activate_control_loop()
   zz.z_fine_down()
   #zz.deactivate_control_loop()

 zz.deactivate_control_loop()

 print('Focused point ')
 while(1):
  frame = vis.take_picture()
  vis.show_picture(frame)
  #vis.debug('Stored_image', img[r_[1]])

if __name__ == '__main__':
 autofocus_v0()
