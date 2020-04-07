# -*- coding: utf-8 -*
import cv2
import os
import numpy as np
import sys

# 顔を検出して黒で塗りつぶす場合はコメントインする
#face_cascade_path = 'haarcascade_frontalface_default.xml'
#face_cascade = cv2.CascadeClassifier(face_cascade_path)

datasetPATH = './datasets/'

def main():
	args = sys.argv
	
	x = 300
	y = 300

	if len(sys.argv) == 3:
		if int(args[1]) > 100 and int(args[1]) < 1000:
			x = int(args[1])
		if int(args[2]) > 100 and int(args[2]) < 1000:
			y = int(args[2])
	if os.path.isdir(datasetPATH) == False:
		os.mkdir(datasetPATH)

	i = 1
	print ("Default Save to ",i)
	cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
	#Decrease frame size
	cam.set(3, x)
	cam.set(4, y)

	while True:
		ret_val, img = cam.read()
		k = cv2.waitKey(1)
		cv2.imshow('my webcam', img)
		if np.all(img) == True:
			frame = optimizeImage(img, x, y)
			cv2.imshow('filter', frame)
			if k==48:
				i = 0
				print ("Changed to ",i)
			elif k==49:
				i = 1
				print ("Changed to ",i)
			elif k==50:
				i = 2
				print ("Changed to ",i)
			elif k==51:
				i = 3
				print ("Changed to ",i)
			elif k==52:
				i = 4
				print ("Changed to ",i)
			elif k==53:
				i = 5
				print ("Changed to ",i)
			elif k==54:
				i = 6
				print ("Changed to ",i)
			elif k==55:
				i = 7
				print ("Changed to ",i)
			elif k==56:
				i = 8
				print ("Changed to ",i)
			elif k==57:
				i = 9
				print ("Changed to ",i)
			elif k==32: 	#space
				cv2.imwrite(datasetPATH + str(i) + '.png', frame)
				print ("Saved ", str(i), ".png")
		if k==27:    # Esc key to stop
			cv2.destroyAllWindows()
			break


def optimizeImage(img, x , y):
	frame = cv2.resize(img, (x, y))

	# 顔を検出して黒で塗りつぶす場合はコメントインする
	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
	#if len(faces) != 1:
	#	return [[],[]]
	#for x, y, w, h in faces:
	#	pts = np.array( [ [x,y], [x,y+h], [x+w,y+h], [x+w,y] ] )
	#	frame = cv2.fillPoly(frame, pts =[pts], color=(0,0,0))

	#Blur the image
	blur = cv2.blur(frame,(3,3))
	 	
 	#Convert to HSV color space
	hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
		
	#Create a binary image with where white will be skin colors and rest is black
	mask2 = cv2.inRange(hsv,np.array([2,50,50]),np.array([15,255,255]))
		
	#Kernel matrices for morphological transformation	
	kernel_square = np.ones((11,11),np.uint8)
	kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
		
	#Perform morphological transformations to filter out the background noise
	#Dilation increase skin color area
	#Erosion increase skin color area
	dilation = cv2.dilate(mask2,kernel_ellipse,iterations = 1)
	erosion = cv2.erode(dilation,kernel_square,iterations = 1)	
	dilation2 = cv2.dilate(erosion,kernel_ellipse,iterations = 1)	
	filtered = cv2.medianBlur(dilation2,5)
	kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8,8))
	dilation2 = cv2.dilate(filtered,kernel_ellipse,iterations = 1)
	kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	dilation3 = cv2.dilate(filtered,kernel_ellipse,iterations = 1)
	median = cv2.medianBlur(dilation2,5)
	ret,thresh = cv2.threshold(median,127,255,0)
		
	#Find contours of the filtered frame
	#contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
	return thresh


if __name__ == '__main__':
    main()

