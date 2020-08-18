#! /usr/bin/python3
import serial
import time
from RPi import GPIO

reset = 3
button = 2
key = 0

def cylinder():
    ser.write(b'a')
    time.sleep(5)
    ser.write(b'a')

#init part
ser = serial.Serial('/dev/ttyS0')
GPIO.setmode(GPIO.BCM)
GPIO.setup(reset,GPIO.OUT)
GPIO.setup(button,GPIO.IN)
GPIO.output(reset,GPIO.HIGH)
while(True):
    if (GPIO.input(button)):
        cylinder()
        GPIO.output(reset,GPIO.LOW)
        time.sleep(1)

        GPIO.output(reset,GPIO.HIGH)
    #'key = input()
    if key == 'q':
        break
    #print('test')
    #print(GPIO.input(button))
ser.close()
