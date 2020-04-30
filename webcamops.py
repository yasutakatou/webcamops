# -*- coding: utf-8 -*
import cv2
import numpy as np
import cvui
import time
import sys
import pyautogui
import csv
import os
import win32gui
import ctypes
import winxpgui

moveValue = [10]
repeatValue = [1]
config = []
images = []
title = ''

datasetPATH = './datasets/'

def main():
	global title

	args = sys.argv
	
	x = 300
	y = 300

	if len(sys.argv) < 2:
		viewUsecase()

	hwnd = getWindowHWND(args[1])

	if hwnd == 0:
		print('target window not found: ', args[1])
		sys.exit()

	title = args[1]
	print('target window title: ', args[1])
	print('hwnd: ',str(hwnd))

	if len(sys.argv) == 4:
		if int(args[2]) > 100 and int(args[2]) < 1000:
			x = int(args[2])
		if int(args[3]) > 100 and int(args[3]) < 1000:
			y = int(args[3])

	print("X/Y: " + str(x) + "/" +  str(y))
	readCSV('config')
	readImages(datasetPATH)
	handMouse(x, y)


def getWindowHWND(title):
	titles = get_window_title()

	hwnd = 0
	for strs in titles:
		if strs.find(title) != -1 and strs.find('webcamops.py') == -1:
			hwnd = winxpgui.FindWindow(0, strs)
			return hwnd
	
	return hwnd


def viewUsecase():
	print("usecase: python webcamops.py arg1:(target window title) arg2:(1000 > x size > 100)  arg3:(1000 > y size > 100)")
	sys.exit()


def get_window_title():
	"""
	FYI: http://oregengo.hatenablog.com/entry/2016/10/08/171018

	ctypes.WINFUNCTYPE(戻り値の型, コールバック関数が想定する引数の型)
		: windowsのコールバック関数を定義 定義するだけなので引数は具体的なインスタンスではなく型を指定するのがミソ？
	↓
	user32.EnumWindows: トップレベルウィンドウのハンドルを順番にコールバック関数へ送る
	↓
	user32.IsWindowVisible(hwnd): 可視化されたウィンドウであればTrueを返す
	↓
	user32.GetWindowTextLengthW(hwnd):ウィンドウハンドルのテキスト長を返す
	↓
	ctypes.create_unicode_buffer(長さ): 変更可能な文字列？を作成 型は文字列配列になる 意味的には w_char*10と同じ，違いが良くわからん
	↓
	user32.GetWindowTextW(hwnd, 文字列格納用バッファ, 文字列長さ)

	ctypes.POINTER():引数型のポインタを作成
	ctypes.pointer():引数のポインタを返す
	"""
	# コールバック関数を定義(定義のみで実行ではない) コールバック関数はctypes.WINFUNCTYPEで作成可能
	EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
	# ??
	EnumWindows = ctypes.windll.user32.EnumWindows
	# タイトル格納用変数
	title = []

	def foreach_window(hwnd, lparam):
		if ctypes.windll.user32.IsWindowVisible(hwnd):
			length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
			buff = ctypes.create_unicode_buffer(length +1)
			ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
			title.append(buff.value)

			return True

	EnumWindows(EnumWindowsProc(foreach_window), 0)
	
	return title


def readImages(imagePath):
	if os.path.isdir(datasetPATH):
		files = os.listdir(imagePath)
		for i in files:
			print(datasetPATH + i)
			img = cv2.imread(datasetPATH + i)
			out = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			images.append(out)
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

	cvui.text(frame, x, 5, 'repeatValue (0 - 10)')
	cvui.trackbar(frame, x, 10, width, repeatValue, 0, 10, 1, '%.0Lf')

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

	repCount = repeatValue[0]
	repVal = 0

	vFlag = False
	hFlag = False
	sFlag = False

	#Decrease frame size
	cap.set(3, x)
	cap.set(4, y)

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

		frame = optimizeImage(frame, x, y)

		minVal = 0
		minCnt = 0
		i = 1
		for img in images:
			# FYI: https://qiita.com/t_okkan/items/e08116d989bd9e241052
			#		https://www.pynote.info/entry/opencv-template-matching
			#	類似度の計算方法memo
			# 	cv2.TM_SQDIFF,cv2.TM_SQDIFF_NORMED: 誤検知が多い
			# 	cv2.TM_CCORR,cv2.TM_CCORR_NORMED: 上手くいく。軽い
			#	cv2.TM_CCOEFF,cv2.TM_CCOEFF_NORMED: 上手くいく。CCORRと比べると重い？
			result = cv2.matchTemplate(frame, img, cv2.TM_CCOEFF)
			mVal, xVal, mLoc, xLoc = cv2.minMaxLoc(result)
			print(i, mVal, xVal, mLoc, xLoc)
			bufVal = mVal
			if bufVal > minVal or minVal == 0:
				minVal = bufVal
				minCnt = i
			i = i + 1

		print('detect: ' + str(minCnt) + ' score:' + str(minVal))

		if repVal != minCnt:
			repVal = minCnt
			repCount = repeatValue[0]
		else:
			repCount = repCount - 1
			if repCount < 0:
				for i in config:
					if str(minCnt) == i[0]:
						print("do: ",config[minCnt - 1])
						if sFlag == False:
							doAction(config[minCnt - 1][1])
				repVal = 0

		##### Show final image ########
		cv2.imshow('camera',frame)
		###############################

		#close the output video by pressing 'ESC'
		k = cv2.waitKey(1)
		if k == 27:
			cap.release()
			cv2.destroyAllWindows()
			break


def doAction(actions):
	global title

	if actions == 'none':
		return
	elif actions == 'right':
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
		nowHwnd = getWindowHWND(title)
		if nowHwnd == 0:
			return

		print(nowHwnd)

		win32gui.SetForegroundWindow(nowHwnd)
		keyDownFlag = ''
		act = actions.split(' ')
		for i in act:
			#print(i)
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
				pyautogui.press(i)
				if keyDownFlag != '':
					pyautogui.keyUp(keyDownFlag)
					keyDownFlag = ''


def mouseMoveDo(moveX, moveY):
	mousePosition = pyautogui.position()
	if moveX < 0:
		if mousePosition[0] + moveX * moveValue[0] < 0:
			return
	if moveY < 0:
		if mousePosition[1] + moveY * moveValue[0] < 0:
			return	
	pyautogui.moveRel(moveX * moveValue[0], moveY * moveValue[0])


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
	WINDOW_NAME	= 'Trackbars'
	frame = np.zeros((183, 360, 3), np.uint8)
	cvui.init(WINDOW_NAME)

	main()

