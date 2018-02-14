from imu_framework.tests.context import imu_this_is_starta
from imu_framework.tests.context import imu_tools

if __name__ == '__main__':
    myIMU = imu_this_is_starta()
    myTools = imu_tools()
    rawImuData = 0
    myIMU.connect()
    i = 0
    print('start')
    while i <= 5000:
        myIMU.setData()
        rawImuData = myIMU.getAllAvalableData()

        XAaccel = rawImuData[0]
        YAaccel = rawImuData[1]
        ZAaccel = rawImuData[2]

        XRotGyro = rawImuData[3]
        YRotGyro = rawImuData[4]
        ZRotGyro = rawImuData[5]

        XMagno = rawImuData[6]
        YMagno = rawImuData[7]
        ZMagno = rawImuData[8]

        timeStamp = rawImuData[9]

        # print('timettamp ', timeStamp, 'x acc', XAaccel, ' y acc', YAaccel, ' z acc', ZAaccel, ' x ', XRotGyro, ' y ', YRotGyro,
        #       ' z ', ZRotGyro, ' x ', XMagno, ' y ', YMagno, ' z ', ZMagno)
        # # myTools.memoryPacket(rawImuData)
        # # myTools.getMemmoryPacket()
        myTools.print2CvFile(rawImuData, i, fileName='updown')
        i += 1
        # myIMU.disconnect()
    print('done')