# context.py - Allows tests to run from the tests directory more easily
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from imu_framework.imu_framework.quatern_tools import quaternion_tools
# from imu_framework.imu_framework.imus.imu_9250 import imu_9250
from imu_framework.imu_framework.imus.imu_sparton_procesed_acc import imu_this_is_starta
from imu_framework.imu_framework.imus.imu_this_is_sparton_no_thread import imu_this_is_starta
from imu_framework.imu_framework.imu_tools import imu_tools
from imu_framework.imu_framework.MAYHONYAHRS import MahonyAHRS
from imu_framework.imu_framework.quatern_tools import quaternion_tools