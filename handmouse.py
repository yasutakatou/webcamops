# -*- coding: utf-8 -*
import cv2
import numpy as np
import cvui
import time
import sys
import pyautogui
import csv
import os

moveValue = [10]
actionValue = [55]
repeatValue = 3
config = []
images = []

datasetPATH = './datasets/'

bf = cv2.BFMatcher(cv2.NORM_HAMMING)
# 特徴点算出のアルゴリズムを決定(コメントアウトで調整して切り替え)
detector = cv2.ORB_create()
#detector = cv2.AKAZE_create()

def main():
	args = sys.argv
	
	x = 300
	y = 300

	if len(sys.argv) == 3:
		if int(args[1]) > 100 and int(args[1]) < 1000:
			x = int(args[1])
		if int(args[2]) > 100 and int(args[2]) < 1000:
			y = int(args[2])

	print("X/Y: " + str(x) + "/" +  str(y))
	readCSV('config')
	readImages(datasetPATH)
	handMouse(x, y)


def readImages(imagePath):
	if os.path.isdir(datasetPATH):
		files = os.listdir(imagePath)
		for i in files:
			print(datasetPATH + i)
			img = cv2.imread(datasetPATH + i)
			images.append(img)
	print('images: ' + str(len(images)))


def readCSV(filename):
	with open(filename) as f:
		reader = csv.reader(f)
		for row in reader:
			config.append(row)


def drawGUI(width, x):
	global actionValue
	global moveValue

	frame[:] = (49, 52, 49)
	cvui.rect(frame,   2,   2, 355, 120, 0xffaa77, 0x4444aa)
	cvui.rect(frame,   2, 125, 355,  55, 0xffaa77, 0x4444aa)

	#########################################################

	cvui.text(frame, x, 5, 'actionValue (10 - 100)')
	cvui.trackbar(frame, x, 10, width, actionValue, 1, 100, 1, '%.0Lf')

	cvui.text(frame, x, 65, 'moveValue (10 - 100)')
	cvui.trackbar(frame, x, 75, width, moveValue, 1, 100, 1, '%.0Lf')

	#########################################################

	cvui.text(frame, x + (80 * 1.25), 130, "role")

	if cvui.button(frame, x , 145, "Horizon"):
		return "Horizon"

	if cvui.button(frame, x + (80 * 1.25), 145, "Vertical"):
		return "Vertical"

	if cvui.button(frame, x + (80 * 2.5), 145, "Stop"):
		return "Stop"

	if cvui.button(frame, x + (80 * 3.5), 145, "Exit"):
		exit()

	#cvui.update()
	cv2.imshow(WINDOW_NAME, frame)

	return ""


def handMouse(x, y):
	#Open Camera object
	cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

	vFlag = False
	hFlag = False
	sFlag = False

	#Decrease frame size
	cap.set(3, x)
	cap.set(4, y)

	bf = cv2.BFMatcher(cv2.NORM_HAMMING)
	# 特徴点算出のアルゴリズムを決定(コメントアウトで調整して切り替え)
	detector = cv2.ORB_create()
	# detector = cv2.AKAZE_create()

	while(1):
		ret = drawGUI(300, 10)

		if ret == "Horizon":
			print("Horizon reverse")
			time.sleep(2)
			if hFlag == True:
				hFlag = False
			else:
				hFlag = True
		elif ret == "Vertical":
			print("Vertical reverse")
			time.sleep(2)
			if vFlag == True:
				vFlag = False
			else:
				vFlag = True
		elif ret == "Stop":
			time.sleep(2)
			if sFlag == True:
				print("Resume")
				sFlag = False
			else:
				print("Stop")
				sFlag = True

		#Capture frames from the camera
		ret, frame = cap.read()

		if vFlag == True:
			frame = cv2.flip(frame, 0)

		if hFlag == True:
			frame = cv2.flip(frame, 1)

		frame = optimizeImage(frame)
		(target_kp, target_des) = calc_kp_and_des(frame)

		minVal = 1000
		minCnt = 0
		if np.all(target_des) == False:
			i = 1
			for img in images:
				bufVal = calcImage(img, target_kp, target_des)
				if bufVal < minVal:
					minVal = bufVal
					minCnt = i
				i = i + 1

		if minCnt != 0 and minVal < actionValue[0]:
			print('detect: ' + str(minCnt) + ' score:' + str(minVal))
			for i in config:
				if str(minCnt) == i[0]:
					print(config[minCnt - 1])
					if sFlag == False:
						doAction(config[minCnt - 1][1])

		##### Show final image ########
		cv2.imshow('camera',frame)
		###############################

		#close the output video by pressing 'ESC'
		k = cv2.waitKey(1)
		if k == 27:
			cap.release()
			cv2.destroyAllWindows()
			break


def calcImage(image, target_kp, target_des):
	try:
		(comparing_kp, comparing_des) = calc_kp_and_des(image)
		#画像同士をマッチング
		matches = bf.match(target_des, comparing_des)
		dist = [m.distance for m in matches]
		#類似度を計算する
		ret = sum(dist) / len(dist)
	except cv2.error:
		ret = 100000
	return ret


def doAction(actions):
	if actions == 'right':
		mouseMoveDo( 1,  0)
	elif actions == 'left':
		mouseMoveDo(-1,  0)
	elif actions == 'up':
		mouseMoveDo( 0 ,-1)
	elif actions == 'down':
		mouseMoveDo( 0 , 1)
	elif actions == 'click':
		pyautogui.click()
	elif actions == 'rclick':
		pyautogui.rightClick()
	elif actions == 'dclick':
		pyautogui.doubleClick() 
	else:
		keyDownFlag = ''
		for i in actions:
			print(i)
			if i == 'shift':
				pyautogui.keyDown('shift')
				keyDownFlag = i
			elif i == 'ctrl':
				pyautogui.keyDown('ctrl')
				keyDownFlag = i
			elif i == 'alt':
				pyautogui.keyDown('alt')
				keyDownFlag = i
			elif i == 'enter':
				pyautogui.press('enter')
			elif i == 'space':
				pyautogui.press('space')
			else:
				if keyDownFlag != '':
					pyautogui.keyUp(keyDownFlag)
					keyDownFlag = ''
				pyautogui.press(i)


def mouseMoveDo(moveX, moveY):
	mousePosition = pyautogui.position()
	if moveX < 0:
		if mousePosition[0] + moveX * moveValue[0] < 0:
			return
	if moveY < 0:
		if mousePosition[1] + moveY * moveValue[0] < 0:
			return	
	pyautogui.moveRel(moveX * moveValue[0], moveY * moveValue[0])


def optimizeImage(frame):

	# 顔を検知して黒で塗りつぶしたい場合
	# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
	# if len(faces) != 1:
	#	return [[],[]]
	# for x, y, w, h in faces:
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


def calc_kp_and_des(img):
	return detector.detectAndCompute(img, None)


if __name__ == '__main__':
	WINDOW_NAME	= 'Trackbars'
	frame = np.zeros((183, 360, 3), np.uint8)
	cvui.init(WINDOW_NAME)

	main()


