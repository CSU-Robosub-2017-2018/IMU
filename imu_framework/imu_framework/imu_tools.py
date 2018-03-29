import numpy as np
import csv
from .imu_memory import imu_data
from .MAYHONYAHRS import MahonyAHRS
from .quatern_tools import quaternion_tools
import pylab as plt


class imu_tools():
    def __init__(self, fifoMemSize=50, deltaT=0.1, imu=None):

        self.fifoMemSize = fifoMemSize
        self.centerFifoMemSize = int(fifoMemSize / 2)

        self.fifoMemIteration = 0
        self.deltaT = deltaT

        self.memData = imu_data(fifoMemSize=fifoMemSize, imu=imu)
        self.arhs = MahonyAHRS()
        self.qtools = quaternion_tools()

    def get_raw_scale_data(self):
        output = self.memData.getRawData()
        return output

    def get_arhs_rot_matrix(self):
        rawImuData = self.memData.getRawData()

        accX = rawImuData[0]
        accY = rawImuData[1]
        accZ = rawImuData[2]
        gyrX = rawImuData[3]
        gyrY = rawImuData[4]
        gyrZ = rawImuData[5]

        self.arhs.update(accX,
                         accY,
                         accZ,
                         gyrX,
                         gyrY,
                         gyrZ)  # gyroscope units must be radians
        quat = self.arhs.quat()
        R = self.qtools.quatern2rotMat(quat)  # transpose because ahrs provides Earth relative to sensor
        R = np.array(R)
        R = self.qtools.matlabTranspos(R)

        return R

    def get_arhs_tcAccel(self):
        rawImuData = self.memData.getRawData()
        R = self.get_arhs_rot_matrix()
        accX = rawImuData[0]
        accY = rawImuData[1]
        accZ = rawImuData[2]

        inputAcc = np.array([[accX], [accY], [accZ]])
        tcAcc = R.dot(inputAcc)

        tcAcc[2] = tcAcc[2] - 1
        # tcAcc[0] = tcAcc[0] - 5.113477569707675e-04
        # tcAcc[1] = tcAcc[1] - 0.002636871607988
        # tcAcc[2] = tcAcc[2] - 4.357790047748496e-04
        tcAcc = tcAcc * 9.81

        tcAcc = np.transpose(tcAcc)
        tcAcc = np.array([tcAcc[0, 1], tcAcc[0, 1], tcAcc[0, 2]])
        return tcAcc

    def get_arhs_x_vector(self):
        R = self.get_arhs_rot_matrix()
        xVector = [R[0][0], R[1][0], R[2][0]]
        return xVector

    def get_arhs_y_vector(self):
        R = self.get_rot_matrix()
        xVector = [R[0][1], R[1][1], R[2][1]]
        return xVector

    def get_arhs_z_vector(self):
        R = self.get_arhs_rot_matrix()
        xVector = [R[0][2], R[1][2], R[2][2]]
        return xVector

    def get_arhs_vel_bank(self):
        return self.memData.getVelBank()

    def get_arhs_pos_bank(self):
        return self.memData.getPosBank()

    def get_arhs_pos(self):
        iter = self.memData.getIteration()
        output = np.array([0, 0, 0])

        if iter < self.fifoMemSize:
            # print ('stage 1')
            tcAcc = self.get_arhs_tcAccel()
            self.memData.fifo_ACC_MemoryUpdate(tcAcc)

        if (iter >= self.fifoMemSize) & (iter < (self.fifoMemSize) * 2):
            # print ('stage 2')

            accFifoData = self.memData.getfifoAccData()
            filteredAccData = self.bandPassFilter(accFifoData, 1, 500)
            velFromAcc = self.integration(filteredAccData)
            # choose the center
            centerVel = velFromAcc[self.centerFifoMemSize, :]
            self.memData.fifo_VEL_MemoryUpdate(centerVel)
            self.memData.setVelBank(centerVel)

            tcAcc = self.get_arhs_tcAccel()
            self.memData.fifo_ACC_MemoryUpdate(tcAcc)

        if (iter >= (self.fifoMemSize) * 2) & (iter < (self.fifoMemSize) * 3):
            # print ('stage 3')

            velFifoData = self.memData.getfifoVelData()
            filteredVelData = self.bandPassFilter(velFifoData, 1, 500)
            posFromVel = self.integration(filteredVelData)
            # choose the center
            centerPos = posFromVel[self.centerFifoMemSize, :]
            self.memData.fifo_POS_MemoryUpdate(centerPos)
            self.memData.setPosBank(centerPos)

            accFifoData = self.memData.getfifoAccData()
            filteredAccData = self.bandPassFilter(accFifoData, 1, 500)
            velFromAcc = self.integration(filteredAccData)
            # choose the center
            centerVel = velFromAcc[self.centerFifoMemSize, :]
            self.memData.fifo_VEL_MemoryUpdate(centerVel)

            tcAcc = self.get_arhs_tcAccel()
            self.memData.fifo_ACC_MemoryUpdate(tcAcc)

        if iter >= (self.fifoMemSize) * 3:
            # print ('stage 4')
            posFifoData = self.memData.getfifoPosData()
            filteredPosData = self.bandPassFilter(posFifoData, 1, 500)
            output = filteredPosData[self.centerFifoMemSize, :]

            velFifoData = self.memData.getfifoVelData()
            filteredVelData = self.bandPassFilter(velFifoData, 1, 500)
            posFromVel = self.integration(filteredVelData)
            # choose the center
            centerPos = posFromVel[self.centerFifoMemSize, :]
            self.memData.fifo_POS_MemoryUpdate(centerPos)

            accFifoData = self.memData.getfifoAccData()
            filteredAccData = self.bandPassFilter(accFifoData, 1, 500)
            velFromAcc = self.integration(filteredAccData)
            # choose the center
            centerVel = velFromAcc[self.centerFifoMemSize, :]
            self.memData.fifo_VEL_MemoryUpdate(centerVel)

            tcAcc = self.get_arhs_tcAccel()
            self.memData.fifo_ACC_MemoryUpdate(tcAcc)

        # print(iter)
        return output

    def integration(self, data):
        integral = 0
        i = 0
        while i <= len(data):
            integral += data * self.deltaT
        return integral

    def highPassFilter(self, dataIn, cutoff=1):
        cutoff = cutoff / 2

        dataInX = dataIn[:, 0]
        dataInY = dataIn[:, 1]
        dataInZ = dataIn[:, 2]

        W = np.fft.rfftfreq(self.fifoMemSize, self.deltaT)

        f_signalX = np.fft.rfft(dataInX)
        f_signalY = np.fft.rfft(dataInY)
        f_signalZ = np.fft.rfft(dataInZ)

        # plt.plot(f_signalX)
        # plt.show()
        #
        # plt.plot(f_signalY)
        # plt.show()
        #
        # plt.plot(f_signalZ)
        # plt.show()

        f_signalX[(W < cutoff)] = 0
        f_signalY[(W < cutoff)] = 0
        f_signalZ[(W < cutoff)] = 0

        filteredX = np.fft.irfft(f_signalX)
        filteredY = np.fft.irfft(f_signalY)
        filteredZ = np.fft.irfft(f_signalZ)

        output = np.array([filteredX, filteredY, filteredZ]).transpose()
        return output

    def lowPassFilter(self, dataIn, cutoff=20):
        cutoff = cutoff / 2

        dataInX = dataIn[:, 0]
        dataInY = dataIn[:, 1]
        dataInZ = dataIn[:, 2]

        W = np.fft.rfftfreq(self.fifoMemSize, self.deltaT)

        f_signalX = np.fft.rfft(dataInX)
        f_signalY = np.fft.rfft(dataInY)
        f_signalZ = np.fft.rfft(dataInZ)

        f_signalX[(W > cutoff)] = 0
        f_signalY[(W > cutoff)] = 0
        f_signalZ[(W > cutoff)] = 0

        filteredX = np.fft.irfft(f_signalX)
        filteredY = np.fft.irfft(f_signalY)
        filteredZ = np.fft.irfft(f_signalZ)

        output = np.array([filteredX, filteredY, filteredZ]).transpose()
        return output

    def bandPassFilter(self, data, lowerCutoff, upperCutoff):
        output = self.highPassFilter(data, lowerCutoff)
        output = self.lowPassFilter(output, upperCutoff)

        return output

    def rawData2Csv(self, data, iteration, fileName='youForgotToNameYourFile',
                    save_path='C:/Users/bob/Desktop/test accelation to position/data_'):

        fileName = fileName + '.csv'
        nameOfFile = save_path + fileName
        # nameOfFile = os.path.join(save_path, fileName , ".csv")

        if iteration == 0:
            with open(nameOfFile, "w") as csvfile:
                fieldnames = ['Time',
                              'X Acc', 'Y Acc', 'Z Acc',
                              'X Gyro', 'Y Gyro', 'Z Gyro',
                              'X Mag', 'Y Mag', 'Z Mag']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'Time': data[9], 'X Acc': data[0], 'Y Acc': data[1], 'Z Acc': data[2],
                                 'X Gyro': data[3], 'Y Gyro': data[4], 'Z Gyro': data[5],
                                 'X Mag': data[6], 'Y Mag': data[7], 'Z Mag': data[8]})

        if iteration != 0:
            with open(nameOfFile, "a") as csvfile:
                fieldnames = ['Time',
                              'X Acc', 'Y Acc', 'Z Acc',
                              'X Gyro', 'Y Gyro', 'Z Gyro',
                              'X Mag', 'Y Mag', 'Z Mag']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'Time': data[9], 'X Acc': data[0], 'Y Acc': data[1], 'Z Acc': data[2],
                                 'X Gyro': data[3], 'Y Gyro': data[4], 'Z Gyro': data[5],
                                 'X Mag': data[6], 'Y Mag': data[7], 'Z Mag': data[8]})

    def dataForMatlabProcesing(self, data, iteration, fileName='youForgotToNameYourFile',
                               save_path='C:/Users/bob/Desktop/IMU/imu_framework/tests/test_files/'):

        fileName = fileName + '.csv'
        nameOfFile = save_path + fileName
        # nameOfFile = os.path.join(save_path, fileName , ".csv")

        if iteration == 0:
            with open(nameOfFile, "w") as csvfile:
                fieldnames = ['Packet number',
                              'Gyroscope X (deg/s)', 'Gyroscope Y (deg/s)', 'Gyroscope Z (deg/s)',
                              'Accelerometer X (g)', 'Accelerometer Y (g)', 'Accelerometer Z (g)',
                              'Magnetometer X (G)', 'Magnetometer Y (G)', 'Magnetometer Z (G)']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'Packet number': 0,
                                 'Gyroscope X (deg/s)': data[3], 'Gyroscope Y (deg/s)': data[4],
                                 'Gyroscope Z (deg/s)': data[5],
                                 'Accelerometer X (g)': data[0], 'Accelerometer Y (g)': data[1],
                                 'Accelerometer Z (g)': data[2],
                                 'Magnetometer X (G)': data[6], 'Magnetometer Y (G)': data[7],
                                 'Magnetometer Z (G)': data[8]})

        if iteration != 0:
            with open(nameOfFile, "a") as csvfile:
                fieldnames = ['Packet number',
                              'Gyroscope X (deg/s)', 'Gyroscope Y (deg/s)', 'Gyroscope Z (deg/s)',
                              'Accelerometer X (g)', 'Accelerometer Y (g)', 'Accelerometer Z (g)',
                              'Magnetometer X (G)', 'Magnetometer Y (G)', 'Magnetometer Z (G)']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'Packet number': iteration,
                                 'Gyroscope X (deg/s)': data[3], 'Gyroscope Y (deg/s)': data[4],
                                 'Gyroscope Z (deg/s)': data[5],
                                 'Accelerometer X (g)': data[0], 'Accelerometer Y (g)': data[1],
                                 'Accelerometer Z (g)': data[2],
                                 'Magnetometer X (G)': data[6], 'Magnetometer Y (G)': data[7],
                                 'Magnetometer Z (G)': data[8]})

    def procesedAccRot2Csv(self, dataAccel, dataR, iteration, fileName='youForgotToNameYourFile',
                           save_path='C:/Users/bob/Desktop/IMU/imu_framework/tests/test_files/'):

        fileName = fileName + '.csv'
        nameOfFile = save_path + fileName
        # nameOfFile = os.path.join(save_path, fileName , ".csv")

        data = [dataAccel[0], dataAccel[1], dataAccel[2],
                dataR[0, 0], dataR[0, 1], dataR[0, 2],
                dataR[1, 0], dataR[1, 1], dataR[1, 2],
                dataR[2, 0], dataR[2, 1], dataR[2, 2]]

        # print(data)

        if iteration == 0:
            with open(nameOfFile, "w") as csvfile:
                fieldnames = ['X Acc', 'Y Acc', 'Z Acc',
                              'R[00]', 'R[01]', 'R[02]',
                              'R[10]', 'R[11]', 'R[12]',
                              'R[20]', 'R[21]', 'R[22]']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'X Acc': data[0], 'Y Acc': data[1], 'Z Acc': data[2],
                                 'R[00]': data[3], 'R[01]': data[4], 'R[02]': data[5],
                                 'R[10]': data[6], 'R[11]': data[7], 'R[12]': data[8],
                                 'R[20]': data[9], 'R[21]': data[10], 'R[22]': data[11]})

        if iteration != 0:
            with open(nameOfFile, "a") as csvfile:
                fieldnames = ['X Acc', 'Y Acc', 'Z Acc',
                              'R[00]', 'R[01]', 'R[02]',
                              'R[10]', 'R[11]', 'R[12]',
                              'R[20]', 'R[21]', 'R[22]']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'X Acc': data[0], 'Y Acc': data[1], 'Z Acc': data[2],
                                 'R[00]': data[3], 'R[01]': data[4], 'R[02]': data[5],
                                 'R[10]': data[6], 'R[11]': data[7], 'R[12]': data[8],
                                 'R[20]': data[9], 'R[21]': data[10], 'R[22]': data[11]})

    def RawAndProcesedData2Csv(self, data, iteration, fileName='youForgotToNameYourFile',
                               save_path='C:/Users/bob/Desktop/test accelation to position/data_'):

        fileName = fileName + '.csv'
        nameOfFile = save_path + fileName
        # nameOfFile = os.path.join(save_path, fileName , ".csv")

        if iteration == 0:
            with open(nameOfFile, "w") as csvfile:
                fieldnames = ['Time',
                              'X Acc', 'Y Acc', 'Z Acc',
                              'R[00]', 'R[01]', 'R[02]',
                              'R[10]', 'R[11]', 'R[12]',
                              'R[20]', 'R[21]', 'R[22]']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'Time': data[9],
                                 'X Acc': data[0], 'Y Acc': data[1], 'Z Acc': data[2],
                                 'R[00]': data[3], 'R[01]': data[4], 'R[02]': data[5],
                                 'R[10]': data[6], 'R[11]': data[7], 'R[12]': data[8],
                                 'R[20]': data[9], 'R[21]': data[10], 'R[22]': data[11]})

        if iteration != 0:
            with open(nameOfFile, "a") as csvfile:
                fieldnames = ['Time',
                              'X Acc', 'Y Acc', 'Z Acc',
                              'R[00]', 'R[01]', 'R[02]',
                              'R[10]', 'R[11]', 'R[12]',
                              'R[20]', 'R[21]', 'R[22]']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'Time': data[9],
                                 'X Acc': data[0], 'Y Acc': data[1], 'Z Acc': data[2],
                                 'R[00]': data[3], 'R[01]': data[4], 'R[02]': data[5],
                                 'R[10]': data[6], 'R[11]': data[7], 'R[12]': data[8],
                                 'R[20]': data[9], 'R[21]': data[10], 'R[22]': data[11]})

    def csvRawData2Array(self, fileName='C:/Users/bob/Desktop/IMU/imu_framework/tests/test_files/keep.csv'):
        csv = np.genfromtxt(fileName, delimiter=",")
        accX = csv[1:-1, 1]
        accY = csv[1:-1, 2]
        accZ = csv[1:-1, 3]

        gyrX = csv[1:-1, 4]
        gyrY = csv[1:-1, 5]
        gyrZ = csv[1:-1, 6]

        magX = csv[1:-1, 7]
        magY = csv[1:-1, 8]
        magZ = csv[1:-1, 9]

        output = [accX, accY, accZ, gyrX, gyrY, gyrZ, magX, magY, magZ]
        return output

    def file_len(fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i

