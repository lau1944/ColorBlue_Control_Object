# ColorBlue_Control_Object
Using OpenCV2 detects blue color , control images position on screen (put the right color in the box !)

### A Game Using OpenCV2 To Control Images

After detect color blue, a red point will display on the center of the color blue

Move the red point to the images **slowly** and control the images !

Demo:
<p align="center">
  <img  src="https://github.com/lau1944/ColorBlue_Control_Object/blob/master/Untitled.png"  width="600"/>
</p>

<p align="center">
  <img  src="https://github.com/lau1944/ColorBlue_Control_Object/blob/master/Untitled1.png"  width="600"/>
</p>


### Code Explain 
- **Step 1** .Display Images and Rectangle box

```python
#generate random position for those three colors
blue_dis = random.randrange (50,450,200)
if blue_dis == 450:
    yellow_dis = random.randrange(50,250,200)
    if yellow_dis == 50:
        green_dis = 250
    if yellow_dis == 250:
        green_dis = 50   
elif blue_dis == 50:
    yellow_dis = random.randrange(250,450,200)
    if yellow_dis == 250:
        green_dis = 450
    if yellow_dis == 450:
        green_dis = 250   
elif blue_dis == 250:
    yellow_dis = random.randrange(50,450,400)
    if yellow_dis == 50:
        green_dis = 450
    if yellow_dis == 450:
        green_dis = 50   
```

```python
    #insert logo function with random position
    InsertLogo_2(frame,blue_img,yBluelogo,blue_dis)
    InsertLogo_2(frame,green_img,yGreenlogo,green_dis)
    InsertLogo_2(frame,yellow_img,yYellowlogo,yellow_dis)
    
    # yellow box
    cv2.rectangle(frame, (50,350), (150, 450),(255,255,0), 3)
    # blue box
    cv2.rectangle(frame, (200,350), (300, 450),(30,144,255), 3)
    # green box
    cv2.rectangle(frame, (400,350), (500, 450),(124,252,0), 3)
```


- **Step 2** .Detect Blue Color
```python
  #find blue in webcam
    centerBlue = None
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
	    c = max(cnts, key=cv2.contourArea)
	    ((xBlue, yBlue), radius) = cv2.minEnclosingCircle(c)
	    M = cv2.moments(c)
      # center blue location
	    xBlue=int(M["m10"] / M["m00"])
	    yBlue=int(M["m01"] / M["m00"])
	    centerBlue = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	    if radius > 10:
		    mode = False
		    cv2.circle(frame, centerBlue, 5, (0, 0, 255), -1)  
```

- **Step 3** .Control the images
```python
#controller !!
    if xBlue >= blue_dis and xBlue <= blue_dis + 100 :
        if yBlue >= yBluelogo and yBlue <= yBluelogo+100 :
            yBluelogo = yBlue
            # xBlue is the central of blue part
            # -50 in order to let imageX display on the red point
            blue_dis = xBlue-50
    if xBlue >= yellow_dis and xBlue <= yellow_dis + 100 :
        if yBlue >= yYellowlogo and yBlue <= yYellowlogo+100 :
            yYellowlogo = yBlue
            yellow_dis = xBlue-50
    if xBlue >= green_dis and xBlue <= green_dis + 100 :
        if yBlue >= yGreenlogo and yBlue <= yGreenlogo+100 :
            yGreenlogo = yBlue
            green_dis = xBlue-50       
```


## Thank You !
