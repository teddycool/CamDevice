__author__ = 'teddycool'

from Vision import Vision
import time
from Inputs import IoInputs
from Actuators import LedIndicator
#Global GPIO used by all...
import RPi.GPIO as GPIO
import os
from CamDeviceConfig import deviceconfig
from Sensors import gy521, gy273


class MainLoop(object):
    def __init__(self):
        #TODO: fix logging to file readable from web
        self._vision= Vision.Vision()
        GPIO.setmode(GPIO.BCM)
        self._accel = gy521.GY521()
        self._comp = gy273.GY273()
        self._calButton = IoInputs.PushButton(GPIO, deviceconfig["IO"]["GreenButton"])
        self._resetButton = IoInputs.PushButton(GPIO, deviceconfig["IO"]["RedButton"])
        self._streamSwitch = IoInputs.OnOnSwitch(GPIO, deviceconfig["IO"]["Switch1.1"], deviceconfig["IO"]["Switch1.2"])

        self._onLed =  LedIndicator.LedIndicator(GPIO, deviceconfig["IO"]["GreenLed"])
        self._streamLed = LedIndicator.LedIndicator(GPIO, deviceconfig["IO"]["YellowLed"])
        self._resetLed = LedIndicator.LedIndicator(GPIO, deviceconfig["IO"]["RedLed"])

    def initialize(self):
        print "Main init..."
        #self._inputs.initialize()
        self.time=time.time()
        self._stream = True
        frame = self._vision.initialize()
        self._lastframetime = time.time()
        self._calButton.initialize()
        self._resetButton.initialize()
        self._streamSwitch.initialize()
        self._onLed.activate()
        self._streamLed.activate(True)
        print "CamDevice started at ", self.time
        return frame

    def update(self):
        start = time.time()
        print "Main update time: " + str(time.time() - start)
        frame = self._vision.update()

        if self._streamSwitch.update() == 'ON1':
            self._stream = True
            self._streamLed.activate(True)
        else:
            self._stream = False
            self._streamLed.activate(False)

        reset = self._resetButton.update()
        if reset == "Pressed":
            self._resetLed.activate(True)
        if reset == "LongPressed":
            self._resetLed.activate(False)
            self._streamLed.activate(False)
            self._onLed.activate(False)
            print "Rebooting..."
            os.system('sudo reboot')
        if reset == "Released":
            self._resetLed.activate(False)

        calibrate = self._calButton.update()

        print "Accelerometer data: " + str(self._accel.getAccelerometerdata(True))
        print "Compass data:" + str(self._comp.getXYZ())

        #Rotate camera stream with accelerometer data
        if (self._accel.getAccelerometerdata(True)[0] > 0.8 and  self._accel.getAccelerometerdata(True)[0] < 1.2):
            self._vision.setRotation(0)
        if (self._accel.getAccelerometerdata(True)[0] > -1.2 and  self._accel.getAccelerometerdata(True)[0] < -0.8):
            self._vision.setRotation(180)
        if (self._accel.getAccelerometerdata(True)[1] > 0.8 and self._accel.getAccelerometerdata(True)[1] < 1.2):
            self._vision.setRotation(90)
        if (self._accel.getAccelerometerdata(True)[1] > -1.2 and self._accel.getAccelerometerdata(True)[1] < -0.8):
            self._vision.setRotation(270)
        return frame

    def draw(self, frame):
        start = time.time()
        #frame = self._currentStateLoop.draw(frame)
        self._streamSwitch.draw(frame,"StreamSwitch",10, 20)
        self._resetButton.draw(frame,"ResetButton",10, 40)
        self._calButton.draw(frame, "CalButton", 10, 60)
        if self._stream:
            framerate = 1/(time.time()-self._lastframetime)
            self._lastframetime= time.time()
            self._vision.draw(frame, framerate) #Actually draw frame to mjpeg streamer...
            print "Main draw time: " + str(time.time()-start)

    def __del__(self):
        self._onLed.activate(False)
        GPIO.cleanup()