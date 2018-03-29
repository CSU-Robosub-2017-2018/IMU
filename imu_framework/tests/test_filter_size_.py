from imu_framework.tests.context import imu_tools
from imu_framework.tests.context import imu_base
import pylab as plt


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
    # myTools = imu_tools(imu=myIMU_no_thrd_sparton)
    myTools = imu_tools(fifoMemSize=5000, imu=myIMU_base)

    i = 0
    print('start')
    while i <= 4999:

        # rawAccel = myTools.get_raw_scale_data()
        # print(i)
        # print(rawAccel)
        # myTools.dataForMatlabProcesing(rawAccel, i, 'LoggedData_CalInertialAndMag')

        # tcAcceleration = myTools.get_arhs_tcAccel()
        # print(tcAcceleration)
        # R = myTools.get_arhs_rot_matrix()
        # print(R)
        # myTools.procesedAccRot2Csv(tcAcceleration, R, i, 'dataFromPython', 'C:/Users/bob/Desktop/IMU/imu_framwork_matlab/test matlab/')
        #
        # zVector = myTools.get_arhs_z_vector()
        # print(zVector)
        i = i + 1

        ######## disconnect all IMUs #############################################

    # myIMU_no_thrd_sparton.disconnect()
    print(i)

    time = np.linspace(0, 10, 2000)
    signal = np.cos(3 * np.pi * time) + np.cos(10 * np.pi * time)
    signalIN = np.array([signal, 2 * signal, 3 * signal]).transpose()

    myTools = imu_tools(signal.size, deltaT=time[1] - time[0])
    cut_signal_tools_10 = myTools.bandPassFilter(signalIN, 8, 11)
    cut_signal_tools_3 = myTools.bandPassFilter(signalIN, 1, 5)

    plt.subplot(331)
    plt.plot(time, signalIN[:, 0])
    plt.xlim(0, 1)
    plt.subplot(332)
    plt.plot(time, signalIN[:, 1])
    plt.xlim(0, 1)
    plt.subplot(333)
    plt.plot(time, signalIN[:, 2])
    plt.xlim(0, 1)

    plt.subplot(334)
    plt.plot(time, cut_signal_tools_10[:, 0])
    plt.xlim(0, 1)
    plt.subplot(335)
    plt.plot(time, cut_signal_tools_10[:, 1])
    plt.xlim(0, 1)
    plt.subplot(336)
    plt.plot(time, cut_signal_tools_10[:, 2])
    plt.xlim(0, 1)

    plt.subplot(337)
    plt.plot(time, cut_signal_tools_3[:, 0])
    plt.xlim(0, 1)
    plt.subplot(338)
    plt.plot(time, cut_signal_tools_3[:, 1])
    plt.xlim(0, 1)
    plt.subplot(339)
    plt.plot(time, cut_signal_tools_3[:, 2])
    plt.xlim(0, 1)

    plt.show()


