# WebCamOps

![demo](https://github.com/yasutakatou/handmouse/blob/pic/webcamops.gif)

While watching something on PC while eating something, To display the next screen, you grab the mouse from spoon.
If you keep repeating, your wrist hurts more and more.
This solution is a shadow control for operating a PC. You forget to grab the mouse, while your eating.
More,This solution don't use Deep Leaning, very fast! (Even in my poor notebook, Comfortable do.)

![cam1](https://github.com/yasutakatou/handmouse/blob/pic/cam1.png)
Old laptop webcam is enough spec!

<HR>

First annotate your figure with a webcam.

```
python record.py
```

This code is recording your figure to picture file. Two arguments. The X and Y size of the camera. (default: x = 300, y = 300)
After running, The camera and the filtered video will be displayed at the same time.
You save data by press key .You can define up to 9 from 1-9.

Annotated dataset is ready.<br>
![annotation2](https://github.com/yasutakatou/handmouse/blob/pic/annotation3.png)<br>

Second, define the operation in the config file.<br>
It is in csv format. It is defined by **the image file name and operation**.

```
1,right
```

In this case, when it is similar to 1.png, move the mouse cursor to the right.<br>
Definition for mouse operation.

|Definition|operation|
|:---|:---|
|right|Move mouse cursor right|
|left|Move mouse cursor to left|
|up|Move mouse cursor up|
|down|Move mouse cursor down|
|click|Left click|
|rclick|right click|
|dclick|Left double click|

For key input, write the character you want to input or the definition.<br>
It will be pressed at the same time when separated by a space.

```
1,ctrl w
```

Type Ctrl + w if it looks like 1.png.<br>
Below are the definitions for the keyboard.

|Definition|operation|
|:---|:---|
|shift|holding the shift key|
|ctrl|holding the ctrl key|
|alt|holding the alt key|

For other keys, see below.It depends on pyautogui.
(KEYBOARD_KEYS)[https://pyautogui.readthedocs.io/en/latest/keyboard.html]

**none** is a definition that does nothing. This is useful if you are always in the picture.

```
1,none
```

Once the config is complete, run the operation code.

```
python webcamops.py Chrome
```

Three arguments. Window Title,The X and Y size of the camera.<br>

![bar](https://github.com/yasutakatou/handmouse/blob/pic/trackbar2.png)<br>

After launching, the Trackbars window will appear in addition to the camera image.

|item|effect|
|:---|:---|
|repeatValue|The number of repetitions. For fast PCs it can prevent frequent detections.|
|moveValue|The amount of mouse movement. The larger it moves, the more it moves at once|
|Horizon|Horizontal flip|
|Vetical|Vertical flip|
|Stop|Pause. Press again to resume|
|Exit|Stop the program|

Since it is a shadow drawing method, you can operate it with a shape other than your hand or body.

![pine](https://github.com/yasutakatou/handmouse/blob/pic/pine.png)
