''' test_live_plotting.py - Use this program to connect, gather, and plot live data from any imu on file.

'''

from imu_framework.tests.context import imu_tools
from imu_framework.tests.context import imu_base
from imu_framework.tests.context import plottingTools

import numpy as np

if __name__ == '__main__':
    myIMU_base = imu_base()
    myIMU_base.connect(fileName='LoggedData_CalInertialAndMag_eddited.csv')

    myTools = imu_tools(imu=myIMU_base, deltaT=1/250)
    endOffile = myIMU_base.lengthOfFile


    display = plottingTools()

    i = 0
    print('start')
    while i <= endOffile-1:

        # rawData = myTools.get_raw_scale_data()
        # rawAccel = [rawData[0], rawData[1], rawData[2]]
        # rawGyr = [rawData[3], rawData[4], rawData[5]]

        # display.add(i,rawData[0], rawData[1], rawData[2])

        # print (rawAccel)

        data = myTools.get_arhs_tcAccel_R()

        tCAccel = [data[0], data[1], data[2]]
        R1by9 = [data[3], data[4], data[5],
                    data[6], data[7], data[8],
                    data[9], data[10], data[11]]

        display.add(i, data[0], data[1], data[2])

        i = i + 1

    print('stop')

