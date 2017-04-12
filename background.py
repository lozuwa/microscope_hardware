import cv2
import numpy as np

array = np.zeros([720,1080], np.uint8)
array[:,:] = 255

while(True):
 cv2.imshow('Background', array)
 cv2.waitKey(0)
