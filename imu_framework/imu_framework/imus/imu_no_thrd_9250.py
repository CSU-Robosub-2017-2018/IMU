#
#imu9250 spesific code using i2c on python
#
#uses base_imu

from base_imu import imu
import smbus
import struct
import time
import threading
import thread


def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

class imu9250(imu):



# Converts two bytes into a binary String format
    def tobinary(high, low):
        return '{0:08b}'.format(high) + '{0:08b}'.format(low)

# requires 16-bit String (1's and 0's)
    def binary_twos(word):
        wordint = int(word, 2)
        if word[0] == '0':
            return wordint
        else:
            return twos_comp(wordint, 16)

    # Given register and bus constraints, outputs the correct +/- int corresponding to high and low register values
    def data_to_int(bus, link, highreg, lowreg):
        highdata = bus.read_byte_data(link, highreg)
        lowdata = bus.read_byte_data(link, lowreg)
        dblbyte = '{0:08b}'.format(highdata) + '{0:08b}'.format(lowdata)
        return twos_comp(int(dblbyte, 2), 16)


    #connect to above def
    bus = smbus.SMBus(1)  # i2c port 1
    link = 0x68
    #initalice verialbes that will pass into base_imu
    ax = data_to_int(bus, link, 59, 60)
    ay = data_to_int(bus, link, 61, 62)
    az = data_to_int(bus, link, 63, 64)

    gx = data_to_int(bus, link, 67, 68)
    gy = data_to_int(bus, link, 69, 70)
    gz = data_to_int(bus, link, 71, 72)

    #pass veribls to base_imu
    def __init__(self, ax, ay, az, gx, gy, gz):
        imu.__init__(self, ax, ay, az, gx, gy, gz)

    '''
    def startPulling(self):
        if not self.pull_stop_event.is_set():
            thread.start_new_thread(self.pullImuData, (self.pull_stop_event,))

    def pullAllData(self):
        # raise Exception('testing')
        while not self.pull_stop_event.is_set():
            self.lock.acquire()
            self.XAaccelData = self.i2cGetInt(59, 60)
            self.YAaccelData = self.i2cGetInt(61, 62)
            self.ZAaccelData = self.i2cGetInt(63, 64)
            self.XRotGyroData = self.i2cGetInt(67, 68)
            self.XRotGyroData = self.i2cGetInt(69, 70)
            self.ZRotGyroData = self.i2cGetInt(71, 72)
            self.lock.release()
    '''