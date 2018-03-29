# context.py - Allows tests to run from the tests directory more easily
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

### tools ######################################################################
from imu_framework.imu_framework.quatern_tools import quaternion_tools
from imu_framework.imu_framework.imu_tools import imu_tools
from imu_framework.imu_framework.MAYHONYAHRS import MahonyAHRS

from imu_framework.imu_framework.imus.imu_base import imu_base

### imus ######################################################################
# from imu_framework.imu_framework.imus.imu_no_thrd_9250 import imu_no_thrd_9250
# from imu_framework.imu_framework.imus.imu_thrd_9250 import imu_thrd_9250

# from imu_framework.imu_framework.imus.imu_no_thrd_bno55 import imu_no_thrd_bno55
# from imu_framework.imu_framework.imus.imu_no_thrd_bno55 import imu_no_thrd_bno55

# from imu_framework.imu_framework.imus.imu_thrd_sparton import imu_thrd_sparton
from imu_framework.imu_framework.imus.imu_no_thrd_sparton import imu_no_thrd_sparton


# from imu_framework.imu_framework.imu_memory import imu_data # fix me do i need this