''' imu_base.py - This is the base imu that takes in csv files and behaves like
an imu function live. This class should be used for and preliminary testing or
for comparing two different algorithms.
'''

from imu_framework.imu_framework.imus.imu import imu
import numpy as np

class imu_base(imu):

    ##
    # @brief Base class that reads in a csv file and behaves like a live imu
    # @param filePath The absolute file path to the csv file
    # @param self.counter Initializes counter to zero
    # @param self.lengthOfFile Initializes length of the file to zero
    def __init__(self, filePath = None):
        imu.__init__(self)
        self.hasAccel = True
        self.hasGyro = True
        self.hasMagno = True
        self.filePath = filePath

        self.accX = None
        self.accY = None
        self.accZ = None
        self.gyrX = None
        self.gyrY = None
        self.gyrZ = None
        self.magX = None
        self.magY = None
        self.magZ = None

        self.counter = 0
        self.lengthOfFile = 0

    ##
    # @brief reads in the desired csv file, stores the values and updates self.lengthOfFile to the length of the data
    # @param fileName  The name of the csv file that will be used
    # @return lengthOfFile returns the length of the file
    def connect(self, fileName='imu_base_data.csv'):
        pathAndFileName = 'C:/Users/bob/Desktop/IMU/imu_framework/tests/test_files/' + fileName # Fix me remove hardcode path


        csv = np.genfromtxt(pathAndFileName, delimiter=",")
        self.accX = csv[1:-1, 1]
        self.accY = csv[1:-1, 2]
        self.accZ = csv[1:-1, 3]

        self.gyrX = csv[1:-1, 4]
        self.gyrY = csv[1:-1, 5]
        self.gyrZ = csv[1:-1, 6]

        self.magX = csv[1:-1, 7]
        self.magY = csv[1:-1, 8]
        self.magZ = csv[1:-1, 9]

        self.lengthOfFile = len(self.accZ)
        print(self.lengthOfFile)

    ##
    # @brief This function updates the list of xyz acceleration, gyroscope, and magnetometer global variables one row at a time to simulate live data
    def setData(self):

        if(self.counter<self.lengthOfFile):


            self.XAaccelData = self.accX[self.counter]/ (2026*9.8)
            self.YAaccelData = self.accY[self.counter]/ (2026*9.8)
            self.ZAaccelData = self.accZ[self.counter]/ (2026*9.8)

            self.XRotGyroData = (self.gyrX[self.counter]/ 110)*(3.14159265 /180)
            self.YRotGyroData = (self.gyrY[self.counter]/ 110)*(3.14159265 /180)
            self.ZRotGyroData = (self.gyrZ[self.counter]/ 110)*(3.14159265 /180)

            self.XMagnoData = self.magX[self.counter]* 1 * 10 ** (-7)
            self.YMagnoData = self.magY[self.counter]* 1 * 10 ** (-7)
            self.ZMagnoData = self.magZ[self.counter]* 1 * 10 ** (-7)



            self.XAaccelData = self.accX[self.counter]/ (2026)
            self.YAaccelData = self.accY[self.counter]/ (2026)
            self.ZAaccelData = self.accZ[self.counter]/ (2026)

            self.XRotGyroData = (self.gyrX[self.counter]/ 110)
            self.YRotGyroData = (self.gyrY[self.counter]/ 110)
            self.ZRotGyroData = (self.gyrZ[self.counter]/ 110)

            self.XMagnoData = self.magX[self.counter]* 1 * 10 ** (-7)
            self.YMagnoData = self.magY[self.counter]* 1 * 10 ** (-7)
            self.ZMagnoData = self.magZ[self.counter]* 1 * 10 ** (-7)



            # self.XAaccelData = self.accX[self.counter]
            # self.YAaccelData = self.accY[self.counter]
            # self.ZAaccelData = self.accZ[self.counter]
            #
            # self.XRotGyroData = self.gyrX[self.counter]*(3.14159265 /180)
            # self.YRotGyroData = self.gyrY[self.counter]*(3.14159265 /180)
            # self.ZRotGyroData = self.gyrZ[self.counter]*(3.14159265 /180)
            #
            # self.XMagnoData = self.magX[self.counter]
            # self.YMagnoData = self.magY[self.counter]
            # self.ZMagnoData = self.magZ[self.counter]


            # print(self.counter)
            self.counter = self.counter + 1

    ##
    # @brief This function returns the length of the imported csv file
    # @return The length of the loaded csv file
    def getLenOfFile(self):
        return self.lengthOfFile