''' generate_test_data.py - Use this program to save raw data that can be used for the base_imu.py.
'''

from imu_framework.tests.context import imu_tools
# from imu_framework.tests.context import imu_base


# from imu_framework.tests.context import imu_no_thrd_9250
# from imu_framework.tests.context import imu_thrd_9250

# from imu_framework.tests.context import imu_no_thrd_bmo
# from imu_framework.tests.context import imu_thrd_bmo

from imu_framework.tests.context import imu_no_thrd_sparton
# from imu_framework.tests.context import imu_thrd_sparton

if __name__ == '__main__':

    ######## instantiate IMUs ####################################
    # myIMU_no_thrd_9250 = imu_no_thrd_9250()
    # myIMU_thrd_9250 = imu_thrd_9250()

    myIMU_no_thrd_sparton = imu_no_thrd_sparton()
    # myIMU_thrd_sparton = imu_thrd_sparton()

    ######## connect all IMUs #############################################
    # myIMU_no_thrd_9250.connect()
    # myIMU_thrd_9250.connect()

    myIMU_no_thrd_sparton.connect()
    # myIMU_thrd_sparton.connect()

    # myIMU_base.connect()

    # fix me   take all and put into tools so multipal instantiations are can be achived
    ##########################################################################
    myTools = imu_tools(imu=myIMU_no_thrd_sparton)

    i = 0
    print('start')
    while i <= 3000:

        print(i)
        rawAccel = myTools.get_raw_scale_data()
        myTools.rawData2Csv(rawAccel, i, 'sparton_imu_test_rot_z', 'C:/Users/bob/Desktop/Oscillatory-Motion-Tracking-With-x-IMU/')

        i = i + 1

        ######## disconnect all IMUs #############################################

    # myIMU_no_thrd_sparton.disconnect()
    print(i)