# -*- coding: utf-8 -*
import cv2
import numpy as np
import cvui
import time
import sys
import pyautogui

actionValue = [100]
moveValue = [10]
clickValue = [15]

def main():
	args = sys.argv
	
	x = 500
	y = 500

	if len(sys.argv) == 3:
		if int(args[1]) > 100 and int(args[1]) < 1000:
			x = int(args[1])
		if int(args[2]) > 100 and int(args[2]) < 1000:
			y = int(args[2])

	print("X/Y: " + str(x) + "/" +  str(y))

	handMouse(x, y)

def drawGUI(width, x):
	frame[:] = (49, 52, 49)
	cvui.rect(frame,   2,   2, 320, 190, 0xffaa77, 0x4444aa)
	cvui.rect(frame,   2, 195, 320,  55, 0xffaa77, 0x4444aa)

	#########################################################

	cvui.text(frame, x, 5, 'clickValue (10 - 100)')
	cvui.trackbar(frame, x, 10, width, clickValue, 1, 100, 1, '%.0Lf')

	cvui.text(frame, x, 65, 'actionValue (10 - 100)')
	cvui.trackbar(frame, x, 75, width, actionValue, 1, 100, 1, '%.0Lf')

	cvui.text(frame, x, 130, 'moveValue (10 - 100)')
	cvui.trackbar(frame, x, 140, width, moveValue, 1, 100, 1, '%.0Lf')

	#########################################################

	cvui.text(frame, x + (80 * 1.25), 200, "role")

	if cvui.button(frame, x , 220, "Horizon"):
		return "Horizon"

	if cvui.button(frame, x + (80 * 1.25), 220, "Vertical"):
		return "Vertical"

	if cvui.button(frame, x + (80 * 2.5), 220, "[STOP]"):
		return "Stop"

	#########################################################

	cvui.update()
	cv2.imshow(WINDOW_NAME, frame)

	return ""


