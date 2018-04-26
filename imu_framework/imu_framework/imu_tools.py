''' imu_tools.py - Use this class get and process data from the imus. Including saving csv files, fft filters, ahrs,
and much more.
'''

import numpy as np
import csv
from .imu_memory import imu_data
from .MAYHONYAHRS import MahonyAHRS
from .quatern_tools import quaternion_tools


class imu_tools():

    ##
    # @brief Obtain and process data from the imus
    # @param fifoMemSize The size of three dimensional fifo memory
    # @param deltaT The period for input of samples
    # @param imu The handle for the imus that will be implemented
    def __init__(self, fifoMemSize=50, deltaT=0.1, imu=None):

        self.fifoMemSize = fifoMemSize
        self.centerFifoMemSize = int(fifoMemSize / 2)

        self.fifoMemIteration = 0
        self.deltaT = deltaT

        self.memData = imu_data(fifoMemSize=fifoMemSize, imu=imu) #FIX ME alow for multiple imus
        self.arhs = MahonyAHRS()
        self.qtools = quaternion_tools()

        self.totalVel = 0
        self.totalPos = 0

    ##
    # @brief Obtain unprocessed data from the imu
    # @return output Returns the unprocessed data from the imu
    def get_raw_scale_data(self):
        output = self.memData.getRawData()
        return output

    ##
    # @brief Obtain the rotation matrix from the imu's most current data
    # @return R The resulting rotation matrix from the imu's most current data in a list of size 3 by 3
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

    ##
    # @brief Obtain the tilt corrected acceleration from the imu's most current data
    # @return tcAcc The resulting tilt corrected acceleration from the imu's most current data in a list of size 3
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
        # self.memData.setAccBank(tcAcc)
        # print(tcAcc)
        return tcAcc


    ##
    # @brief Obtain the tilt corrected acceleration and rotation matrix from the imu's most current data
    # @return tcAcc The resulting tilt corrected acceleration and rotation matrix from the imu's most current data in
    # a list of size 1 by 12 with the first three the x, y, and z acceleration and the last 9 for the rotation matrix
    def get_arhs_tcAccel_R (self):
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

        inputAcc = np.array([[accX], [accY], [accZ]])
        tcAcc = R.dot(inputAcc)

        tcAcc[2] = tcAcc[2] - 1
        # tcAcc[0] = tcAcc[0] - 5.113477569707675e-04
        # tcAcc[1] = tcAcc[1] - 0.002636871607988
        # tcAcc[2] = tcAcc[2] - 4.357790047748496e-04
        tcAcc = tcAcc * 9.81

        tcAcc = np.transpose(tcAcc)
        tcAcc = np.array([tcAcc[0, 0], tcAcc[0, 1], tcAcc[0, 2]])
        # self.memData.setAccBank(tcAcc)
        # print(tcAcc)

        output = [tcAcc[0], tcAcc[1], tcAcc[2],
                R[0, 0], R[0, 1], R[0, 2],
                R[1, 0], R[1, 1], R[1, 2],
                R[2, 0], R[2, 1], R[2, 2]]

        return output

    ##
    # @brief Obtain the tilt x corrected acceleration vector from the imu's most current data
    # @return xVector The resulting x tilt corrected acceleration from the imu's most current data
    def get_arhs_x_vector(self):
        R = self.get_arhs_rot_matrix()
        xVector = [R[0][0], R[1][0], R[2][0]]
        return xVector

    ##
    # @brief Obtain the tilt y corrected acceleration vector from the imu's most current data
    # @return xVector The resulting y tilt corrected acceleration from the imu's most current data
    def get_arhs_y_vector(self):
        R = self.get_rot_matrix()
        yVector = [R[0][1], R[1][1], R[2][1]]
        return yVector

    ##
    # @brief Obtain the tilt z corrected acceleration vector from the imu's most current data
    # @return xVector The resulting z tilt corrected acceleration from the imu's most current data
    def get_arhs_z_vector(self):
        R = self.get_arhs_rot_matrix()
        zVector = [R[0][2], R[1][2], R[2][2]]
        return zVector

    ##
    # @brief Obtain the acceleration bank for the specific imu of choice from its own memory class
    # @return self.memData.getVelBank() The entire acceleration memory bank for the imu of choice
    def getAccBank(self):
        output = self.memData.getAccBank()
        return output

    ##
    # @brief Obtain the velocity bank for the specific imu of choice from its own memory class
    # @return self.memData.getVelBank() The entire velocity memory bank for the imu of choice
    def get_arhs_vel_bank(self):
        return self.memData.getVelBank()

    ##
    # @brief Obtain the position bank for the specific imu of choice from its own memory class
    # @return self.memData.getVelBank() The entire position memory bank for the imu of choice
    def get_arhs_pos_bank(self):
        return self.memData.getPosBank()

    ##
    # @brief Obtain the position from live data (currently does not work properly)
    # @return output The current position according the imu
    def get_arhs_pos_live(self):
        iter = self.memData.getIteration()
        output = np.array([0, 0, 0])

        if iter < self.fifoMemSize:
            # print ('stage 1')
            tcAcc = self.get_arhs_tcAccel()
            self.memData.fifo_ACC_MemoryUpdate(tcAcc)

        if (iter >= self.fifoMemSize) & (iter < (self.fifoMemSize) * 2):
            # print ('stage 2')

            accFifoData = self.memData.getfifoAccData()
            filteredAccData = self.bandPassFilter(accFifoData, 0, 100)
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
            filteredVelData = self.bandPassFilter(velFifoData, 0, 100)
            posFromVel = self.integration(filteredVelData)
            # choose the center
            centerPos = posFromVel[self.centerFifoMemSize, :]
            self.memData.fifo_POS_MemoryUpdate(centerPos)
            self.memData.setPosBank(centerPos)

            accFifoData = self.memData.getfifoAccData()
            filteredAccData = self.bandPassFilter(accFifoData, 0, 100)
            velFromAcc = self.integration(filteredAccData)
            # choose the center
            centerVel = velFromAcc[self.centerFifoMemSize, :]
            self.memData.fifo_VEL_MemoryUpdate(centerVel)

            tcAcc = self.get_arhs_tcAccel()
            self.memData.fifo_ACC_MemoryUpdate(tcAcc)

        if iter >= (self.fifoMemSize) * 3:
            print ('stage 4')
            posFifoData = self.memData.getfifoPosData()
            filteredPosData = self.bandPassFilter(posFifoData, 0, 100)
            output = filteredPosData[self.centerFifoMemSize, :]

            velFifoData = self.memData.getfifoVelData()
            filteredVelData = self.bandPassFilter(velFifoData, 0, 100)
            posFromVel = self.integration(filteredVelData)
            # choose the center
            centerPos = posFromVel[self.centerFifoMemSize, :]
            self.memData.fifo_POS_MemoryUpdate(centerPos)

            accFifoData = self.memData.getfifoAccData()
            filteredAccData = self.bandPassFilter(accFifoData, 0, 100)
            velFromAcc = self.integration(filteredAccData)
            # choose the center
            centerVel = velFromAcc[self.centerFifoMemSize, :]
            self.memData.fifo_VEL_MemoryUpdate(centerVel)

            tcAcc = self.get_arhs_tcAccel()
            self.memData.fifo_ACC_MemoryUpdate(tcAcc)

        # print(iter)
        return output

    ##
    # @brief Take the integral of a set of date using summation (become more accure with faster sample rates)
    # @param data Three dimensional data set with the same length as the fifo storage buffers
    # @return integral Is the integral of the data by summing up rectangles of with sample input period
    def integration(self, data):
        data_size = len(data)
        integral = np.zeros([data_size+1, 3])

        i = 1
        while i <= data_size-1:
            integral[i] = integral[i-1] + data[i] * self.deltaT
            i = i + 1
        return integral

    ##
    # @brief Take the fft of a set of date and set any frequency less than the cut off to zero. The function also has
    # commented out lines that plot all three dimensions before the high pass filter and afterwards
    # @param dataIn Three dimensional data set
    # @param cutoff The desired cut off frequency for the filter
    # @return output Is the high pass filtered data using an ideal fft
    def highPassFilter(self, dataIn, cutoff=0.2):
        cutoff = cutoff / 2

        dataInX = dataIn[:, 0]
        dataInY = dataIn[:, 1]
        dataInZ = dataIn[:, 2]

        data_size = len(dataIn)

        W = np.fft.rfftfreq(data_size, self.deltaT/100)

        f_signalX = np.fft.rfft(dataInX)
        f_signalY = np.fft.rfft(dataInY)
        f_signalZ = np.fft.rfft(dataInZ)

