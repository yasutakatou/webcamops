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
		frame = optimizeImage(img, x, y)
		cv2.imshow('filter', frame)
		cv2.imshow('my webcam', img)
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
		elif k==27:    # Esc key to stop
			cam.release()
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

	out = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	## FYI: https://qiita.com/ayuma/items/883901c68719abbc7a78
	# 一般的な二値化
	#threshold = 100
	#_, image_th = cv2.threshold(out, threshold, 255, cv2.THRESH_BINARY)

	# 大津の二値化
	_, image_th = cv2.threshold(out, 0, 255, cv2.THRESH_OTSU)

	# adaptive threshold
	#image_th = cv2.adaptiveThreshold(out, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 1)

	## FYI: https://qiita.com/ayuma/items/07ec25f1d50629fed698
	# medianフィルタ
	blur = cv2.medianBlur(image_th, 3)

	# bilateralフィルタ
	#blur = cv2.bilateralFilter(image_th, 9, 75, 75)

	return blur


if __name__ == '__main__':
    main()

