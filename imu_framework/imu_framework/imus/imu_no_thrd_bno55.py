''' imu_no_thrd_bno55.py - Use this class to obtain data from the bn055 imu. The data is obtained without using
threading. This class is not currently functioning on the raspbery pi as it will need to be
reconfigure to connect properly to the bno55 imu. The method for connecting the imu may change
but the file should remain essentially the same.
'''

from imu_framework.imu_framework.imus.imu import imu
import smbus

class imu_no_thrd_bno55(imu):

    ##
    # @brief Obtains data from the bno55 imu without threading
    # @param filePath The absolute file path to the csv file
    # @param bus The bus number associated to the imu
    # @param link The link number associated to the imu
    def __init__(self):
        imu.__init__(self)

        self.hasAccel = True
        self.hasGyro = True
        self.hasMagno = False
        self.bus = smbus.SMBus(1)  # i2c port 1
        self.link = 0x68

        # Accel data register
        self.BNO055_ACCEL_DATA_X_LSB_ADDR = 0X08
        self.BNO055_ACCEL_DATA_X_MSB_ADDR = 0X09
        self.BNO055_ACCEL_DATA_Y_LSB_ADDR = 0X0A
        self.BNO055_ACCEL_DATA_Y_MSB_ADDR = 0X0B
        self.BNO055_ACCEL_DATA_Z_LSB_ADDR = 0X0C
        self.BNO055_ACCEL_DATA_Z_MSB_ADDR = 0X0D
        
        # Mag data register
        self.BNO055_MAG_DATA_X_LSB_ADDR = 0X0E
        self.BNO055_MAG_DATA_X_MSB_ADDR = 0X0F
        self.BNO055_MAG_DATA_Y_LSB_ADDR = 0X10
        self.BNO055_MAG_DATA_Y_MSB_ADDR = 0X11
        self.BNO055_MAG_DATA_Z_LSB_ADDR = 0X12
        self.BNO055_MAG_DATA_Z_MSB_ADDR = 0X13
        
        # Gyro data registers
        self.BNO055_GYRO_DATA_X_LSB_ADDR = 0X14
        self.BNO055_GYRO_DATA_X_MSB_ADDR = 0X15
        self.BNO055_GYRO_DATA_Y_LSB_ADDR = 0X16
        self.BNO055_GYRO_DATA_Y_MSB_ADDR = 0X17
        self.BNO055_GYRO_DATA_Z_LSB_ADDR = 0X18
        self.BNO055_GYRO_DATA_Z_MSB_ADDR = 0X19

        # Temperature data register
        self.BNO055_TEMP_ADDR = 0X34

    ##
    # @brief This function updates the list of xyz acceleration, gyroscope, and magnetometer global variables
    def setData(self):
        self.XAaccelData = data_to_int(self.bus, self.link, self.BNO055_ACCEL_DATA_X_MSB_ADDR, self.BNO055_ACCEL_DATA_X_LSB_ADDR)
        self.YAaccelData = data_to_int(self.bus, self.link, self.BNO055_ACCEL_DATA_Y_MSB_ADDR, self.BNO055_ACCEL_DATA_Y_LSB_ADDR)
        self.ZAaccelData = data_to_int(self.bus, self.link, self.BNO055_ACCEL_DATA_Z_MSB_ADDR, self.BNO055_ACCEL_DATA_Z_LSB_ADDR)

        self.XRotGyroData = data_to_int(self.bus, self.link, self.BNO055_GYRO_DATA_X_MSB_ADDR, self.BNO055_GYRO_DATA_X_LSB_ADDR)
        self.YRotGyroData = data_to_int(self.bus, self.link, self.BNO055_GYRO_DATA_Y_MSB_ADDR, self.BNO055_GYRO_DATA_Y_LSB_ADDR)
        self.ZRotGyroData = data_to_int(self.bus, self.link, self.BNO055_GYRO_DATA_Z_MSB_ADDR, self.BNO055_GYRO_DATA_Z_LSB_ADDR)

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
