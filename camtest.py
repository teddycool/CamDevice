from Vision import Vision
from CamDeviceConfig import deviceconfig
from Sensors import gy521
import time

vision = Vision.Vision()
accel = gy521.GY521()
print "Vision init"
frame = vision.initialize()
print  "First vision update"


lastframetime = time.time()
try:
    while 1:
        framerate = 1 / (time.time() - lastframetime)
        lastframetime = time.time()
        frame = vision.update()
        accel = accel.getAccelerometerdata()
        text = str(accel)
        if accel[0]>0.8 and accel[0]<1.2:
            vision._cam.hflip = True
        else:
            vision._cam.hflip = False
        if accel[1] > 0.8 and accel[1] < 1.2:
            vision._cam.vflip = True
        else:
            vision._cam.vflip = False
        vision.draw(frame, framerate,text)
        print text
        time.sleep(0.2)
except:
    vision.__del__()
