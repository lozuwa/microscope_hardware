from threading import Thread 
import os, sys
import cv2

class WebcamVideoStream:
  def __init__(self, src=0):
    # Initialize the video camera stream and read the first frame from the stream 
    try:
      self.stream = cv2.VideoCapture(src)
      self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #1280)
      self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) #1024)
    except:
      print('Bad camera driver')
      sys.exit()
    (self.grabbed, self.frame) = self.stream.read()
    # Initialize the variable used to indicate if the thread should be stopped
    self.stopped = False

  def start(self):
    Thread(target=self.update, args=()).start()
    return self

  def update(self):
    while True:
      if self.stopped:
        return
      (self.grabbed, self.frame) = self.stream.read()

  def read(self):
    return self.frame

  def stop(self):
    self.stopped = True   
    self.stream.release()
