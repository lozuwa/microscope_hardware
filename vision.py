import cv2
import numpy as np
import sys, os 

try:
 cap = cv2.VideoCapture(0)
except:
 print('Failed camera')

def debug(windows, frame):
 cv2.imshow(str(windows), frame)
 cv2.waitKey(1)

def show_picture(frame):
 cv2.imshow('f_', frame)
 cv2.waitKey(1)

def show_image_debug(frame, val):
 cv2.putText(frame, str(val), (320, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
 cv2.imshow('f_', frame)
 cv2.waitKey(1)

def save_image(frame, text):
 cv2.imwrite('images/'+str(text)+".png", frame)

def take_picture():
 for i in range(5):
  _, frame = cap.read()
  cv2.waitKey(1)
 return frame

def laplacian(frame, debug = False, gaussian = False):
 if debug == True:
  r_ = cv2.Laplacian(frame, cv2.CV_64F) if gaussian == False else cv2.Laplacian(cv2.GaussianBlur(frame, (5,5), 0), cv2.CV_64F)
  show_image_debug(frame, r_.var())
  return r_, r_.var()
 else:
  return cv2.Laplacian(frame, cv2.CV_64F).var() if gaussian==False else cv2.Laplacian(gaussian(frame), cv2.CV_64F).var()

def gaussian(frame):
 return cv2.GaussianBlur(frame, (5, 5), 0)

def exit():
 #cap.release()
 cv2.destroyAllWindows()
 #sys.exit()
