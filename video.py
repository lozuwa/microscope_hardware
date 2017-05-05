import numpy as np
import os, sys, cv2
from threading import Thread
#from webcam import WebcamVideoStream

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

class Streamer:
  def __init__(self, use_button=False):
    # Initialize GPIO 
    if use_button:
      import RPi.GPIO as gpio 
      gpio.setmode(gpio.BCM)
      gpio.setwarnings(False)
      try:
        gpio.setup(26, gpio.IN, gpio.PUD_UP) # y positionr 
      except:
        print('Failed GPIO initialization')
    # Init camera
    self.vs = WebcamVideoStream(0).start()
    # Variables
    method = [cv2.INTER_NEAREST, cv2.INTER_LINEAR, cv2.INTER_AREA, cv2.INTER_CUBIC]
    self.tp = 1 
    self.frame = []
    self.refPt = []
    self.cropping = False
    self.ROI = np.zeros([1,1], np.uint8)
    # Image windows 
    cv2.namedWindow( "_" )
    cv2.namedWindow( "__" )
    cv2.namedWindow( "_t" )
    cv2.createTrackbar( 'x', '_t', 1, 10, self.callback )
    cv2.setMouseCallback( "_", self.click_and_crop )

  def callback(self, *arg):
    self.tp = cv2.getTrackbarPos('x', '_t')

  def click_and_crop(self, event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
      self.refPt = [ (x, y) ]
      self.cropping = True
   
    elif event == cv2.EVENT_LBUTTONUP:
      self.refPt.append( (x, y) )
      self.cropping = False
      # Update zoom screen
      self.update_zoom()

  def update_zoom(self):
    if ( (self.refPt[0][0] - self.refPt[1][0])**2  < 50) and ( (self.refPt[0][1] - self.refPt[1][1])**2 < 50 ):
      pass
    else:
      self.ROI = self.frame.copy()[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]
      cv2.rectangle( self.frame, self.refPt[0], self.refPt[1], (0, 255, 255), 2 )
      cv2.destroyWindow('__')
      cv2.waitKey(1)
      #print(ROI.shape)
      r_ = self.resize( self.ROI )
      cv2.imshow( "_", self.frame )
      cv2.imshow( "__", r_ )
      #print(r_.shape)
      cv2.waitKey( 200 )
    
  def resize(self, f_):
    return cv2.resize( f_, (f_.shape[1]*self.tp, f_.shape[0]*self.tp), self.method[0] )

  def stream(self):
    c = 0
    while( 1 ):
      self.frame = self.vs.read()
      if False: #gpio.input(26) == 0:
        cv2.imwrite( 'images/'+str(c)+'.png',self.frame )
        cv2.putText( self.frame, 'Foto tomada', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 2 )
        cv2.waitKey( 200 )
        c += 1
      cv2.imshow( '_', self.frame )
      cv2.waitKey( 1 )

  def exit(self):
    self.vs.stop()
    cv2.destroyAllWindows()
    sys.exit()

if __name__ == '__main__':
  s = Streamer()
  s.stream()