########################################################################################################################
        # plt.subplot(131)
        # plt.plot(W, f_signalX)
        # plt.xlim(0, 50)
        # plt.subplot(132)
        # plt.plot(W, f_signalX)
        # plt.xlim(0, 50)
        # plt.subplot(133)
        # plt.plot(W, f_signalX)
        # plt.xlim(0, 50)
        # plt.show()
########################################################################################################################

        f_signalX[(W < cutoff)] = 0
        f_signalY[(W < cutoff)] = 0
        f_signalZ[(W < cutoff)] = 0

########################################################################################################################
        # plt.subplot(131)
        # plt.plot(W, f_signalX)
        # plt.xlim(0, 50)
        # plt.subplot(132)
        # plt.plot(W, f_signalX)
        # plt.xlim(0, 50)
        # plt.subplot(133)
        # plt.plot(W, f_signalX)
        # plt.xlim(0, 50)
        # plt.show()
########################################################################################################################

        filteredX = np.fft.irfft(f_signalX)
        filteredY = np.fft.irfft(f_signalY)
        filteredZ = np.fft.irfft(f_signalZ)

        output = np.array([filteredX, filteredY, filteredZ]).transpose()
        return output

    ##
    # @brief Take the fft of a set of date and set any frequency greater than the cut off to zero. The function also has
    # commented out lines that plot all three dimensions before the low pass filter and afterwards
    # @param dataIn Three dimensional data set
    # @param cutoff The desired cut off frequency for the filter
    # @return output Is the low pass filtered data using an ideal fft
    def lowPassFilter(self, dataIn, cutoff=8):
        cutoff = cutoff / 2

        dataInX = dataIn[:, 0]
        dataInY = dataIn[:, 1]
        dataInZ = dataIn[:, 2]

        data_size = len(dataIn)

        W = np.fft.rfftfreq(data_size, self.deltaT/100)

        f_signalX = np.fft.rfft(dataInX)
        f_signalY = np.fft.rfft(dataInY)
        f_signalZ = np.fft.rfft(dataInZ)

