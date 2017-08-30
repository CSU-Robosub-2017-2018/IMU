from imu_framework.imus.imu import imu
import struct
import time
import serial


class imu_this_is_starta(imu):
    def __init__(self,porty='COM4', timeout=2):
        imu.__init__(self)
        self.hasAccel = True
        self.hasGyro = True
        self.hasMagno = True
        self.ser = serial.Serial(timeout=timeout, xonxoff=1, baudrate=115200)
        self.ser.port = porty

        self.openString = bytes('\r\n\r\nprinttrigger 1 s.p set drop\r\n', 'utf-8')
        self.closeString = bytes('\r\n\r\nprinttrigger 0 s.p set drop\r\n', 'utf-8')

    def connect(self):
        self.ser.open()
        self.ser.write(self.openString)
        print(self.ser.read(65))


    def disconnect(self):
        self.ser.write(self.closeString)
        self.ser.flush()
        self.ser.close()

    def setData(self):
        outPutFromImu = self.ser.readline()
        v = list(map(int, outPutFromImu.decode("utf-8").split(',')))
        self.ser.flush()
        self.XAaccelData = v[4]
        self.YAaccelData = v[5]
        self.ZAaccelData = v[6]

        self.XRotGyroData = v[7]
        self.YRotGyroData = v[8]
        self.ZRotGyroData = v[9]

        self.XMagnoData = v[1]
        self.YMagnoData = v[2]
        self.ZMagnoData = v[3]
