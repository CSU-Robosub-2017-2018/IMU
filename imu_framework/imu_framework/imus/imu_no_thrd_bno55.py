from imu_framework.imu_framework.imus.imu import imu
import smbus

class imu_no_thrd_bno55(imu):

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


    #connect to above def
    bus = smbus.SMBus(1)  # i2c port 1
    link = 0x68

    def setData(self):
        self.XAaccelData = data_to_int(self.bus, self.link, self.BNO055_ACCEL_DATA_X_MSB_ADDR, self.BNO055_ACCEL_DATA_X_LSB_ADDR)
        self.YAaccelData = data_to_int(self.bus, self.link, self.BNO055_ACCEL_DATA_Y_MSB_ADDR, self.BNO055_ACCEL_DATA_Y_LSB_ADDR)
        self.ZAaccelData = data_to_int(self.bus, self.link, self.BNO055_ACCEL_DATA_Z_MSB_ADDR, self.BNO055_ACCEL_DATA_Z_LSB_ADDR)

        self.XRotGyroData = data_to_int(self.bus, self.link, self.BNO055_GYRO_DATA_X_MSB_ADDR, self.BNO055_GYRO_DATA_X_LSB_ADDR)
        self.YRotGyroData = data_to_int(self.bus, self.link, self.BNO055_GYRO_DATA_Y_MSB_ADDR, self.BNO055_GYRO_DATA_Y_LSB_ADDR)
        self.ZRotGyroData = data_to_int(self.bus, self.link, self.BNO055_GYRO_DATA_Z_MSB_ADDR, self.BNO055_GYRO_DATA_Z_LSB_ADDR)


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