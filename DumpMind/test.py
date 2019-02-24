#!/usr/bin/python
import cv2
import time
import json
import subprocess
import serial

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

cam = cv2.VideoCapture(0)
cam.set(3,1920)
cam.set(4,1080)
#cam.set(5,10)

img_counter = 0

while True:
    start = time.time()
    ret, frame = cam.read()
    ret, frame = cam.read()
    ret, frame = cam.read()
    ret, frame = cam.read()
    ret, frame = cam.read()
    if ret:
        cv2.imwrite("/tmp/plate.jpg", frame)
        
        process = subprocess.Popen(['alpr', '-c', 'us', '-j', '/tmp/plate.jpg'], stdout=subprocess.PIPE)
        out, err = process.communicate()
        data = json.loads(out)
        if ( len(data["results"]) > 0 and data["results"][0]["confidence"] > 85.0 ):
            print(data["results"][0]["plate"]+"  "+str(data["results"][0]["confidence"]))
            ser.write("'"+data["results"][0]["plate"]+"'")
    stop =  time.time() - start
    time.sleep(0.1)

cam.release()
