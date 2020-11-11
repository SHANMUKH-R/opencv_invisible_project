"""
@author: R.SHANMUKH
"""

import numpy as np 
import cv2
import time

capture = cv2.VideoCapture(0) 
time.sleep(2)

bg = 0 #bg is background

# We have captured the background here
for i in range(30):
    ret, bg = capture.read() 


while(capture.isOpened()):
    ret, image = capture.read()

    if not ret:
        break
    # Converting BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #HSB Hue Saturation and brightness
     
    
    # HSV values
    lower_red = np.array([161, 155, 84])
    upper_red = np.array([179, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red, upper_red)   #separating the cloak part

    lower_red = np.array([94, 80, 2])
    upper_red = np.array([126, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1 = mask1+mask2 #OR ! or x
    #Noise removal
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask2 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)

    mask2 = cv2.bitwise_not(mask1) #Except the cloak

    res1 = cv2.bitwise_and(bg, bg, mask=mask1) #used for segementation of colour
    res2 = cv2.bitwise_and(image, image, mask=mask2) #Used to substitute the cloak part
    final = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow('Success !!', final)
    s = cv2.waitKey(10)
    if s == 27:
        break

capture.releae()
cv2.destroyAllWindows()

    
