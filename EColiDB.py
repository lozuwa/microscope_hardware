import sys, os 
import cv2
import numpy as np 

''' 
up: 2490368
right: 2555904
down: 2621440
left: 2424832
'''

refPt = []
cropping = False

def click_and_crop(event, x, y, flags, param):
	global refPt, cropping

	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True

	elif event == cv2.EVENT_LBUTTONUP:
		refPt.append((x, y))
		cropping = False
		cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
		cv2.imshow("image", image)
		cv2.waitKey(10)


def pick(f_):
	global image 
	image = f_
	clone = image.copy()
	cv2.namedWindow("image")
	cv2.setMouseCallback("image", click_and_crop)
	while True:
		cv2.imshow("image", image)
		key = cv2.waitKey(1) & 0xFF	 
		if len(refPt) == 2:
			roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
			cv2.imshow("ROI", roi)
			cv2.waitKey(0)
		if key == ord("c"):
			break
	 
	cv2.destroyAllWindows()

if __name__ == '__main__':
	dst = 'C:/Users/HP/Dropbox/CLICK_Medical/Databases'
	for folder in [each for each in os.listdir(dst+'/') if not (each.endswith('checkpoints') or each.endswith('.py'))]:
		print(dst+'/'+folder)
		for img in os.listdir(dst+'/'+folder+'/'):
			f_ = cv2.imread(dst+'/'+folder+'/'+img)
			print(f_.shape)
			pick( cv2.resize( f_, (1000, 800) ) )
