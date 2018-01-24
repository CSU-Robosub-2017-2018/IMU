import numpy as np
import csv
import os.path


class imu_tools():

    def __init__(self, gen_mem_size = 0):
        self.gen_mem = np.zeros(gen_mem_size) # int gen_mem_size for kalman/other memery needing stuff
        self.gen_mem_idx = 0
        self.gen_mem_size = gen_mem_size


    def highPassFilter(self, inputData, filterSize):
        frequency = fouriorTransform(self, inputData)
        if frequency <= filterSize or frequency >= (-filterSize):
            frequency = 0

        outputData = inversFouriorTransform(self, frequency)
        return outputData

    def lowPassFilter(self, inputData, filterSize):
        frequency = fouriorTransform(self, inputData)

        if frequency >= filterSize or frequency <= (-filterSize):
            frequency = 0

        outputData = inversFouriorTransform(self, frequency)

        return outputData

    def print2CvFile(self, dof, data, fileName, testRawFiltered, iteration, save_path='C:/Users/bob/Desktop/imu_framework/imu_framework/data/test'):

        save_path = ''
        if testRawFiltered == 'test':
            save_path = 'C:/Users/bob/Desktop/imu_framework/imu_framework/data/test' #'/home/pi/Desktop/imu_framework/imu_framework/data/test'
            fileName = fileName + '_test_data'
        if testRawFiltered == 'raw':
            save_path = 'C:/Users/bob/Desktop/imu_framework/imu_framework/data/raw' # '/home/pi/Desktop/imu_framework/imu_framework/data/raw'
            fileName = fileName + '_raw_data'
        if testRawFiltered == 'filtered':
            save_path = 'C:/Users/bob/Desktop/imu_framework/imu_framework/data/filtered' # '/home/pi/Desktop/imu_framework/imu_framework/data/filtered'
            fileName = fileName + '_filtered_data'

        nameOfFile = os.path.join(save_path, fileName + ".csv")

        if iteration ==0:
            with open(nameOfFile, "w") as csvfile:
                fieldnames = ['X Acc', 'Y Acc', 'Z Acc', 'X Gyro', 'Y Gyro', 'Z Gyro', 'X Mag', 'Y Mag', 'Z Mag']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'X Acc': data[0], 'Y Acc': data[1], 'Z Acc': data[2],
                                 'X Gyro': data[3], 'Y Gyro': data[4], 'Z Gyro': data[5],
                                 'X Mag': data[6], 'Y Mag': data[7], 'Z Mag': data[8]})


        if iteration !=0:
            with open(nameOfFile, "a") as csvfile:
                fieldnames = ['X Acc', 'Y Acc', 'Z Acc', 'X Gyro', 'Y Gyro', 'Z Gyro', 'X Mag', 'Y Mag', 'Z Mag']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'X Acc': data[0], 'Y Acc': data[1], 'Z Acc': data[2],
                                 'X Gyro': data[3], 'Y Gyro': data[4], 'Z Gyro': data[5],
                                 'X Mag': data[6], 'Y Mag': data[7], 'Z Mag': data[8]})

    def csvData2NpArray(self,fileName):

        datafile = open( fileName , 'r')
        datareader = csv.reader(datafile, delimiter=';')
        data = []
        for row in datareader:
            data.append(row)
        tupleData = tuple(data)
        out = np.array(tupleData)
        outPut = np.delete(out, 0, 0)
        return outPut

    def npArray2Tuple(self, array):
        outPut = tuple(map(tuple, array))
        return outPut

    def filoMemoryUpdate(self, array):
        npArray = np.array(array)
        if self.gen_mem_idx <
        self.gen_mem[self.gen_mem_idxn] = npArray
        self.gen_mem_idx += 1
        if self.gen_mem_idx >= self.gen_mem_size:
            self.gen_mem_idx = 0


def fouriorTransform(self, inputData):
    data = np.array(inputData)
    outputData = np.fft.rfft(data)
    return outputData


def inversFouriorTransform(self, inputData):
    outputData = np.fft.irfft(inputData)
    return outputData
