# WebCamOps

![demo](https://github.com/yasutakatou/webcamops/blob/pic/webcamops.gif)

## solution

While watching something on PC while eating something, To display the next screen, you grab the mouse from spoon.<br>
If you keep repeating, your wrist hurts more and more...<br>
<br>
This solution is a shadow control for operating a PC. You forget to grab the mouse, while your eating.<br>
More,This solution don't use Deep Leaning, very fast! (Even in my poor notebook, Comfortable do.)<br>

![cam1](https://github.com/yasutakatou/webcamops/blob/pic/cam1.png)
<br>Old laptop webcam is enough spec!

<HR>

## Preparation

**First** annotate your figure with a webcam.

```
python record.py
```

This code is recording your figure to picture file. Two arguments.<br>
The X and Y size of the camera. **(default: x = 300, y = 300)**<br>
After running, The camera and the filtered video will be displayed at the same time.<br>
You save data by press key. **You can define up to 9 from 1-9.**<br>

Annotated dataset is ready.<br>
![annotation2](https://github.com/yasutakatou/webcamops/blob/pic/annotation3.png)<br>

**Second**, define the operation in the config file.<br>
It is in csv format. It is defined by **the image file name and operation**.

```
1,right
```

In this case, when it is similar to 1.png, move the mouse cursor to the right.<br>
<br>
### Definition for mouse operation.

|Definition|operation|
|:---|:---|
|right|Move mouse cursor right|
|left|Move mouse cursor to left|
|up|Move mouse cursor up|
|down|Move mouse cursor down|
|click|Left click|
|rclick|right click|
|dclick|Left double click|

In case of key input, write the character or special definition.<br>
**When separated by a space, Its meaning pressed at the same time**.

```
1,ctrl w
```

In this case, type Ctrl + w if it looks like 1.png. <br>
<br>
### Definitions for the keyboard.

|Definition|operation|
|:---|:---|
|shift|holding the shift key|
|ctrl|holding the ctrl key|
|alt|holding the alt key|

For other keys, see below.It depends on pyautogui.[pyautogui document](https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys)

ex) 1,ctrl space<br>
Type Ctrl + Space if it looks like 1.png.<br>

**none** is a definition that does nothing. This is useful if something figure are always in the picture.

```
1,none
```

## Ops!

Write the config is complete, run for operation code.

```
python webcamops.py Chrome
```

Three arguments. Window Title,The X and Y size of the camera.<br>

Window title can search by a part of the character string.<br>
If you want to operate "Chrome", you set arg is "Chrome".<br>
You don't have to set full window title. "Google - Google Chrome"

![bar](https://github.com/yasutakatou/webcamops/blob/pic/taskbar2.png)<br>

After launching, the Trackbars window will appear in addition to the camera image.

|item|effect|
|:---|:---|
|repeatValue|The number of repetitions. For fast PCs it can prevent frequent detections.|
|moveValue|The amount of mouse movement. The larger values, the more it moves at once.|
|Horizon|Horizontal flip|
|Vetical|Vertical flip|
|Stop|Pause. Press again to resume|
|Exit|Stop the program|

Since it is a shadow matching method, you can operate it with a shape other than your hand or body.<br>

![pine](https://github.com/yasutakatou/webcamops/blob/pic/pine.png)

*Japanese lovly candy.*
