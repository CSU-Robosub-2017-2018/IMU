from imu_framework.tests.context import imu_tools
from imu_framework.tests.context import imu_base
import numpy as np

if __name__ == '__main__':
    myIMU_base = imu_base()
    myIMU_base.connect(fileName='LoggedData_CalInertialAndMag_eddited.csv')


    myTools = imu_tools(imu=myIMU_base, deltaT=1/250)



    endOffile = myIMU_base.lengthOfFile

    rawAccel = np.zeros([endOffile, 3])
    rawGyr = np.zeros([endOffile, 3])

    tCAccel = np.zeros([endOffile, 3])
    R1by9 = np.zeros([endOffile, 9])




    i = 0
    print('start')
    while i <= endOffile-1:

        # rawData = myTools.get_raw_scale_data()
        # rawAccel[i] = [rawData[0], rawData[1], rawData[2]]
        # rawGyr [i] = [rawData[3], rawData[4], rawData[5]]

        data = myTools.get_arhs_tcAccel_R()

        tCAccel[i] = [data[0], data[1], data[2]]
        R1by9[i] = [data[3], data[4], data[5],
                    data[6], data[7], data[8],
                    data[9], data[10], data[11]]




        i = i + 1

    vel = myTools.integration(tCAccel)

    filtVel = myTools.bandPassFilter(vel, 1, 200)

    pos = myTools.integration(vel)

    filtPos = myTools.bandPassFilter(pos, .01, 200)

    myTools.postProcessing(vel,R1by9, 'testing', 'C:/Users/bob/Desktop/Oscillatory-Motion-Tracking-With-x-IMU/')






    print('stop')



