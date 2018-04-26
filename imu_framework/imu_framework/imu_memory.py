''' imu_memory.py - Use this class to store data obtained from the imu for filtering. It stores data in a fifo fashion
to allow for best results when using a an fft. It stores 3-d information for acceleration, velocity and position.
'''
import numpy as np


class imu_data():

    ##
    # @brief Stores acceleration, velocity and positional data
    # @param fifoMemSize The size of the fifo memory
    # @param imu A handel to the imu of choice
    def __init__(self, fifoMemSize=10000, imu=None):

        self.imu = imu
        self.xaccel = None
        self.yaccel = None
        self.Zaccel = None

        self.fifoMemSize = fifoMemSize
        self.fifoMemIteration = 0

        self.fifo_ACC_Memory = np.zeros([self.fifoMemSize, 3])
        self.fifo_VEL_Memory = np.zeros([self.fifoMemSize, 3])
        self.fifo_POS_Memory = np.zeros([self.fifoMemSize, 3])

        self.AccBank = np.zeros([100000, 3])   # [180000, 3])  aporimentaly 30 min of data
        self.VelBank = np.zeros([100000, 3])   # fix me from hard code
        self.PosBank = np.zeros([100000, 3])

        self.AccBankIteration = 0
        self.VelBankIteration = 0
        self.PosBankIteration = 0



    ##
    # @brief This function stores three dimensions of accelerometer data in a fifo fashion
    # @param inputData Is a list of x, y, and z accelerometer data
    def fifo_ACC_MemoryUpdate(self,inputData):
        i = 0
        if self.fifoMemIteration < self.fifoMemSize:
            self.fifo_ACC_Memory[self.fifoMemIteration, 0] = inputData[0]
            self.fifo_ACC_Memory[self.fifoMemIteration, 1] = inputData[1]
            self.fifo_ACC_Memory[self.fifoMemIteration, 2] = inputData[2]

        if self.fifoMemIteration >= self.fifoMemSize:
            while i <= (self.fifoMemSize - 2):
                self.fifo_ACC_Memory[i, 0] = self.fifo_ACC_Memory[i + 1, 0]
                self.fifo_ACC_Memory[i, 1] = self.fifo_ACC_Memory[i + 1, 1]
                self.fifo_ACC_Memory[i, 2] = self.fifo_ACC_Memory[i + 1, 2]
                i += 1

            self.fifo_ACC_Memory[self.fifoMemSize - 1, 0] = inputData[0]
            self.fifo_ACC_Memory[self.fifoMemSize - 1, 1] = inputData[1]
            self.fifo_ACC_Memory[self.fifoMemSize - 1, 2] = inputData[2]
            # print(self.fifo_ACC_Memory)

        self.fifoMemIteration += 1

    ##
    # @brief This function stores three dimensions of velocity data in a fifo fashion
    # @param inputData Is a list of x, y, and z velocity data
    def fifo_VEL_MemoryUpdate(self, inputData):
        i = 0
        if self.fifoMemIteration < self.fifoMemSize:
            self.fifo_VEL_Memory[self.fifoMemIteration, 0] = inputData[0]
            self.fifo_VEL_Memory[self.fifoMemIteration, 1] = inputData[1]
            self.fifo_VEL_Memory[self.fifoMemIteration, 2] = inputData[2]

        if self.fifoMemIteration >= (self.fifoMemSize)*2:
            while i <= (self.fifoMemSize - 2):
                self.fifo_VEL_Memory[i, 0] = self.fifo_VEL_Memory[i + 1, 0]
                self.fifo_VEL_Memory[i, 1] = self.fifo_VEL_Memory[i + 1, 1]
                self.fifo_VEL_Memory[i, 2] = self.fifo_VEL_Memory[i + 1, 2]
                i += 1

            self.fifo_VEL_Memory[self.fifoMemSize - 1, 0] = inputData[0]
            self.fifo_VEL_Memory[self.fifoMemSize - 1, 1] = inputData[1]
            self.fifo_VEL_Memory[self.fifoMemSize - 1, 2] = inputData[2]

    ##
    # @brief This function stores three dimensions of position data in a fifo fashion
    # @param inputData Is a list of x, y, and z position data
    def fifo_POS_MemoryUpdate(self, inputData):
        i = 0
        if self.fifoMemIteration < self.fifoMemSize:
            self.fifo_POS_Memory[self.fifoMemIteration, 0] = inputData[0]
            self.fifo_POS_Memory[self.fifoMemIteration, 1] = inputData[1]
            self.fifo_POS_Memory[self.fifoMemIteration, 2] = inputData[2]

        if self.fifoMemIteration >= (self.fifoMemSize)*3:
            while i <= (self.fifoMemSize - 2):
                self.fifo_POS_Memory[i, 0] = self.fifo_POS_Memory[i + 1, 0]
                self.fifo_POS_Memory[i, 1] = self.fifo_POS_Memory[i + 1, 1]
                self.fifo_POS_Memory[i, 2] = self.fifo_POS_Memory[i + 1, 2]
                i += 1

            self.fifo_POS_Memory[self.fifoMemSize - 1, 0] = inputData[0]
            self.fifo_POS_Memory[self.fifoMemSize - 1, 1] = inputData[1]
            self.fifo_POS_Memory[self.fifoMemSize - 1, 2] = inputData[2]



    ##
    # @brief This function stores three dimensions of accelerometer data
    # @param inputData Is a list of x, y, and z accelerometer data
    def setAccBank(self, data):
        self.AccBank[self.AccBankIteration] = data
        self.AccBankIteration += 1

    ##
    # @brief This function stores three dimensions of velocity data
    # @param inputData Is a list of x, y, and z velocity data
    def setVelBank(self, data):
        self.VelBank[self.AccBankIteration] = data
        self.VelBankIteration += 1

    ##
    # @brief This function stores three dimensions of position data
    # @param inputData Is a list of x, y, and z position data
    def setPosBank(self, data):
        self.PosBank[self.AccBankIteration] = data
        self.PosBankIteration += 1



######## get data from memory

    ##
    # @brief This function returns the stored accelerometer data
    # @return output Is a list of x, y, and z accelerometer data
    def getAccBank(self):
        ouptut = self.AccBank
        return ouptut

    ##
    # @brief This function returns the stored velocity data
    # @return output Is a list of x, y, and z velocity data
    def getVelBank(self):
        ouptut = self.VelBank
        return ouptut

    ##
    # @brief This function returns the stored position data
    # @return output Is a list of x, y, and z position data
    def getPosBank(self):
        ouptut = self.PosBank
        return ouptut


    ##
    # @brief This function returns the stored fifo accelerometer data
    # @return output Is a list of x, y, and z fifo accelerometer data
    def getfifoAccData(self):
        ouptut = self.fifo_ACC_Memory
        return ouptut

    ##
    # @brief This function returns the stored fifo velocity data
    # @return output Is a list of x, y, and z fifo velocity data
    def getfifoVelData(self):
        ouptut = self.fifo_ACC_Memory
        return ouptut

    ##
    # @brief This function returns the stored fifo position data
    # @return output Is a list of x, y, and z fifo position data
    def getfifoPosData(self):
        ouptut = self.fifo_ACC_Memory
        return ouptut

    ##
    # @brief This function returns data from the imu
    # @return output Is a list of x, y, and z accelerometer data dirctly from the imu
    def getRawData(self):
        self.imu.setData()
        ouptut = self.imu.getAllAvalableData()
        return ouptut

    ##
    # @brief This function returns the current fifo memory iteration
    # @return elf.fifoMemIteration Is the current fifo memory iteration
    def getIteration(self):
        return self.fifoMemIteration
