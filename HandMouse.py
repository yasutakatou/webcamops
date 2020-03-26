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
	
	x = 250
	y = 250

	if len(sys.argv) == 3:
		if int(args[1]) > 100 and int(args[1]) < 1000:
			x = int(args[1])
		if int(args[2]) > 100 and int(args[2]) < 1000:
			y = int(args[2])

	print("X/Y: " + str(x) + "/" +  str(y))

	handMouse(x, y)

def drawGUI(width, x):
	frame[:] = (49, 52, 49)
	cvui.rect(frame,   2,   2, 445, 190, 0xffaa77, 0x4444aa)
	cvui.rect(frame,   2, 195, 445,  55, 0xffaa77, 0x4444aa)
	cvui.rect(frame,   2, 252, 445,  55, 0xffaa77, 0x4444aa)

	#########################################################

	cvui.text(frame, x, 5, 'clickValue (10 - 100)')
	cvui.trackbar(frame, x, 10, width, clickValue, 1, 100, 1, '%.0Lf')

	cvui.text(frame, x, 65, 'actionValue (10 - 100)')
	cvui.trackbar(frame, x, 75, width, actionValue, 1, 100, 1, '%.0Lf')

	cvui.text(frame, x, 130, 'moveValue (10 - 100)')
	cvui.trackbar(frame, x, 140, width, moveValue, 1, 100, 1, '%.0Lf')

	#########################################################

	cvui.text(frame, x + (80 * 1.25), 200, "role")

	if cvui.button(frame, x , 218, "Horizon"):
		return "Horizon"

	if cvui.button(frame, x + (80 * 1.25), 218, "Vertical"):
		return "Vertical"

	if cvui.button(frame, x + (80 * 2.5), 218, "Stop"):
		return "Stop"

	if cvui.button(frame, x + (80 * 3.5), 218, "Exit"):
		exit()

	#########################################################

	cvui.text(frame, x + (80 * 1.25), 255, "finger position")

	if cvui.button(frame, x , 275, "Upper edge"):
		return "Upper"

	if cvui.button(frame, x + (80 * 1.45), 275, "Under edge"):
		return "Under"

	if cvui.button(frame, x + (80 * 2.95), 275, "Left edge"):
		return "Left"

	if cvui.button(frame, x + (80 * 4.20), 275, "Right edge"):
		return "Right"

	#cvui.update()
	cv2.imshow(WINDOW_NAME, frame)

	return ""


