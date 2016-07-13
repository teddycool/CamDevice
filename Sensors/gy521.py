#!/usr/bin/python
#ACCELEROMETER
import smbus
import math
import time
import cv2


class GY521(object):

# Device interface
    def __init__(self, bus=1, adr=0x68):
        # Power management registers
        power_mgmt_1 = 0x6b
        power_mgmt_2 = 0x6c
        self._bus = smbus.SMBus(bus)  # or bus = smbus.SMBus(1) for Revision 2 boards
        self._address = 0x68  # This is the address value read via the i2cdetect command
        self._bus.write_byte_data(self._address, power_mgmt_1, 0)
        self._scalefactoraccel=16384.0


    def getAccelerometerdata(self, scaled=True):
        accel_xout = self._read_word_2c(0x3b)
        accel_yout = self._read_word_2c(0x3d)
        accel_zout = self._read_word_2c(0x3f)
        if scaled:
            return (
            accel_xout / self._scalefactoraccel, accel_yout / self._scalefactoraccel, accel_zout / self._scalefactoraccel)
        else:
            return (accel_xout, accel_yout, accel_zout)

    #What is rotation in this scenario?
    def getRotation(self,  degrees=True):
        x,y,z = self.getAccelerometerdata(False)
        xrotradians = math.atan2(y, self._dist(x,z))
        yrotradians = math.atan2(x, self._dist(y, z))
        #zrotradians = math.atan2(z, self._dist(z))
        if degrees:
            return (math.degrees(xrotradians),-math.degrees(yrotradians))
        else:
            return (xrotradians, yrotradians)

    def getDown(self):
        x,y,z = self.getAccelerometerdata()
        absacc = (math.abs(1-x),math.abs(1-y),math.abs(1-z))
        #TODO...

#Helpfunction, not supposed to be used directly
    def _read_byte(self,adr):
        return self._bus.read_byte_data(self._address, adr)

    def _read_word(self,adr):
        high = self._bus.read_byte_data(self._address, adr)
        low = self._bus.read_byte_data(self._address, adr+1)
        val = (high << 8) + low
        return val

    def _read_word_2c(self,adr):
        val = self._read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def _dist(self,a, b):
        return math.sqrt((a * a) + (b * b))



if __name__ == '__main__':
    gy=GY521()
    while 1:
        print "Accelerometer-data:"
        print gy.getAccelerometerdata(True)
        print gy.getAccelerometerdata(False)
        print "Rotation:"
        print gy.getRotation(True)
        print gy.getRotation(False)
        print "----------------------------------"
        time.sleep(1)