''' test_raw_data.py - Use this program to test the connection between an imu and the computer.

'''

''' test_connectivity.py - Use this file to test connectivity for the sparton or any other imu.

'''

from imu_framework.tests.context import imu_tools
from imu_framework.tests.context import imu_no_thrd_sparton
from time import sleep




if __name__ == '__main__':

    myTools = imu_tools()
    myIMU = imu_no_thrd_sparton()
    myIMU.connect()

    sleep(2)

    myIMU.disconnect()