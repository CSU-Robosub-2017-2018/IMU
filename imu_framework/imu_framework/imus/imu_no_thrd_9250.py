''' imu_no_thrd_9250.py - Use this class to obtain data from the mpu 9250 imu. The data is obtained without using
threading.
'''

from imu_framework.imu_framework.imus.imu import imu
import smbus

class imu9250(imu):

    ##
    # @brief Obtains data from the mpu 9250 imu without threading
    # @param bus The bus number associated to the imu
    # @param link The link number associated to the imu
    def __init__(self):
        imu.__init__(self)

        self.hasAccel = True
        self.hasGyro = True
        self.hasMagno = False
        self.bus = smbus.SMBus(1)  # i2c port 1  FIX ME
        self.link = 0x68                # FIX ME

    ##
    # @brief This function updates the list of xyz acceleration, gyroscope, and magnetometer global variables
    def setData(self):
        self.XAaccelData = data_to_int(self.bus, self.link, 59, 60) / (16384)
        self.YAaccelData = data_to_int(self.bus, self.link, 61, 62) / (16384)
        self.ZAaccelData = data_to_int(self.bus, self.link, 63, 64) / (16384)

        self.XRotGyroData = (data_to_int(self.bus, self.link, 67, 68) / 131)*(3.14159265 /180)
        self.YRotGyroData = (data_to_int(self.bus, self.link, 69, 70) / 131)*(3.14159265 /180)
        self.ZRotGyroData = (data_to_int(self.bus, self.link, 71, 72) / 131)*(3.14159265 /180)


##
# @brief Converts twos complement binary number into a decimal number
# @param val Is the data obtained from the imu represented by a twos complement binary number
# @param bits The total number of bits used to describe the number
# @return val The decimal representation of the input number (val)
def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


##
# @brief This function connects the computer to the imu and gathers the information located in the desired registers
# @param bus The bus on which to connect to the imu
# @param link The hex value for the link to the imu (found using terminal and i2c tools)
# @param highreg The register number for the high value byte
# @param lowreg The register number for the low value byte
# @return The decimal value of the twos complement of the combined high and low bytes
def data_to_int(bus, link, highreg, lowreg):
    highdata = bus.read_byte_data(link, highreg)
    lowdata = bus.read_byte_data(link, lowreg)
    dblbyte = '{0:08b}'.format(highdata) + '{0:08b}'.format(lowdata)
    return twos_comp(int(dblbyte, 2), 16)
# Given register and bus constraints, outputs the correct +/- int corresponding to high and low register values
