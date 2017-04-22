import numpy as np
import os, sys, cv2
from webcam import WebcamVideoStream
#import RPi.GPIO as gpio 

#gpio.setmode(gpio.BCM)
#gpio.setwarnings(False)

class Camera:
  def __init__(self):
    # Initialize GPIO 
    '''try:
      gpio.setup(26, gpio.IN, gpio.PUD_UP) # y positionr 
    except:
      print('Failed GPIO initialization')'''
    # Init camera
    self.vs = WebcamVideoStream(0).start()
    # Variables 
    self.frame = []
    self.refPt = []
    self.cropping = False
    self.update_roi = False 
    self.ROI = np.zeros([1,1], np.uint8)
    # Image windows 
    cv2.namedWindow( "_" )
    cv2.namedWindow( "_t" )
    cv2.createTrackbar( 'x', '_t', 1, 10, self.nothing )
    cv2.setMouseCallback( "_", self.click_and_crop )

  def nothing(self, *arg):
    print(self.ROI.shape)
    tp = cv2.getTrackbarPos('x', '_t') 
    if tp > 0:
      cv2.destroyWindow('__')
      cv2.imshow( "__", self.resize(self.ROI, tp) )
      cv2.waitKey( 1 )

  def click_and_crop(self, event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
      self.refPt = [ (x, y) ]
      self.cropping = True
   
    elif event == cv2.EVENT_LBUTTONUP:
      self.refPt.append( (x, y) )
      self.cropping = False
      self.update_roi = True
      self.update_zoom()

  def update_zoom(self):
    if self.update_roi == True:
      if ( (self.refPt[0][0] - self.refPt[1][0])**2  < 50) and ( (self.refPt[0][1] - self.refPt[1][1])**2 < 50 ):
        pass
      else:
        tp = cv2.getTrackbarPos('x', '_t')
        self.ROI = self.frame.copy()[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]
        cv2.rectangle( self.frame, self.refPt[0], self.refPt[1], (0, 255, 255), 2 )
        cv2.destroyWindow('__')
        cv2.waitKey(1)
        #print(ROI.shape)
        r_ = self.resize( self.ROI, tp )
        cv2.imshow( "_", self.frame )
        cv2.imshow( "__", r_ )
        #print(r_.shape)
        cv2.waitKey( 200 )
        self.update_roi = False
    
  def pyrup(self, f_):
    return cv2.pyrUp( f_, 2 )

  def resize(self, f_, tp):
    p_ = [cv2.INTER_NEAREST, cv2.INTER_LINEAR, cv2.INTER_AREA, cv2.INTER_CUBIC]
    row, col, d = f_.shape
    if (row < 10) and (col < 10):
      pass
    elif (row > 10) and (col > 10) and (row < 100) and (col < 100):
      return cv2.resize( f_, (f_.shape[1]*tp, f_.shape[0]*tp), p_[0] )
    else:
      return cv2.resize( f_, (f_.shape[1]*tp, f_.shape[0]*tp), p_[0] )

  def frames(self):
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