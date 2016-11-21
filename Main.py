__author__ = 'teddycool'

import MainLoop
import time


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
            time.sleep(0.05)


#Testcode to run module. Standard Python way of testing modules.

if __name__ == "__main__":
    cd=Main()
    cd.run()
