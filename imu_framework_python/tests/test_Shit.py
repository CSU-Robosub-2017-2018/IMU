from imu_framework.imus.imu import imu
import struct
import time
import serial


class imu_this():
    ser = serial.Serial(xonxoff=1, baudrate=115200)
    ser.port = 'COM4'

    openString = bytes('\r\n\r\nprinttrigger 1 s.p set drop\r\n', 'utf-8')

    ser.open()
    ser.write(openString)
