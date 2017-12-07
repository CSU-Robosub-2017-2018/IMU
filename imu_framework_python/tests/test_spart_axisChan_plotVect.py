import numpy as np
from imu_framework.quatern_tools import quaternion_tools
from imu_framework.MAYHONYAHRS import MahonyAHRS
from imu_framework.imu_tools import imu_tools
from imu_framework.imus.imu_this_is_sparton_no_thread import imu_this_is_starta
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



if __name__ == '__main__':

    arhs = MahonyAHRS()
    qtools = quaternion_tools()
    myTools = imu_tools()
    myIMU = imu_this_is_starta()

    rawImuData = 0
    myIMU.connect()

    raw_acc_bank = [[0]*3]*60000

    k = 0
    kend = 20
    kend = kend + 1

    i = 0
    print('start')
    while i <= 60000:
        myIMU.setData()
        rawImuData = myIMU.getAllAvalableData()
        timeStamp = rawImuData[9]

        accX = rawImuData[0]
        accY = rawImuData[1]
        accZ = rawImuData[2]
        gyrX = rawImuData[3]
        gyrY = rawImuData[4]
        gyrZ = rawImuData[5]
        magX = rawImuData[6]
        magY = rawImuData[7]
        magZ = rawImuData[8]

        accX = accX / (9.81 * 206.5501)
        accY = accY / (9.81 * 206.5501)
        accZ = accZ / (9.81 * 206.5501)

        gyrX = (gyrX / 110) * (np.pi / 180)
        gyrY = (gyrY / 110) * (np.pi / 180)
        gyrZ = (gyrZ / 110) * (np.pi / 180)

        magX = magX * 1 * 10 ** (-7)
        magY = magY * 1 * 10 ** (-7)
        magZ = magZ * 1 * 10 ** (-7)

        arhs.update(accX,
                    accY,
                    accZ,
                    gyrX,
                    gyrY,
                    gyrZ)  # gyroscope units must be radians
        quat = arhs.quat()
        R = qtools.quatern2rotMat(quat)  # transpose because ahrs provides Earth relative to sensor
        R = np.array(R)
        R = qtools.matlabTranspos(R)

        inputAcc = np.array([[accX], [accY], [accZ]])
        tcAcc = R.dot(inputAcc)

        tcAcc[2] = tcAcc[2] - 1
        tcAcc[0] = tcAcc[0] - 5.113477569707675e-04
        tcAcc[1] = tcAcc[1] - 0.002636871607988
        tcAcc[2] = tcAcc[2] - 4.357790047748496e-04
        tcAcc = tcAcc * 9.81

        tcAcc = np.transpose(tcAcc)

        zVector = [R[0][2], R[1][2], R[2][2]]
        print(zVector)
        # print(zVector)
        # raw_acc_bank[i][:] = tcAcc[:]

        ## crappy plotter
        # if(k>=kend):
        #     plt.close()
        #     soa = np.array([0, 0, 0, R[0][2], R[1][2], R[2][2]])
        #     X, Y, Z, U, V, W = soa
        #     fig = plt.figure()
        #     ax = fig.add_subplot(111, projection='3d')
        #     ax.quiver(X, Y, Z, U, V, W)
        #
        #     ax.set_xlim([-3, 3])
        #     ax.set_ylim([-3, 3])
        #     ax.set_zlim([-3, 3])
        #     plt.pause(0.5)
        #     plt.close()
        #     k = 0

        # k = k + 1
        i = i + 1