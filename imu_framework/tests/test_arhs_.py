from imu_framework.tests.context import imu_tools
from imu_framework.tests.context import imu_no_thrd_sparton

if __name__ == '__main__':

    #### instantiate and connect IMUs ####################################
    myIMU_sparton = imu_no_thrd_sparton()
    myIMU_sparton.connect()

    # fix me   take all and put into tools so multipal instantiations are can be achived
    ######################################################################
    myTools = imu_tools(imu=myIMU_sparton)

    i = 0
    print('start')
    while i <= 1000:

        tcAcceleration = myTools.get_arhs_tcAccel()
        print(tcAcceleration)

        zVector = myTools.get_arhs_z_vector()
        # print(zVector)
        i = i + 1

    #### disconnect all IMUs #############################################
    myIMU_sparton.disconnect()