''' test_arhs.py - Use this test to test arhs on live data or from a file using imu_base.py
'''

from imu_framework.tests.context import imu_tools
from imu_framework.tests.context import imu_base

from imu_framework.tests.context import plottingTools



# from imu_framework.tests.context import imu_no_thrd_9250
# from imu_framework.tests.context import imu_thrd_9250

# from imu_framework.tests.context import imu_no_thrd_bmo
# from imu_framework.tests.context import imu_thrd_bmo

# from imu_framework.tests.context import imu_no_thrd_sparton
# from imu_framework.tests.context import imu_thrd_sparton

if __name__ == '__main__':

    ######## instantiate IMUs ####################################
    # myIMU_no_thrd_9250 = imu_no_thrd_9250()
    # myIMU_thrd_9250 = imu_thrd_9250()

    # myIMU_no_thrd_sparton = imu_no_thrd_sparton()
    # myIMU_thrd_sparton = imu_thrd_sparton()

    myIMU_base = imu_base()


    ######## connect all IMUs #############################################
    # myIMU_no_thrd_9250.connect()
    # myIMU_thrd_9250.connect()

    # myIMU_no_thrd_sparton.connect()
    # myIMU_thrd_sparton.connect()

    myIMU_base.connect()

    # fix me   take all and put into tools so multipal instantiations are can be achived
    ##########################################################################
    myTools = imu_tools(imu=myIMU_base)
    display = plottingTools()


    i = 0
    print('start')
    while i <= 4999:

        tcAcceleration = myTools.get_arhs_tcAccel()

        display.add(i, tcAcceleration[0], tcAcceleration[1], tcAcceleration[2])

        # print(tcAcceleration)
        # R = myTools.get_arhs_rot_matrix()
        # print(R)
        # myTools.procesedAccRot2Csv(tcAcceleration, R, i, 'dataFromPython', 'C:/Users/bob/Desktop/IMU/imu_framwork_matlab/test matlab/')

        i = i + 1

        ######## disconnect all IMUs #############################################

    # myIMU_no_thrd_sparton.disconnect()
    print(i)