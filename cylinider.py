#! /usr/bin/python3

import serial,sys


ser = serial.Serial('/dev/ttyS0')
do = sys.argv[1]  
if do == 'up':

	#print('you text up')
	ser.write(b'a')
if do == 'down':
	#print('you text down')	
	ser.write(b'b')
ser.close()
