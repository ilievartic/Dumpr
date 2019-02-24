import cv2
import time
import json
import subprocess

cam = cv2.VideoCapture(1)
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
    stop =  time.time() - start
    time.sleep(0.1)

cam.release()
