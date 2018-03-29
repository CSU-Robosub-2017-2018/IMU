from imu_framework.tests.context import imu_tools
from imu_framework.tests.context import imu_base


# from imu_framework.tests.context import imu_no_thrd_9250
# from imu_framework.tests.context import imu_thrd_9250

# from imu_framework.tests.context import imu_no_thrd_9250
# from imu_framework.tests.context import imu_thrd_9250

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

    i = 0
    print('start')
    while i <= 4999:

        rawAccel = myTools.get_raw_scale_data()
        # print(i)
        # print(rawAccel)
        myTools.dataForMatlabProcesing(rawAccel, i, 'LoggedData_CalInertialAndMag')

        # tcAcceleration = myTools.get_arhs_tcAccel()
        # print(tcAcceleration)

        # zVector = myTools.get_arhs_z_vector()
        # print(zVector)
        i = i + 1

        ######## disconnect all IMUs #############################################

    # myIMU_no_thrd_sparton.disconnect()
    print(i)