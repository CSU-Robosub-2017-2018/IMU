from imu_framework.imu_framework.imus.imu import imu
import struct
import time
import serial


class imu_thrd_sparton(imu):


    def __init__(self, porty='COM3', timeout=2):
        imu.__init__(self)
        self.hasAccel = True
        self.hasGyro = True
        self.hasMagno = True
        self.ser = serial.Serial(timeout=timeout, xonxoff=1, baudrate=115200)
        self.ser.port = porty

        self.openString = bytes(str('\r\n\r\nprinttrigger 1 accelp.p set\r\n\r\nprinttrigger 1 accelp.p set drop\r\n drop\r\n').encode('utf-8') )
        self.closeString = bytes(str('\r\n\r\nprinttrigger 0 accelp.p set\r\n\r\nprinttrigger 0 accelp.p set drop\r\n drop\r\n').encode('utf-8') )



    def connect(self):
        self.ser.open()
        self.ser.write(self.openString)
        print(self.ser.read(60))


    def disconnect(self):
        self.ser.write(self.closeString)
        self.ser.flush()
        self.ser.close()

    def setData(self):
        outPutFromImu = self.ser.readline()
        # print(outPutFromImu)
        # if outPutFromImu.decode("utf-8")
        try:
            v = list(map(float, outPutFromImu.decode("utf-8").split(',')))
            self.ser.flush()
        except ValueError:
            print('error 1', self.ser.read(60))
            self.ser.flush()
            print('error 2 = ', self.ser.readline())
            v = list(map(float, self.ser.readline().decode("utf-8").split(',')))
            self.ser.flush()

        # try:
        #     i = int(v[8])
        # except IndexError:
        #     print('v[8]')
        #     print()
        #     print()
        #     print('error 1', self.ser.read(60))
        #     self.ser.flush()
        #     print('error 2 = ', self.ser.readline())
        #     v = list(map(float, self.ser.readline().decode("utf-8").split(',')))
        #     self.ser.flush()

        self.XAaccelData = v[4]/206.2
        self.YAaccelData = v[5]/206.2
        self.ZAaccelData = v[6]/206.2

        self.XRotGyroData = v[7]
        self.YRotGyroData = v[8]
        # self.ZRotGyroData = v[9]

        self.XMagnoData = v[1]
        self.YMagnoData = v[2]
        self.ZMagnoData = v[3]

        self.timeStamp = v[0]
