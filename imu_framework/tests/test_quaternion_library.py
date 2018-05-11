''' test_quaternion_library.py - Use this program to check if the quaternion library is correct.

'''

import numpy as np
from imu_framework.tests.context import quaternion_tools

## Axis-angle to rotation matrix

qtools = quaternion_tools()

axis = np.array([1, 2, 3])
axis = axis / np.linalg.norm(axis)
angle = np.pi / 2

R = qtools.axisAngle2rotMat(axis, angle)

print("rAxis-angle to rotation matrix:")
print(R[0][0], R[0][1], R[0][2])
print(R[1][0], R[1][1], R[1][2])
print(R[2][0], R[2][1], R[2][2])
print("")
print("")
print("")
print("")

## Axis-angle to quaternion

q = qtools.axisAngle2quatern(axis, angle)

print("Axis-angle to quaternion:")
print(q[0], q[1], q[2], q[3])
print("")
print("")
print("")
print("")


## Quaternion to rotation matrix

R = qtools.quatern2rotMat(q)
print("Quaternion to rotation matrix:")
print(R[0][0], R[0][1], R[0][2])
print(R[1][0], R[1][1], R[1][2])
print(R[2][0], R[2][1], R[2][2])
print("")
print("")
print("")
print("")


## Rotation matrix to quaternion

q = qtools.rotMat2quatern(R)
print("Rotation matrix to quaternion:")
print(q[0], q[1], q[2], q[3])
print("")
print("")
print("")
print("")


## Rotation matrix to ZYX Euler angles

euler = qtools.rotMat2euler(R)
print("Rotation matrix to ZYX Euler angles:")
print(euler[0], euler[1], euler[2])
print("")
print("")
print("")
print("")


## Quaternion to ZYX Euler angles

euler = qtools.quatern2euler(q)
print("Quaternion to ZYX Euler angles:")
print(euler[0], euler[1], euler[2])
print("")
print("")
print("")
print("")


## ZYX Euler angles to rotation matrix

R = qtools.euler2rotMat(euler[0], euler[1], euler[2])
print("ZYX Euler angles to rotation matrix:")
print(R[0][0], R[0][1], R[0][2])
print(R[1][0], R[1][1], R[1][2])
print(R[2][0], R[2][1], R[2][2])