def handMouse(x, y):
	#Open Camera object
	cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

	#Decrease frame size
	cap.set(3, x)
	cap.set(4, y)

	#######################

	nowPos = (0, 0) # 現在の指先端座標
	prePos = (0, 0) # 前回の指先端座標

	#######################

	vFlag = False # 上下反転フラグ
	hFlag = False # 水平反転フラグ
	sFlag = True # 制御停止フラグ
	aFlag = '' # モーション記録フラグ
	cFlag = 0 # クリック検知フラグ
	eFlag = 'Upper' # 指検知方向フラグ

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
		else:
			if len(ret) > 0:
				time.sleep(2)
				print(eFlag)
				eFlag = ret

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

			fstPos = (0, 0)
			sndPos = (0, 0)
			if (hasattr(defects, 'shape') == True):
				for i in range(defects.shape[0]):
					s,e,f,d = defects[i,0]
					Pos = tuple(cnts[f][0])
					if eFlag == 'Upper':
						if fstPos[1] < Pos[1]:
							fstPos = Pos
						else:
							if sndPos[1] < Pos[1]:
								sndPos = Pos
					if eFlag == 'Under':
						if fstPos[1] > Pos[1]:
							fstPos = Pos
						else:
							if sndPos[1] > Pos[1]:
								sndPos = Pos
					if eFlag == 'Right':
						if fstPos[0] < Pos[0]:
							fstPos = Pos
						else:
							if sndPos[0] < Pos[0]:
								sndPos = Pos
					if eFlag == 'Left':
						if fstPos[0] > Pos[0]:
							fstPos = Pos
						else:
							if sndPos[0] > Pos[0]:
								sndPos = Pos

			cv2.circle(frame,fstPos,10,[100,255,255],3)
			cv2.circle(frame,sndPos,10,[100,255,255],3)
			cv2.line(frame,sndPos,fstPos,[0,255,0],1)

			if cFlag == 0:
				if (sndPos[0] - fstPos[0]) > (clickValue[0] * 3):
					print('Stop')
					if sFlag == True:
						sFlag = False
					else:
						sFlag = True
				elif (sndPos[0] - fstPos[0]) > clickValue[0]:
					print('Click')
					cFlag = 50
					if sFlag == False:
						pyautogui.click()
			
			if (sndPos[0] - fstPos[0]) < (clickValue[0] / 2):
				if cFlag > 0:
					cFlag = cFlag - 1

			nowPos = fstPos

			if prePos[0] == 0 and prePos[1] == 0:
				prePos = fstPos
			else:
				if aFlag == '':
					if   (nowPos[0] - prePos[0])  > actionValue: # Right
						aFlag = 'Right'
					elif (prePos[0] - nowPos[0]) > actionValue: # Left
						aFlag = 'Left'
					elif (nowPos[1] - prePos[1]) > actionValue: # Up
						aFlag = 'Up'
					elif (prePos[1] - nowPos[1]) > actionValue: # Down
						aFlag = 'Down'
					#print(aFlag)
					if sFlag == False:
						print(' - - - - ')
						print(nowPos)
						print(prePos)
						print((nowPos[0] - prePos[0]) * moveValue[0])
						print((nowPos[1] - prePos[1]) * moveValue[0])
						print(' - - - - ')
						mousePosition = pyautogui.position()
						print(mousePosition)
						print(' - - - - ')
				else:
					aFlag = mouseMove(aFlag, sFlag, nowPos, prePos)

			prePos = nowPos

		##### Show final image ########
		cv2.imshow('camera',frame)
		###############################

		#close the output video by pressing 'ESC'
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			cap.release()
			cv2.destroyAllWindows()
			break

def mouseMove(aFlag, sFlag, nowPos, prePos):
	if aFlag == 'Right':
		if (nowPos[0] - prePos[0]) > 0:
			if sFlag == False:
				mouseMoveDo(nowPos[0] - prePos[0], nowPos[1] - prePos[1], nowPos[0] - prePos[0] , 0)
			else:
				return ''
	elif aFlag == 'Left':
		if (prePos[0] - nowPos[0]) > 0:
			if sFlag == False:
				mouseMoveDo(nowPos[0] - prePos[0], nowPos[1] - prePos[1], prePos[0] - nowPos[0] , 0)
			else:
				return ''
	elif aFlag == 'Up':
		if (nowPos[1] - prePos[1]) > 0:
			if sFlag == False:
				mouseMoveDo(nowPos[0] - prePos[0], nowPos[1] - prePos[1], 0, nowPos[1] - prePos[1])
			else:
				return ''
	elif aFlag == 'Down':
		if (prePos[1] - nowPos[1]) > 0:
			if sFlag == False:
				mouseMoveDo(nowPos[0] - prePos[0], nowPos[1] - prePos[1], 0, prePos[1] - nowPos[1])
			else:
				return ''
	return aFlag


def mouseMoveDo(moveX, moveY, valX, valY):
	mousePosition = pyautogui.position()
	if moveX < 0:
		if mousePosition[0] + moveX * moveValue[0] < 0:
			return
	if moveY < 0:
		if mousePosition[1] + moveY * moveValue[0] < 0:
			return
	pyautogui.moveRel(valX * moveValue[0], valY * moveValue[0])


if __name__ == '__main__':
	WINDOW_NAME	= 'Trackbars'
	frame = np.zeros((310, 450, 3), np.uint8)
	cvui.init(WINDOW_NAME)

	main()

