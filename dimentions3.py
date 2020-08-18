#! /usr/bin/python3

import cv2
import numpy as np
import sys
import serial
from time import sleep

# const
thresh = 150 # default 180
maxValue =255
# var
actual_cnts = []
# functions

def min_rect(_cnt):
	rect = cv2.minAreaRect(_cnt)
	# print(rect)
	# print ("aspect ratio",rect[1][0]/rect[1][1])
	aspect_ratio = rect[1][0]/rect[1][1]
	box = cv2.boxPoints(rect)
	box = np.int0(box) 
	# print (box)
	area = cv2.contourArea(box)
	# cv2.drawContours(sample,[box],0,(255,0,0),2)
	# print("min rect area is {}".format(area),end = ' ')
	return area,box,aspect_ratio

def data_cnt(_cnt):
	area = cv2.contourArea(_cnt)
	# print ("Area of cnt {}".format(area))
	# cv2.drawContours(sample,_cnt,number , (0,255,0), 2)
	return area

def cylinder():
	ser.write(b'a')
	sleep(5)
	ser.write(b'a')
	

def lamp():
	ser.write(b'b')
	sleep(5)
	ser.write(b'b')
		
	

	

# main program
try:
	name = sys.argv[1]
except:
	print("no photo")

#serial init
ser = serial.Serial('/dev/ttyS0',9600)




sample = cv2.imread(name,1)
#print (sample)
sample_gray = cv2.cvtColor(sample,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(sample_gray,thresh,maxValue,cv2.THRESH_BINARY)
cv2.imshow("threshold",thresh)

# erosion
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(thresh,kernel,iterations = 1)

#find conture 
#ret,
cnts,hierarchy = cv2.findContours(erosion, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)	

for number,cnt in enumerate(cnts):
	if cv2.contourArea(cnt)>4500:
		actual_cnts.append(cnt)
		# cv2.drawContours(sample,cnts,number , (0,255,0), 1)


number_of_possable_ECU = 0

for number,cnt in enumerate(actual_cnts):
	
	rect_area,rect_box,aspect_ratio = min_rect(cnt)
	cnt_area = data_cnt(cnt)
	# print (rect_area - cnt_area)
	if (rect_area - cnt_area) < 3000 and  0.5<aspect_ratio <2.2:
		number_of_possable_ECU += 1
		# M = cv2.moments(cnt)
		# X = int(M["m10"] / M["m00"])
		# Y = int(M["m01"] / M["m00"])
		# cv2.drawContours(sample,[rect_box],0,(0,0,255 ),2)
		# cv2.putText(sample,"OK",(int(M['m10']/M['m00']),int(M['m01']/M['m00'])), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,0,0),2,cv2.LINE_AA)
if number_of_possable_ECU >0:

	print("found {} ECU ".format(number_of_possable_ECU),end='')
	lamp()
	print("on photo "+name)
else:
	print("no ecu ",end='')
	#cylinder() 
	print("on photo "+name)
	 
cv2.imshow(name,sample)


cv2.waitKey(10)
