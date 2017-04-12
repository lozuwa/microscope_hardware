import cv2
import numpy as np
import os, sys
import RPi.GPIO as gpio 

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
try:
 gpio.setup(26, gpio.IN, gpio.PUD_UP) # y positionr 
except:
 print('Failed GPIO initialization')

try:
 cap = cv2.VideoCapture(0)
except:
 try:
  cap = cv2.VideoCapture(1)
 except:
  try:
   cap = cv2.VideoCapture(2)
  except:
   print('no camera')
   sys.exit()

def vision():
 c = 0
 while(1):
  ret, frame = cap.read()
  #frame = cv2.resize(frame, (720,640))
  if gpio.input(26) == 0:
   cv2.imwrite( 'images/' + str(c) + '.png', frame )
   cv2.putText(frame, 'Foto tomada', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 2)
   cv2.imshow('_', cv2.resize(frame,(720,640)))
   cv2.waitKey(200)
   c += 1
  cv2.imshow('_', frame)#cv2.resize(frame,(720,640))) #cv2.pyrUp(frame, dstsize=(frame.shape[1]*1, frame.shape[0]*1)))
  cv2.waitKey(1)

def exit():
 cap.release()
 cv2.destroyAllWindows()
 sys.exit()

vision()
