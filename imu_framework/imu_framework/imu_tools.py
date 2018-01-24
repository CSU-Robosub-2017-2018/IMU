import numpy as np
import csv
import os.path
import matplotlib.pyplot as plt


class imu_tools():
    def __init__(self, fifoMemSize=10000, deltaT=0.0001):

        self.fifoMemSize = fifoMemSize
        self.fifoMemIteration = 0
        self.fifoMemory = np.zeros(self.fifoMemSize)

        self.deltaT = deltaT

        self.memoryXAData = 0
        self.memoryYAData = 0
        self.memoryZAData = 0
        self.memoryXGAData = 0
        self.memoryYGAData = 0
        self.memoryZGAData = 0
        self.memoryXMData = 0
        self.memoryYMData = 0
        self.memoryZMData = 0

        self.memoryXVData = 0
        self.memoryYVData = 0
        self.memoryZVData = 0
        self.memoryXGVData = 0
        self.memoryYGVData = 0
        self.memoryZGVData = 0

        self.memoryXPData = 0
        self.memoryYPData = 0
        self.memoryZPData = 0
        self.memoryXGPData = 0
        self.memoryYGPData = 0
        self.memoryZGPData = 0

    def fifoMemoryUpdate(self, inputData):
        i = 0
        if self.fifoMemIteration < self.fifoMemSize:
            self.fifoMemory[self.fifoMemIteration] = inputData
        if self.fifoMemIteration >= self.fifoMemSize:
            while i <= (self.fifoMemSize - 2):
                self.fifoMemory[i] = self.fifoMemory[i + 1]
                i += 1
            self.fifoMemory[self.fifoMemSize - 1] = inputData
        self.fifoMemIteration += 1

    def memoryPacket(self, inputData):
        self.memoryXAData = inputData[0]
        self.memoryYAData = inputData[1]
        self.memoryZAData = inputData[2]
        self.memoryXGAData = inputData[3]
        self.memoryYGAData = inputData[4]
        self.memoryZGAData = inputData[5]
        self.memoryXMData = inputData[6]
        self.memoryYMData = inputData[7]
        self.memoryZMData = inputData[8]

        self.memoryXVData = self.memoryXVData + self.memoryXAData * self.deltaT
        self.memoryYVData = self.memoryYVData + self.memoryYAData * self.deltaT
        self.memoryZVData = self.memoryZVData + self.memoryZAData * self.deltaT
        self.memoryXGVData = self.memoryXGVData + self.memoryXGAData * self.deltaT
        self.memoryYGVData = self.memoryYGVData + self.memoryYGAData * self.deltaT
        self.memoryZGVData = self.memoryZGVData + self.memoryZGAData * self.deltaT

        self.memoryXPData = self.memoryXPData + self.memoryXVData * self.deltaT
        self.memoryYPData = self.memoryYPData + self.memoryYVData * self.deltaT
        self.memoryZPData = self.memoryZPData + self.memoryZVData * self.deltaT
        self.memoryXGPData = self.memoryXGPData + self.memoryXGVData * self.deltaT
        self.memoryYGPData = self.memoryYGPData + self.memoryYGVData * self.deltaT
        self.memoryZGPData = self.memoryZGPData + self.memoryZGVData * self.deltaT

    def getMemmoryPacket(self):
        outPut = [0] * 21
        outPut[0] = self.memoryXAData
        outPut[1] = self.memoryYAData
        outPut[2] = self.memoryZAData
        outPut[3] = self.memoryXGAData
        outPut[4] = self.memoryYGAData
        outPut[5] = self.memoryZGAData
        outPut[6] = self.memoryXVData
        outPut[7] = self.memoryYVData
        outPut[8] = self.memoryZVData
        outPut[9] = self.memoryXGVData
        outPut[10] = self.memoryYGVData
        outPut[11] = self.memoryZGVData
        outPut[12] = self.memoryXPData
        outPut[13] = self.memoryYPData
        outPut[14] = self.memoryZPData
        outPut[15] = self.memoryXGPData
        outPut[16] = self.memoryYGPData
        outPut[17] = self.memoryZGPData
        outPut[18] = self.memoryXMData
        outPut[19] = self.memoryYMData
        outPut[20] = self.memoryZMData
        print(outPut)
        return outPut

    def get_fifoMemory(self):
        return self.fifoMemory

    def highPassFilter(self, filterSize=150000):
        W = np.fft.fftfreq(self.fifoMemSize, 0.0000025)
        f_signal = np.fft.fft(self.fifoMemory)
        cut_f_signal = f_signal.copy()
        cut_f_signal[(np.abs(W) < filterSize)] = 0
        cut_signal = np.fft.ifft(cut_f_signal)
        return cut_signal

    def lowPassFilter(self, filterSize):
        W = np.fft.fftfreq(self.fifoMemSize, 0.0000025)
        f_signal = np.fft.fft(self.fifoMemory)
        cut_f_signal = f_signal.copy()
        cut_f_signal[(np.abs(W) > filterSize)] = 0
        cut_signal = np.fft.ifft(cut_f_signal)
        return cut_signal

    # def movingAverage(self, filterSize):
        


    def print2CvFile(self, data, iteration, fileName='youForgotToNameYourFile',
                     save_path='C:/Users/bob/Desktop/test accelation to position/data_'):

                     #save_path='C:/Users/bob/Desktop/IMU/imu_framework/tests/test_files/data_'):
        # '/home/pi/Desktop/imu_framework//IMU/tests/test_files/data/csv'............
        fileName = fileName + '.csv'
        nameOfFile = save_path + fileName
        #nameOfFile = os.path.join(save_path, fileName , ".csv")

        if iteration == 0:
            with open(nameOfFile, "w") as csvfile:
                fieldnames = ['Time', 'X Acc', 'Y Acc', 'Z Acc', 'X Gyro', 'Y Gyro', 'Z Gyro', 'X Mag', 'Y Mag', 'Z Mag']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'Time': data[9], 'X Acc': data[0], 'Y Acc': data[1], 'Z Acc': data[2],
                                 'X Gyro': data[3], 'Y Gyro': data[4], 'Z Gyro': data[5],
                                 'X Mag': data[6], 'Y Mag': data[7], 'Z Mag': data[8]})

        if iteration != 0:
            with open(nameOfFile, "a") as csvfile:
                fieldnames = ['Time', 'X Acc', 'Y Acc', 'Z Acc', 'X Gyro', 'Y Gyro', 'Z Gyro', 'X Mag', 'Y Mag', 'Z Mag']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'Time': data[9], 'X Acc': data[0], 'Y Acc': data[1], 'Z Acc': data[2],
                                 'X Gyro': data[3], 'Y Gyro': data[4], 'Z Gyro': data[5],
                                 'X Mag': data[6], 'Y Mag': data[7], 'Z Mag': data[8]})


    def npArray2Tuple(self, array):
        outPut = tuple(map(tuple, array))
        return outPut

    def livePlot(self, data):
        plt.clf()
        plt.plot(data)
        plt.pause(0.00000000001)



    def csvData2NpArray(self, fileName = 'C:/Users/bob/Desktop/IMU/imu_framework/tests/test_files/keep.csv', column=0, start=1, stop=-1):
        csv = np.genfromtxt(fileName, delimiter=",")
        output = csv[start:stop, column]
        return output

    def myCsvData2NpArray(self, fileName = 'C:/Users/bob/Desktop/IMU/imu_framework/tests/test_files/keep.csv'):
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