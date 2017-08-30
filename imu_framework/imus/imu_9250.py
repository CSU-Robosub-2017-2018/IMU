'''  imu_9250.py -- Connects a raspberry pi 3 to the IMU9250 using i2c
protacal.  One thread continuously gathers information from the imu.
'''
from .imu import imu
import smbus
import struct
import time
import threading
import _thread


##
# @brief Child class for imu.py for the MPU9250 IMU (Cheap Amazon IMU)
# @param bus initializes communication with IMU over I2C port 1
# @param link initializes communication over I2C link (IMU's decision)
class imu_9250(imu):

    bus = smbus.SMBus(1)  # i2c port 1
    link = 0x68

    ##
    # @brief __init__(self): initializes variables from the parent class with data specific to this imu
    # @param imu.__init__(self)  instance of the parent class
    # @param self.hasAccel  Initializes hasAccel to True, used for malfunction check
    # @param self.hasGyro  Initializes hasGyro to True, used for malfunction check
    # @param self.hasMagno  Initializes hasMagno to False, used for malfunction check
    # @param self.lock used for multithreading
    # @param self.poll_stop_event = threading.Event()  used for multithreading
    # @param self.startpolling() self.lock used for multithreading
    def __init__(self):
        imu.__init__(self)

        self.hasAccel = True
        self.hasGyro = True
        self.hasMagno = False
        self.bus = smbus.SMBus(1)  # i2c port 1
        self.link = 0x68

        #threading
        self.lock = _thread.allocate_lock()
        #self.lock = None
        self.poll_stop_event = threading.Event()
        self.startpolling()
        # thread.start_new_thread(self.pollImage, (self.poll_stop_event))

    ##
    # @brief startpolling(self): Function that starts thread polling
    # @param self.poll_stop_event.is_set(): poll until told to stop
    # @return _thread.start_new_thread(self.pollAllData, (self.poll_stop_event,))
    def startpolling(self):
        if not self.poll_stop_event.is_set():
            _thread.start_new_thread(self.pollAllData, (self.poll_stop_event,))

    ##
    # @brief stoppolling(self): Function that stops polling
    # @return self.poll_stop_event.set() sets variable that stops polling function
    def stoppolling(self):
        self.poll_stop_event.set()

    ##
    # @brief pollAllData(self, poll_stop_event): Function that gathers data from the imu
    # @param self.XAaccelData  Initializes X Accelerometer data to data from imu
    # @param self.YAaccelData  Initializes Y Accelerometer Data to data from imu
    # @param self.ZAaccelData  Initializes Z Accelerometer Data to data from imu
    # @param self.XRotGyroData  Initializes X Gyroscope Data to data from imu
    # @param self.YRotGyroData  Initializes Y Gyroscope Data to data from imu
    # @param self.ZRotGyroData  Initializes Z Gyroscope Data to data from imu
    def pollAllData(self, poll_stop_event):
        # raise Exception('testing')
        while not poll_stop_event.is_set():

            self.lock.acquire()
            self.XAaccelData = data_to_int(self.bus, self.link, 59, 60)/16384
            self.YAaccelData = data_to_int(self.bus, self.link, 61, 62)/16384
            self.ZAaccelData = data_to_int(self.bus, self.link, 63, 64)/16384

            self.XRotGyroData = data_to_int(self.bus, self.link, 67, 68)
            self.YRotGyroData = data_to_int(self.bus, self.link, 69, 70)
            self.ZRotGyroData = data_to_int(self.bus, self.link, 71, 72)
            self.lock.release()


##
# @brief twos_comp(val, bits):  Function that takes in two's complement input and returns integer in base 10
# @pre   needs the binary twos complement number and how many bits describe that number
# @return returns the number n base 10 format
def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


##
# @brief data_to_int(bus, link, highreg, lowreg):  Conects the computer directly to the imu  used for data collection
# @param highdata data is obtained from two different registers,  this is the high byte
# @param lowdata data is obtained from two different registers,  this is the low byte
# @return returns the combined data after passing it through the twos complement function

# Given register and bus constraints, outputs the correct +/- int corresponding to high and low register values
def data_to_int(bus, link, highreg, lowreg):
    highdata = bus.read_byte_data(link, highreg)
    lowdata = bus.read_byte_data(link, lowreg)
    dblbyte = '{0:08b}'.format(highdata) + '{0:08b}'.format(lowdata)
    return twos_comp(int(dblbyte, 2), 16)