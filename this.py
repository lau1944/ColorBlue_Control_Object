import numpy as np
import cv2
import random
from collections import deque

pts = deque(maxlen=100)

# capture video source from webcam
cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

# load image from local file 
blue_img = cv2.imread('blue.png')
#resize image size
blue_img = cv2.resize(blue_img, (100, 100)) 

green_img = cv2.imread('green.png')
green_img = cv2.resize(green_img, (100, 100)) 

yellow_img = cv2.imread('yellow.png')
yellow_img = cv2.resize(yellow_img, (100, 100)) 

yBluelogo = 50
yGreenlogo = 50
yYellowlogo = 50
#3 colors in 3 position 
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

'''
def transparentOverlay(src , overlay , pos=(0,0),scale = 1):
    overlay = cv2.resize(overlay,(0,0),fx=scale,fy=scale)
    h,w,_ = overlay.shape  # Size of foreground
    rows,cols,_ = src.shape  # Size of background Image
    y,x = pos[0],pos[1]    # Position of foreground/overlay image
    
    #loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x+i >= rows or y+j >= cols:
                continue
            alpha = float(overlay[i][j][2]/255.0) # read the alpha channel 
            src[x+i][y+j] = alpha*overlay[i][j][:3]+(1-alpha)*src[x+i][y+j]
    return src
'''


#insert logo function, img1 = video frame , img2 = the image overlay the video frame
# x, y means the position of img2 will overlay




def InsertLogo_2(img1, img2, x, y):
	# Direct access pixels of images to put logo
	rows,cols,channels = img2.shape
	roi = img1[x:x+rows, y:y+cols ]

	# Now create a mask of logo and create its inverse mask also
	img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
	for i in range(rows):
		for j in range(cols):
			if mask[i][j] != 0 and i+x < 480 and j+y < 640:
				img1[i+x][j+y]=img2[i][j]
	return img1

while(True):

   
    # Capture frame-by-frame
    ret, frame = cap.read()
    #flip camera view with the right sight
    frame = cv2.flip(frame, 1)
    #rowsFrame, colsFrame, channelsFrame = frame.shape

    #blue rgb range
    lower_blue = np.array([70, 50, 50], dtype=np.uint8)
    upper_blue = np.array([130,255,255], dtype=np.uint8)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #create mask , Threshold the HSV image to get only blue colors 
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
  
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    mask = cv2.erode(mask, kernel, iterations = 2)
    mask = cv2.dilate(mask, kernel, iterations = 2)

    # apply a series of erosions and dilations to the mask
    # using an elliptical kernel

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    
    #find blue in webcam
    centerBlue = None
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
	    c = max(cnts, key=cv2.contourArea)
	    ((xBlue, yBlue), radius) = cv2.minEnclosingCircle(c)
	    M = cv2.moments(c)
	    xBlue=int(M["m10"] / M["m00"])
	    yBlue=int(M["m01"] / M["m00"])
	    centerBlue = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	    if radius > 10:
		    mode = False
		    cv2.circle(frame, centerBlue, 5, (0, 0, 255), -1)  
    



    # Bitwise-AND mask and original image
    # covert to binary frame
    # which blue becomes white, others will become black(null)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    #insert logo function with random position
    InsertLogo_2(frame,blue_img,yBluelogo,blue_dis)
    InsertLogo_2(frame,green_img,yGreenlogo,green_dis)
    InsertLogo_2(frame,yellow_img,yYellowlogo,yellow_dis)

    #controller !!
    if xBlue >= blue_dis and xBlue <= blue_dis + 100 :
        if yBlue >= yBluelogo and yBlue <= yBluelogo+100 :
            yBluelogo = yBlue
            # xBlue is the central of blue part
            # -50 in order to let image display on the red point
            blue_dis = xBlue-50
    if xBlue >= yellow_dis and xBlue <= yellow_dis + 100 :
        if yBlue >= yYellowlogo and yBlue <= yYellowlogo+100 :
            yYellowlogo = yBlue
            yellow_dis = xBlue-50
    if xBlue >= green_dis and xBlue <= green_dis + 100 :
        if yBlue >= yGreenlogo and yBlue <= yGreenlogo+100 :
            yGreenlogo = yBlue
            green_dis = xBlue-50       
            


    #create 3 rectangle box with 3 colors
    # yellow
    cv2.rectangle(frame, (50,350), (150, 450),(255,255,0), 3)
    # blue
    cv2.rectangle(frame, (200,350), (300, 450),(30,144,255), 3)
    # green
    cv2.rectangle(frame, (400,350), (500, 450),(124,252,0), 3)
    #cv2.rectangle(frame, (450,yellow_dis-100), (150, 150),color, 3)
    #cv2.rectangle(frame, (250,green_dis-100), (150, 150),color, 3)
    
    # Display the resulting frame
    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    # break when you win 
    if yBluelogo >= 350  and blue_dis >= 30 and blue_dis <= 170 :
        if yYellowlogo >= 350 and yellow_dis >= 180 and yellow_dis < 320 :
            if yGreenlogo >= 350 and green_dis >= 360 and green_dis < 550 :
                print('You Win!')
                break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()