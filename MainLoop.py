__author__ = 'teddycool'
#State-switching and handling of general rendering
#from Inputs import Inputs
#from Board import Board
from Vision import Vision
import time
from Inputs import IoInputs
from Actuators import LedIndicator
#Global GPIO used by all...
import RPi.GPIO as GPIO
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
        #Move to statemachine...

        self._streamLed = LedIndicator.LedIndicator(GPIO, deviceconfig["IO"]["YellowLed"])

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
        self._streamSwitch.draw(frame,"StreamSwitch",10, 50)
        if self._stream:
            framerate = 1/(time.time()-self._lastframetime)
            self._lastframetime= time.time()
            self._vision.draw(frame, framerate) #Actually draw frame to mjpeg streamer...
            print "Main draw time: " + str(time.time()-start)


    def changeState(self, newstate):
        self._currentStateLoop = self._state[newstate]
        self._currentStateLoop.initialize()

    def __del__(self):
        self._onLed.activate(False)
        GPIO.cleanup()