__author__ = 'teddycool'

# Put up the camera, run calibrate
# Start to play...


import MainLoop
import time
from CamDeviceConfig import deviceconfig


class Main(object):

    def __init__(self):
        print "Init Main object for CamDevice..."
        self._mainLoop=MainLoop.MainLoop()


    def run(self):
        self._mainLoop.initialize()
        stopped = False
        while not stopped:
            framestarttime = time.time()
            frame = self._mainLoop.update()
            self._mainLoop.draw(frame)
            #time.sleep(0.01)


#Testcode to run module. Standard Python way of testing modules.
#OBS !! comment out   line 47: "C:\Python27\Lib\site-packages\pygame\_camera_vidcapture.py":
#       #self.dev.setresolution(width, height) on row 49 in:
#
if __name__ == "__main__":
    cd=Main()
    cd.run()