########################################################################################################################
        # plt.subplot(131)
        # plt.plot(W, f_signalX)
        # plt.xlim(0, 1)
        # plt.subplot(132)
        # plt.plot(W, f_signalX)
        # plt.xlim(0, 1)
        # plt.subplot(133)
        # plt.plot(W, f_signalX)
        # plt.xlim(0, 1)
        # plt.show()
########################################################################################################################

        f_signalX[(W > cutoff)] = 0
        f_signalY[(W > cutoff)] = 0
        f_signalZ[(W > cutoff)] = 0

########################################################################################################################
        # plt.subplot(131)
        # plt.plot(W, f_signalX)
        # plt.xlim(0, 100)
        # plt.subplot(132)
        # plt.plot(W, f_signalX)
        # plt.xlim(0, 100)
        # plt.subplot(133)
        # plt.plot(W, f_signalX)
        # plt.xlim(0, 100)
        # plt.show()
########################################################################################################################

        filteredX = np.fft.irfft(f_signalX)
        filteredY = np.fft.irfft(f_signalY)
        filteredZ = np.fft.irfft(f_signalZ)

        output = np.array([filteredX, filteredY, filteredZ]).transpose()
        return output

    ##
    # @brief This function uses the high pass and low pass filters to make a band pass filter
    # @param dataIn Three dimensional data set
    # @param lowerCutoff The desired cut off frequency for the high pass filter
    # @param upperCutoff The desired cut off frequency for the low pass filter
    # @return output Is the band pass filtered data using an ideal fft
    def bandPassFilter(self, data, lowerCutoff, upperCutoff):
        output = self.highPassFilter(data, lowerCutoff)
        output = self.lowPassFilter(output, upperCutoff)

        return output

    ##
    # @brief This function saves the raw data to the csv file such that the file cannot be corrupted. This could
    # possibly be improved as this method is very slow.
    # @param data The raw data list of size 10 which consists of the following in this order x, y, z acceleration
    # x, y, z rotation x, y, z magnetometer and time stamp
    # @param iteration At iteration 0, the file is created and for all other numbers the data is just appened
    # to the file.
    # @param fileName The desired name of the file excluding .csv or .txt (default is set to 'youForgotToNameYourFile')
    # @param save_path The absolute file path to where you want to save this file
    def rawData2Csv(self, data, iteration, fileName='youForgotToNameYourFile',
                    save_path='C:/Users/bob/Desktop/IMU/imu_framework/tests/test_files/'):

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

    ##
    # @brief This function saves data that is ready for further matlab processing to a csv file such that the
    # file cannot be corrupted. This could possibly be improved as this method is very slow.
    # @param data The data list of size 9 which consists of the following in this order x, y, z acceleration
    # x, y, z rotation x, y, z magnetometer. The acceleration data should be in g and gyroscope data should be in
    # degrees/sec
    # @param iteration At iteration 0, the file is created and for all other numbers the data is just appened
    # to the file.
    # @param fileName The desired name of the file excluding .csv or .txt (default is set to 'youForgotToNameYourFile')
    # @param save_path The absolute file path to where you want to save this file
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

    ##
    # @brief This function saves processed acceleration and the corresponding rotation matrix a csv file such that the
    # file cannot be corrupted. This could possibly be improved as this method is very slow.
    # @param dataAccel The tilt corrected acceleration data in a list of size 3
    # @param dataR The rotation matrix of size 3 by 3
    # @param iteration At iteration 0, the file is created and for all other numbers the data is just
    # appened to the file.
    # @param fileName The desired name of the file excluding .csv or .txt (default is set to 'youForgotToNameYourFile')
    # @param save_path The absolute file path to where you want to save this file
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

    ##
    # @brief This function loads in data directly from a file into a numpy array
    # @param fileName The absolute file path and name of the file that is desired to be imported
    # @param output A list of size 9 by length of file that is being loaded
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

    ##
    # @brief This function saves processed postion and the corresponding rotation matrix a csv file such that the
    # file cannot be corrupted. This could possibly be improved as this method is very slow.
    # @param dataPos The position of the imu in a list of size 3
    # @param dataR The rotation matrix of in a list of size 3 by 3
    # @param iteration At iteration 0, the file is created and for all other numbers the data is
    # just appened to the file.
    # @param fileName The desired name of the file excluding .csv or .txt (default is set to 'youForgotToNameYourFile')
    # @param save_path The absolute file path to where you want to save this file
    def procesedPosRot2Csv(self, dataPos, dataR, iteration, fileName='youForgotToNameYourFile',
                           save_path='C:/Users/bob/Desktop/IMU/imu_framework/tests/test_files/'):

        fileName = fileName + '.csv'
        nameOfFile = save_path + fileName

        data = [dataPos[0], dataPos[1], dataPos[2],
                dataR[0, 0], dataR[0, 1], dataR[0, 2],
                dataR[1, 0], dataR[1, 1], dataR[1, 2],
                dataR[2, 0], dataR[2, 1], dataR[2, 2]]

        # print(data)

        if iteration == 0:
            with open(nameOfFile, "w") as csvfile:
                fieldnames = ['X Pos', 'Y Pos', 'Z Pos',
                              'R[00]', 'R[01]', 'R[02]',
                              'R[10]', 'R[11]', 'R[12]',
                              'R[20]', 'R[21]', 'R[22]']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'X Pos': data[0], 'Y Pos': data[1], 'Z Pos': data[2],
                                 'R[00]': data[3], 'R[01]': data[4], 'R[02]': data[5],
                                 'R[10]': data[6], 'R[11]': data[7], 'R[12]': data[8],
                                 'R[20]': data[9], 'R[21]': data[10], 'R[22]': data[11]})

        if iteration != 0:
            with open(nameOfFile, "a") as csvfile:
                fieldnames = ['X Pos', 'Y Pos', 'Z Pos',
                              'R[00]', 'R[01]', 'R[02]',
                              'R[10]', 'R[11]', 'R[12]',
                              'R[20]', 'R[21]', 'R[22]']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'X Pos': data[0], 'Y Pos': data[1], 'Z Pos': data[2],
                                 'R[00]': data[3], 'R[01]': data[4], 'R[02]': data[5],
                                 'R[10]': data[6], 'R[11]': data[7], 'R[12]': data[8],
                                 'R[20]': data[9], 'R[21]': data[10], 'R[22]': data[11]})

    ##
    # @brief This function determine the length of a csv file (this code is not used anymore)
    # @param fileName The absolute file path and name of the file that is desired to be imported
    # @param i The length of the csv file
    def file_len(fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i