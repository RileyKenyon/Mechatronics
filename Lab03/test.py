import cv2
import numpy as np
import RPi.GPIO as GPIO

# Config CV
lower_value = 35
upper_value = 65
WIN1 = "Camera"
WIN2 = "Mask"
WIN3 = "Output"
WIN4 = "Trackbar"
WIDTH = 150
HEIGHT = 100

# Config output pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.OUT)
GPIO.output(4,GPIO.HIGH);

def check(x):
    global upper_value, lower_value
    lower_value = cv2.getTrackbarPos('Lower',WIN4)
    upper_value = cv2.getTrackbarPos('Upper',WIN4)

cap = cv2.VideoCapture(0)
#cv2.namedWindow(WIN1)
#cv2.namedWindow(WIN2)
#cv2.namedWindow(WIN3)
#cv2.namedWindow(WIN4)
#cv2.createTrackbar('Lower',WIN4,0,255,check)
#cv2.createTrackbar('Upper',WIN4,0,255,check)

# Check for Green Value
green = np.uint8([[[0, 255, 0]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV);
print("Green in HSV: ",hsv_green)

while cap.isOpened() == True:
    # Aquire image
    ret, frame = cap.read()
    
    # Convert to hsv colorspace
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    # Create mask
    upper_lim = np.array([upper_value, 255, 255])
    lower_lim = np.array([lower_value, 125, 125])
    mask = cv2.inRange(hsv,lower_lim,upper_lim)
    
    # Overlay mask with image (bitwise AND)
    res = cv2.bitwise_and(frame,frame,mask=mask)
    
    if cv2.countNonZero(mask) > 50:
        #print("Green Light!")
    	GPIO.output(4,GPIO.LOW)
    else:
        GPIO.output(4,GPIO.HIGH)
#    cv2.imshow(WIN1,frame)
#    cv2.imshow(WIN2,mask)
#    cv2.imshow(WIN3,res)
#    cv2.resizeWindow(WIN1,WIDTH,HEIGHT)
#    cv2.resizeWindow(WIN2,WIDTH,HEIGHT)
#    cv2.resizeWindow(WIN3,WIDTH,HEIGHT)
    key = cv2.waitKey(30)
    if key <= -1:
        key = 0
    if chr(key) == 'q':
        print("Upper Limit:",upper_value)
        print("Lower Limit:",lower_value)
        break

cv2.destroyAllWindows()

