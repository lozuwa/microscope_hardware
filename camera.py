import numpy as np
import os, sys, cv2
import RPi.GPIO as gpio 

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

class Camera():
  def __init__(self):
    # Initialize GPIO 
    try:
      gpio.setup(26, gpio.IN, gpio.PUD_UP) # y positionr 
    except:
      print('Failed GPIO initialization')
    # Init camera 
    try:
      self.cap = cv2.VideoCapture(0)
    except:
      print('No camera')
      sys.exit()

  def vision():
    c = 0
    while(1):
      ret, frame = self.cap.read()
      #frame = cv2.resize(frame, (720,640))
      if gpio.input(26) == 0:
        cv2.imwrite( 'images/'+str(c)+'.png',frame )
        cv2.putText( frame, 'Foto tomada', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 2 )
        cv2.imshow('_', cv2.resize(frame,(720,640)))
        cv2.waitKey(200)
        c += 1
      cv2.imshow('_', frame)
      cv2.waitKey(1)

  def exit():
    self.cap.release()
    cv2.destroyAllWindows()
    sys.exit()