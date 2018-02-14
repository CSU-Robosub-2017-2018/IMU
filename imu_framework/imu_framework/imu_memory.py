import numpy as np


class imu_data():

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

        self.AccBank = np.zeros([self.fifoMemSize, 3])   # [180000, 3])  # set to aporimentaly 30 min of data
        self.VelBank = np.zeros([self.fifoMemSize, 3])
        self.PosBank = np.zeros([self.fifoMemSize, 3])

        self.AccBankIteration = 0
        self.VelBankIteration = 0
        self.PosBankIteration = 0



    ######## set data to memory
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




    def setAccBank(self, data):
        self.AccBank[self.AccBankIteration] = data
        self.AccBankIteration += 1

    def setVelBank(self, data):
        self.VelBank[self.AccBankIteration] = data
        self.VelBankIteration += 1

    def setPosBank(self, data):
        self.PosBank[self.AccBankIteration] = data
        self.PosBankIteration += 1



######## get dat from memory
    def getAccBank(self):
        ouptut = self.AccBank
        return ouptut

    def getVelBank(self):
        ouptut = self.VelBank
        return ouptut

    def getPosBank(self):
        ouptut = self.PosBank
        return ouptut



    def getfifoAccData(self):
        ouptut = self.fifo_ACC_Memory
        return ouptut

    def getfifoVelData(self):
        ouptut = self.fifo_ACC_Memory
        return ouptut

    def getfifoPosData(self):
        ouptut = self.fifo_ACC_Memory
        return ouptut


    def getRawData(self):
        self.imu.setData()
        ouptut = self.imu.getAllAvalableData()
        return ouptut

    def getIteration(self):
        return self.fifoMemIteration
