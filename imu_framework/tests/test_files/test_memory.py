import numpy as np
from imu_framework.tests.context import quaternion_tools
from imu_framework.tests.context import imu_tools
from imu_framework.tests.context import imu_memory


if __name__ == '__main__':

    qtools = quaternion_tools()
    myTools = imu_tools()
    myMem = imu_memory()

    size = 10000

    rawData_ = np.linspace(0, size-1, size)
    rawData = np.zeros([size,3])
    rawData[:,0] = rawData_
    rawData[:,1] = rawData_
    rawData[:,2] = rawData_

    # print(rawData)

    i = 0
    print('start')
    while i <= size-1:
        myMem.fifo_POS_MemoryUpdate(rawData[i])

        i = i + 1