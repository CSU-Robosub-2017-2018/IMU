from imu_framework.tests.context import imu_tools
from imu_framework.tests.context import imu_no_thrd_sparton


if __name__ == '__main__':

    #### instantiate and connect IMUs ####################################
    myIMU_sparton = imu_no_thrd_sparton()
    myIMU_sparton.connect()

    # fix me   take all and put into tools so multipal instantiations are can be achived
    ######################################################################
    myTools = imu_tools( fifoMemSize=100, imu=myIMU_sparton)

    i = 0
    print('start')
    while i <= 10000:

        pos = myTools.get_arhs_pos()
        print(pos)
        i = i + 1

    # print(myTools.get_arhs_vel_bank())
    print('stop')
    #### disconnect all IMUs #############################################
    myIMU_sparton.disconnect()