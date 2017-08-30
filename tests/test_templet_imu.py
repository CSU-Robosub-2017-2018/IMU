#!/usr/bin/env python3

''' test_imu.py  - Tests the basic connection to the IMU, and filters by gathering
    all available data followed by filtering it.   The filtered data will be displayed
    the data to the terminal.
'''
from imu_framework.imus.imu_9250 import imu_9250
from imu_framework.imu_tools import imu_tools

##
# @brief Main test code used to access all information from the IMU(s), filter it, and pass it on
# @param rawImuData initializes the IMU for use
# @param separation Separates the tuple obtained from the IMU(s) into their respective measurements
# @return separation Returns 9 DOF variables
if __name__ == '__main__':

    myIMU = imu_9250()
    myFilter = imu_tools()

    rawImuData = 0

    while True:
        rawImuData = myIMU.getAllAvalableData()

        XAaccel = rawImuData[0]
        YAaccel = rawImuData[1]
        ZAaccel = rawImuData[2]

        XRotGyro = rawImuData[3]
        YRotGyro = rawImuData[4]
        ZRotGyro = rawImuData[5]

        XMagno = rawImuData[6]
        YMagno = rawImuData[7]
        ZMagno = rawImuData[8]

        myFilter.fifoMemoryUpdate(rawImuData)

