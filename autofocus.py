import z_positioner as zz
import vision as vis 
import algorithms as alg
import numpy as np
import time, os, sys 

def autofocus_v1():
 zz.activate_control_loop()

 print("Reset z")
 zz.z_reset()

 print("Analysis")
 fields = []
 img = []
 for i in range(35):
  frame = vis.take_picture()
  vis.show_picture(frame)

  img.append(frame)
  frame, frame_var = vis.laplacian(frame, debug=True, gaussian=False)
  fields.append(frame_var)

  zz.z_up()
  print(frame_var, i)

 m = max(fields)
 index = fields.index(m)
 print("Start focus")
 print("Max: ", m, "Index: ", index)

 count = 0
 while(True):
  frame = vis.take_picture()
  vis.show_picture(frame)
 
  frame, frame_var = vis.laplacian(frame, debug=True, gaussian=False)
  fields.append(frame_var)

  print(frame_var, count, (frame_var-m)**2)
  count+=1

  if frame_var > m:
   print('done!')
   break
  elif ( (frame_var-m)**2 < 2):
   print('done!')
   break 
  elif ( (frame_var-m)**2 >= 2 and (frame_var-m)**2 < 150 ):
   zz.z_fine_down()
  else:
   zz.z_down()

 zz.deactivate_control_loop()

 while(True):
  frame = vis.take_picture()
  vis.show_picture(frame)
  vis.debug("Image in sequence max", img[index])

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
 for i in range(30):
  frame = vis.take_picture()
  vis.show_picture(frame)
  
  img.append(frame)
  frame, frame_var = vis.laplacian(frame, debug=True, gaussian=False)
  mic_fields.append(frame_var)
  
  zz.z_up()
  
  print(frame_var, i)

 
 # Analyse fields 
 m = max(mic_fields)
 index = mic_fields.index(m)
 print('Focus point at: ', 30-index, 'Coordinates: ', index, ',', m)

 for i in range(np.abs(30-index)):
  frame = vis.take_picture()
  vis.show_picture(frame)

  frame, frame_var = vis.laplacian(frame, debug=True, gaussian=False)

  zz.z_down()

  print(frame_var, i)

 zz.deactivate_control_loop()

 print('Focused point ')
 while(1):
  frame = vis.take_picture()
  vis.show_picture(frame)
  vis.debug('Stored_image', img[index])

def autofocus_v2():
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
 autofocus_v1()
