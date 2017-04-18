from threading import Thread 
import cv2

class WebcamVideoStream:
  def _init_(self, src=0):
    # Initialize the video camera stream and read the first frame from the stream 
    self.stream = cv2.VideoCapture(src)
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
