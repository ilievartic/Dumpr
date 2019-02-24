#!/usr/bin/python
import cv2
import time
import json
import subprocess
import serial
import requests
import datetime

url = "http://35.188.64.208:80/getfuel"
payload = "{\n\t\"space_id\": \"12345\",\n\t\"time\": \"%sZ\",\n\t\"plate_num\": \"%s\"\n}"
headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "4a793993-b0bf-4489-903b-9e422fea59d0"
    }

sendWifi = True

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

while True:
    start = time.time()
    for i in range(8):
        # empty the framebuffer
        ret, frame = cam.read()
    if ret:
        cv2.imwrite("/tmp/plate.jpg", frame)
        
        process = subprocess.Popen(['alpr', '-c', 'us', '-j', '/tmp/plate.jpg'], stdout=subprocess.PIPE)
        out, err = process.communicate()
        data = json.loads(out)
        stop =  time.time() - start
        if ( len(data["results"]) > 0 and data["results"][0]["confidence"] > 85.0 ):
            print "%s conf:%.2f cycletime:%.2f" % (data["results"][0]["plate"], data["results"][0]["confidence"], stop)
            out = "%s\n" % data["results"][0]["plate"]
            if( sendWifi ):
                dt = datetime.datetime.now()+datetime.timedelta(hours=5)
                response = requests.request("POST", url, data=(payload % (dt.isoformat(), data["results"][0]["plate"])), headers=headers, timeout=5)
            else:
                ser.write(out.encode())
        elif (not sendWifi):
            ser.write(" \n".encode())
    
    time.sleep(0.1)

cam.release()
