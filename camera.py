import cv2
import numpy as np
import os, sys

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
 while(1):
  ret, frame = cap.read()
  cv2.imshow('_', frame)
  cv2.waitKey(10)

def exit():
 cap.release()
 cv2.destroyAllWindows()
 sys.exit()

