#!/usr/bin/python
#COMPASS

import smbus
import time
import math
import cv2



class GY273(object):

    def __init__(self, bus=1, adr= 0x1e):
        self._bus = smbus.SMBus(bus)
        self._address = adr
        self._scale = 0.92
        self._write_byte(0, 0b01110000)  # Set to 8 samples @ 15Hz
        self._write_byte(1, 0b00100000)  # 1.3 gain LSb / Gauss 1090 (default)
        self._write_byte(2, 0b00000000)  # Continuous sampling

    #Device interface
    def getXYZ(self):
        # Y,Y,Z as on sensor, must be mapped to placing of sensor. Use accelerometer-data to figure out what is 'down'...
        x = round(self._read_word_2c(3) * self._scale, 2)
        y = round(self._read_word_2c(7) * self._scale, 2)
        z = round(self._read_word_2c(5) * self._scale, 2)
        return (x, y, z)

    def getBearing(self):
        x_out = self._read_word_2c(3) * self._scale
        y_out = self._read_word_2c(7) * self._scale
        z_out = self._read_word_2c(5) * self._scale

        bearing = math.atan2(y_out, x_out)
        if (bearing < 0):
            bearing += 2 * math.pi
        return round(bearing,2)

    #Help functions
    def _read_byte(self, adr):
        return self._bus.read_byte_data(self._address, adr)

    def _read_word(self, adr):
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

    def _write_byte(self, adr, value):
        self._bus.write_byte_data(self._address, adr, value)






if __name__ == '__main__':
    gy=GY273()
    while 1:
        print "X, Y, Z: " + str(gy.getXYZ())
        print "Bearing"  + str(gy.getBearing())
        print "----------------------------------"
        time.sleep(0.5)