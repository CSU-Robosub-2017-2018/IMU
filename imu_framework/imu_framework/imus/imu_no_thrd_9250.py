#
#imu9250 spesific code using i2c on python
#
#uses base_imu

from imu_framework.imu_framework.imus.imu import imu
import smbus

class imu9250(imu):

    def __init__(self):
        imu.__init__(self)

        self.hasAccel = True
        self.hasGyro = True
        self.hasMagno = False
        self.bus = smbus.SMBus(1)  # i2c port 1
        self.link = 0x68



    #connect to above def
    bus = smbus.SMBus(1)  # i2c port 1
    link = 0x68

    def setData(self):
        self.XAaccelData = data_to_int(self.bus, self.link, 59, 60) / (16384)
        self.YAaccelData = data_to_int(self.bus, self.link, 61, 62) / (16384)
        self.ZAaccelData = data_to_int(self.bus, self.link, 63, 64) / (16384)

        self.XRotGyroData = (data_to_int(self.bus, self.link, 67, 68) / 131)*(3.14159265 /180)
        self.YRotGyroData = (data_to_int(self.bus, self.link, 69, 70) / 131)*(3.14159265 /180)
        self.ZRotGyroData = (data_to_int(self.bus, self.link, 71, 72) / 131)*(3.14159265 /180)


def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


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
