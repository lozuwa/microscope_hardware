import numpy as np 
import cv2 
import time, os, sys 

def nothing():
 return 0

cv2.namedWindow('animation')
xsize = 300
ysize = 150
img = np.zeros([ysize, xsize], np.uint8)

xis = 1
yis = 1
xes = 299
yes = 149

xir = 100
yir = 20
xer = 120
yer = 40

while(True):
 img = np.zeros([ysize, xsize], np.uint8)
 # Slide animation 
 cv2.rectangle(img, (xis,yis), (xes,yes), (255,0,0), 4)
 cv2.line(img, (80, 1), (80, 149), (255,0,0), 3)
 # ROI animation 
 xir += 1 if xir < (xsize-50) else nothing()
 xer += 1 if xer < (xsize-30) else nothing()
 yir += 1 if yir < (ysize-40) else nothing()
 yer += 1 if yer < (ysize-20) else nothing()
 cv2.rectangle(img, (xir,yir), (xer,yer), (255,0,0), 2)
 # Show image
 cv2.imshow('animation', img)
 cv2.waitKey(10)
