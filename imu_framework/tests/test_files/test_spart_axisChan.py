import numpy as np
from imu_framework.tests.context import quaternion_tools
from imu_framework.tests.context import MahonyAHRS
from imu_framework.tests.context import imu_tools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == '__main__':

    arhs = MahonyAHRS()
    qtools = quaternion_tools()
    myTools = imu_tools()

    [accX, accY, accZ, gyrX, gyrY, gyrZ, magX, magY, magZ] \
        = imu_tools.myCsvData2NpArray(
        'C:/Users/bob/Desktop/IMU/imu_framework/tests/test_files/keep.csv')  ## input constants

    accX = np.array(accX)
    accY = np.array(accY)
    accZ = np.array(accZ)
    gyrX = np.array(gyrX)
    gyrY = np.array(gyrY)
    gyrZ = np.array(gyrZ)
    magX = np.array(magX)
    magY = np.array(magY)
    magZ = np.array(magZ)

    accX = accX / (9.81 * 206.5501)
    accY = accY / (9.81 * 206.5501)
    accZ = accZ / (9.81 * 206.5501)

    gyrX = (gyrX / 110) * (np.pi / 180)
    gyrY = (gyrY / 110) * (np.pi / 180)
    gyrZ = (gyrZ / 110) * (np.pi / 180)

    magX = magX * 1 * 10 ** (-7)
    magY = magY * 1 * 10 ** (-7)
    magZ = magZ * 1 * 10 ** (-7)

    acc = np.array([accX, accY, accZ])
    gyr = np.array([gyrX, gyrY, gyrZ])
    mag = np.array([magX, magY, magZ])

    raw_acc_bank = [[0]*3]*len(accX)

    i = 0
    while i <= len(accX) - 1:
        arhs.update(accX[i],
                    accY[i],
                    accZ[i],
                    gyrX[i],
                    gyrY[i],
                    gyrZ[i])  # gyroscope units must be radians
        quat = arhs.quat()
        R = qtools.quatern2rotMat(quat)  # transpose because ahrs provides Earth relative to sensor
        R = np.array(R)
        R = qtools.matlabTranspos(R)
        nickAngles = qtools.rotMat2euler(R)

        inputAcc = np.array([[accX[i]], [accY[i]], [accZ[i]]])
        tcAcc = R.dot(inputAcc)

        tcAcc[2] = tcAcc[2] - 1
        tcAcc[0] = tcAcc[0] - 5.113477569707675e-04
        tcAcc[1] = tcAcc[1] - 0.002636871607988
        tcAcc[2] = tcAcc[2] - 4.357790047748496e-04
        tcAcc = tcAcc * 9.81
        tcAcc = np.transpose(tcAcc)

        print(nickAngles)
        # raw_acc_bank[i][:] = tcAcc[:]


        soa = np.array([0, 0, 0, R[0][2], R[1][2], R[2][2]])

        X, Y, Z, U, V, W = soa
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.quiver(X, Y, Z, U, V, W)
        ax.set_xlim([-5, 5])
        ax.set_ylim([-5, 5])
        ax.set_zlim([-5, 5])
        plt.pause(0.5)
        plt.close()

        i = i + 1

    # print(raw_acc_bank)