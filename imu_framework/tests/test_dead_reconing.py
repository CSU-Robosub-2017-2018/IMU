''' test_raw_data.py - Use this program to test the live dead reckoning algorithm.

'''

from imu_framework.tests.context import imu_tools
from imu_framework.tests.context import imu_base


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

    # myIMU_base = imu_base()


    ######## connect all IMUs #############################################
    # myIMU_no_thrd_9250.connect()
    # myIMU_thrd_9250.connect()

    myIMU_no_thrd_sparton.connect()
    # myIMU_thrd_sparton.connect()

    # myIMU_base.connect(fileName='imu_base_data_upDown_z.csv')

    # fix me   take all and put into tools so multipal instantiations are can be achived
    ##########################################################################
    myTools = imu_tools( fifoMemSize=1000, imu=myIMU_no_thrd_sparton)

    i = 0
    print('start')
    while i <= 10000:

        R = myTools.get_arhs_rot_matrix()
        pos = myTools.get_arhs_pos()
        # print(i)
        print(pos)

        # myTools.procesedPosRot2Csv(pos, R, i, 'dataFromPython', 'C:/Users/bob/Desktop/IMU/imu_framwork_matlab/test matlab/')

        i = i + 1

    # print(myTools.get_arhs_vel_bank())
    print('stop')
    #### disconnect all IMUs #############################################
    myIMU_base.disconnect()
    myIMU_no_thrd_sparton.disconnect()
