#! /usr/bin/python3
import serial
import time
from RPi import GPIO
import cv2
import os
  
reset = 3
button = 2
key = 0

def cylinder():
    ser.write(b'a')
    time.sleep(5)
    ser.write(b'a')

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)
  
#init part
ser = serial.Serial('/dev/ttyS0')
GPIO.setmode(GPIO.BCM)
GPIO.setup(reset,GPIO.OUT)
GPIO.setup(button,GPIO.IN)
GPIO.output(reset,GPIO.HIGH)

ser.write(b'a')

cam = cv2.VideoCapture(0)
winName = "Movement Indicator"
#cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)
# cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE )
# Read three images first:

t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

#serial init 
#ser = serial.Serial('/dev/ttyS0',9600)

while True:
  cv2.imshow( winName, diffImg(t_minus, t, t_plus) )
 
  # Read next image
  t_minus = t
  t = t_plus
  t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
  totalDiff = cv2.countNonZero(diffImg(t_minus, t, t_plus)) 
  # print(totalDiff)
  
  if totalDiff > 180000:
    print("movement")
    cam.release()
    # cv2.waitKey(5000)
    time.sleep(5)
    # im =cam.read()[1]
    
    cam = cv2.VideoCapture(0)
    # im = cam.read()[1]
    # cv2.imshow("photo",im)
    im =cam.read()[1]
    t = time.asctime()
    ta =  t.split(" ")[-2].split(":") 
    ba =  ta[0]+"-"+ta[1]+"-"+ta[2] +".png"



    cv2.imwrite(ba,im)
    

    os.system("python3 dimentions3.py {}".format(ba))
    # totalDiff = 0
    # print(totalDiff)
    # t = 0
    # t_plus = 0
    # t_minus=0

    #cylinder()
  
    t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
  
	#add conveyor
  if (GPIO.input(button)):
	  cylinder()
	  GPIO.output(reset,GPIO.LOW)
	  time.sleep(1)
	  GPIO.output(reset,GPIO.HIGH)
  
  
  key = cv2.waitKey(10)
  if key == 27:
    cv2.destroyWindow(winName)
    break
 
print("Goodbye")
ser.close()