def handMouse(x, y):
	#Open Camera object
	cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

	#Decrease frame size
	cap.set(3, x)
	cap.set(4, y)

	#######################

	nowFar = (0, 0) # 現在の指先端座標
	preFar = (0, 0) # 前回の指先端座標

	#######################

	vFlag = False # 上下反転フラグ
	hFlag = False # 水平反転フラグ
	sFlag = False # 制御停止フラグ
	aFlag = '' # モーション記録フラグ
	cFlag = 0 # クリック検知フラグ

	#######################

	while(1):
		ret = drawGUI(300, 10)

		if ret == "Horizon":
			time.sleep(2)
			if hFlag == True:
				hFlag = False
			else:
				hFlag = True
		elif ret == "Vertical":
			time.sleep(2)
			if vFlag == True:
				vFlag = False
			else:
				vFlag = True
		elif ret == "Stop":
			time.sleep(2)
			if sFlag == True:
				sFlag = False
			else:
				sFlag = True

		#Measure execution time 
		start_time = time.time()
		
		#Capture frames from the camera
		ret, frame = cap.read()

		if vFlag == True:
			frame = cv2.flip(frame, 0)

		if hFlag == True:
			frame = cv2.flip(frame, 1)

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
		contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)   
		
		#Find Max contour area (Assume that hand is in the frame)
		max_area=100
		ci=0
		for i in range(len(contours)):
			cnt=contours[i]
			area = cv2.contourArea(cnt)
			if(area>max_area):
				max_area=area
				ci=i

		if len(contours) != 0:
			cnts = contours[ci]
			#Find convex hull
			hull = cv2.convexHull(cnts)
			#Find convex defects
			hull2 = cv2.convexHull(cnts,returnPoints = False)
			defects = cv2.convexityDefects(cnts,hull2)
			#Get defect points and draw them in the original image
			FarDefect = []
			maxFar = (0, 0)
			sndFar = (0, 0)
			if (hasattr(defects, 'shape') == True):
				for i in range(defects.shape[0]):
					s,e,f,d = defects[i,0]
					start = tuple(cnts[s][0])
					end = tuple(cnts[e][0])
					far = tuple(cnts[f][0])
					FarDefect.append(far)
					if maxFar[1] < far[1]:
						maxFar = far
					else:
						if sndFar[1] < far[1]:
							sndFar = far

			cv2.line(frame,sndFar,maxFar,[0,255,0],1)

			if cFlag == 0:
				if (sndFar[0] - maxFar[0]) > (clickValue[0] * 3):
					print('Stop')
					if sFlag == True:
						sFlag = False
					else:
						sFlag = True
				elif (sndFar[0] - maxFar[0]) > clickValue[0]:
					print('Click')
					cFlag = 50
					if sFlag == False:
						pyautogui.click()
			
			if (sndFar[0] - maxFar[0]) < (clickValue[0] / 2):
				if cFlag > 0:
					cFlag = cFlag - 1

			nowFar = maxFar

			if preFar[0] == 0 and preFar[1] == 0:
				preFar = maxFar
			else:
				if aFlag == '':
					if   (nowFar[0] - preFar[0])  > actionValue: # Right
						aFlag = 'Right'
					elif (preFar[0] - nowFar[0]) > actionValue: # Left
						aFlag = 'Left'
					elif (nowFar[1] - preFar[1]) > actionValue: # Up
						aFlag = 'Up'
					elif (preFar[1] - nowFar[1]) > actionValue: # Down
						aFlag = 'Down'
					#print(aFlag)
					if sFlag == False:
						print(' - - - - ')
						print(nowFar)
						print(preFar)
						print((nowFar[0] - preFar[0]) * moveValue[0])
						print((nowFar[1] - preFar[1]) * moveValue[0])
						print(' - - - - ')
						mousePosition = pyautogui.position()
						if mousePosition[0] - ((nowFar[0] - preFar[0]) * moveValue[0]) > 0 and mousePosition[1] - ((nowFar[1] - preFar[1]) * moveValue[0]) > 0:
							pyautogui.moveRel((nowFar[0] - preFar[0]) * moveValue[0], (nowFar[1] - preFar[1]) * moveValue[0])
				else:
					if aFlag == 'Right':
						if (nowFar[0] - preFar[0]) > 0:
							if sFlag == False:
								mousePosition = pyautogui.position()
								if mousePosition[0] - ((nowFar[0] - preFar[0]) * moveValue[0]) > 0 and mousePosition[1] - ((nowFar[1] - preFar[1]) * moveValue[0]) > 0:
									pyautogui.moveRel((nowFar[0] - preFar[0]) * moveValue[0], 0)
						else:
							aFlag = ''
					elif aFlag == 'Left':
						if (preFar[0] - nowFar[0]) > 0:
							if sFlag == False:
								mousePosition = pyautogui.position()
								if mousePosition[0] - ((nowFar[0] - preFar[0]) * moveValue[0]) > 0 and mousePosition[1] - ((nowFar[1] - preFar[1]) * moveValue[0]) > 0:
									pyautogui.moveRel((nowFar[0] - preFar[0]) * moveValue[0], 0)
						else:
							aFlag = ''
					elif aFlag == 'Up':
						if (nowFar[1] - preFar[1]) > 0:
							if sFlag == False:
								mousePosition = pyautogui.position()
								if mousePosition[0] - ((nowFar[0] - preFar[0]) * moveValue[0]) > 0 and mousePosition[1] - ((nowFar[1] - preFar[1]) * moveValue[0]) > 0:
									pyautogui.moveRel(0, (nowFar[1] - preFar[1]) * moveValue[0])
						else:
							aFlag = ''
					elif aFlag == 'Down':
						if (preFar[1] - nowFar[1]) > 0:
							if sFlag == False:
								mousePosition = pyautogui.position()
								if mousePosition[0] - ((nowFar[0] - preFar[0]) * moveValue[0]) > 0 and mousePosition[1] - ((nowFar[1] - preFar[1]) * moveValue[0]) > 0:
									pyautogui.moveRel(0, (nowFar[1] - preFar[1]) * moveValue[0])
						else:
							aFlag = ''

			preFar = nowFar

		##### Show final image ########
		cv2.imshow('camera',frame)
		###############################

		#close the output video by pressing 'ESC'
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			cap.release()
			cv2.destroyAllWindows()
			break


if __name__ == '__main__':
	WINDOW_NAME	= 'Trackbars'
	frame = np.zeros((260, 324, 3), np.uint8)
	cvui.init(WINDOW_NAME)

	main()

