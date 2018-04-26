'''
    #   For more information see:
    #   http://www.x-io.co.uk/node/8#quaternions
    #
    #	Date          Author          Notes
    #	27/09/2011    SOH Madgwick    Initial release
    #	25/11/2017	  Billy Phillips  MATLAB to Python

    quatern_tools.py - Use this class to convert interchangeably between quaternions, rotation matrix,
    and euler angles.
'''
import numpy as np



class quaternion_tools():


    def axisAngle2quatern(self, axis, angle):
        axis0 = axis[0]
        axis1 = axis[1]
        axis2 = axis[2]

        q0 = np.cos(angle / 2)
        q1 = -axis0 * np.sin(angle / 2)
        q2 = -axis1 * np.sin(angle / 2)
        q3 = -axis2 * np.sin(angle / 2)
        q = np.array([q0, q1, q2, q3])
        return q

    # AXISANGLE2ROTMAT Converts an axis-angle orientation to a rotation matrix
    #
    #   q = axisAngle2rotMat(axis, angle)
    #
    #   Converts and axis-angle orientation to a rotation matrix where a 3D
    #   rotation is described by an angular rotation around axis defined by a
    #   vector.
    #
    #   For more information see:
    #   http://www.x-io.co.uk/node/8#quaternions
    #
    #	Date          Author          Notes
    #	27/09/2011    SOH Madgwick    Initial release
    #	25/11/2017	  Billy Phillips  MATLAB to Python

    ##
    # @brief Converts and axis-angle orientation to a rotation matrix where a 3D
    # rotation is described by an angular rotation around axis defined by a vector.
    # @param axis The axis described by a list of size three
    # @param angel The angle of rotation
    # @return R The resulting rotation matrix of size 3 by 3
    def axisAngle2rotMat(self, axis, angle):
        kx = axis[0]
        ky = axis[1]
        kz = axis[2]
        cT = np.cos(angle)
        sT = np.sin(angle)
        vT = 1 - np.cos(angle)

        R0 = [0] * 3
        R1 = [0] * 3
        R2 = [0] * 3

        R0[0] = kx * kx * vT + cT
        R0[1] = kx * ky * vT - kz * sT
        R0[2] = kx * kz * vT + ky * sT

        R1[0] = kx * ky * vT + kz * sT
        R1[1] = ky * ky * vT + cT
        R1[2] = ky * kz * vT - kx * sT

        R2[0] = kx * kz * vT - ky * sT
        R2[1] = ky * kz * vT + kx * sT
        R2[2] = kz * kz * vT + cT

        R = [R0, R1, R2]
        return R

    # EULER2ROTMAT Converts a ZYX Euler angle orientation to a rotation matrix
    #
    #   q = euler2rotMat(axis, angle)
    #
    #   Converts ZYX Euler angle orientation to a rotation matrix where phi is
    #   a rotation around X, theta around Y and psi around Z.
    #
    #   For more information see:
    #   http://www.x-io.co.uk/node/8#quaternions
    #
    #	Date          Author          Notes
    #	27/09/2011    SOH Madgwick    Initial release
    #	25/11/2017	  Billy Phillips  MATLAB to Python

    ##
    # @brief Converts ZYX Euler angle orientation to a rotation matrix where phi is
    # a rotation around X, theta around Y and psi around Z.
    # @param phi Phi rotation around X
    # @param theta Theta rotation around Y
    # @param psi Psi rotation around Z
    # @return R The resulting rotation matrix of size 3 by 3
    def euler2rotMat(self, phi, theta, psi):
        R0 = [0] * 3
        R1 = [0] * 3
        R2 = [0] * 3

        R0[0] = np.cos(psi) * np.cos(theta)
        R0[1] = -np.sin(psi) * np.cos(phi) + np.cos(psi) * np.sin(theta) * np.sin(phi)
        R0[2] = np.sin(psi) * np.sin(phi) + np.cos(psi) * np.sin(theta) * np.cos(phi)

        R1[0] = np.sin(psi) * np.cos(theta)
        R1[1] = np.cos(psi) * np.cos(phi) + np.sin(psi) * np.sin(theta) * np.sin(phi)
        R1[2] = -np.cos(psi) * np.sin(phi) + np.sin(psi) * np.sin(theta) * np.cos(phi)

        R2[0] = -np.sin(theta)
        R2[1] = np.cos(theta) * np.sin(phi)
        R2[2] = np.cos(theta) * np.cos(phi)

        R = [R0, R1, R2]

        return R

    # QUATERN2EULER Converts a quaternion orientation to ZYX Euler angles
    #
    #   q = quatern2euler(q)
    #
    #   Converts a quaternion orientation to ZYX Euler angles where phi is a
    #   rotation around X, theta around Y and psi around Z.
    #
    #   For more information see:
    #   http://www.x-io.co.uk/node/8#quaternions
    #
    #	Date          Author          Notes
    #	27/09/2011    SOH Madgwick    Initial release
    #	25/11/2017	  Billy Phillips  MATLAB to Python

    ##
    # @brief Converts a quaternion orientation to ZYX Euler angles where phi is a
    # rotation around X, theta around Y and psi around Z.
    # @param q A Quaternion described by a list of size 4
    # @return [phi, theta, psi] The resulting ZYX Euler angles.
    def quatern2euler(self, q):
        q0 = q[0]
        q1 = q[1]
        q2 = q[2]
        q3 = q[3]

        R00 = 2 * q0 ** 2 - 1 + 2 * q1 ** 2
        R10 = 2 * (q1 * q2 - q0 * q3)
        R20 = 2 * (q1 * q3 + q0 * q2)
        R21 = 2 * (q2 * q3 - q0 * q1)
        R22 = 2 * q0 ** 2 - 1 + 2 * q3 ** 2

        phi = np.arctan2(R21, R22)
        theta = -np.arctan(R20 / np.sqrt(1 - R20 ** 2))
        psi = np.arctan2(R10, R00)

        euler = [phi, theta, psi]

        return euler

    # QUATERN2ROTMAT Converts a quaternion orientation to a rotation matrix
    #
    #   R = quatern2rotMat(q)
    #
    #   Converts a quaternion orientation to a rotation matrix.
    #
    #   For more information see:
    #   http://www.x-io.co.uk/node/8#quaternions
    #
    #	Date          Author          Notes
    #	27/09/2011    SOH Madgwick    Initial release
    #	25/11/2017	  Billy Phillips  MATLAB to Python

    ##
    # @brief Converts a quaternion orientation to a rotation matrix.
    # @param q A Quaternion described by a list of size 4
    # @return R The resulting rotation matrix of size 3 by 3
    def quatern2rotMat(self, q):
        q0 = q[0]
        q1 = q[1]
        q2 = q[2]
        q3 = q[3]

        R0 = [0] * 3
        R1 = [0] * 3
        R2 = [0] * 3

        R0[0] = 2 * q0 ** 2 - 1 + 2 * q1 ** 2
        R0[1] = 2 * (q1 * q2 + q0 * q3)
        R0[2] = 2 * (q1 * q3 - q0 * q2)

        R1[0] = 2 * (q1 * q2 - q0 * q3)
        R1[1] = 2 * q0 ** 2 - 1 + 2 * q2 ** 2
        R1[2] = 2 * (q2 * q3 + q0 * q1)

        R2[0] = 2 * (q1 * q3 + q0 * q2)
        R2[1] = 2 * (q2 * q3 - q0 * q1)
        R2[2] = 2 * q0 ** 2 - 1 + 2 * q3 ** 2

        R = [R0, R1, R2]
        return R

    # QUATERN2ROTMAT Converts a quaternion to its conjugate
    #
    #   qConj = quaternConj(q)
    #
    #   Converts a quaternion to its conjugate.
    #
    #   For more information see:
    #   http://www.x-io.co.uk/node/8#quaternions
    #
    #	Date          Author          Notes
    #	27/09/2011    SOH Madgwick    Initial release
    #	25/11/2017	  Billy Phillips  MATLAB to Python

    ##
    # @brief Converts a quaternion to its conjugate.
    # @param q A Quaternion described by a list of size 4
    # @return qConj The resulting quaternion conjugate
    def quaternConj(self, q):
        q0 = q[0]
        q1 = q[1]
        q2 = q[2]
        q3 = q[3]

        qConj = [q0 - q1 - q2 - q3]
        return qConj

    # QUATERNPROD Calculates the quaternion product
    #
    #   ab = quaternProd(a, b)
    #
    #   Calculates the quaternion product of quaternion a and b.
    #
    #   For more information see:
    #   http://www.x-io.co.uk/node/8#quaternions
    #
    #	Date          Author          Notes
    #	27/09/2011    SOH Madgwick    Initial release
    #	25/11/2017	  Billy Phillips  MATLAB to Python

    ##
    # @brief Calculates the quaternion product of quaternion a and b.
    # @param a A Quaternion described by a list of size 4
    # @param b A Quaternion described by a list of size 4
    # @return ab The resulting quaternion product
    def quaternProd(self, a, b):
        a0 = a[0]
        a1 = a[1]
        a2 = a[2]
        a3 = a[3]

        b0 = b[0]
        b1 = b[1]
        b2 = b[2]
        b3 = b[3]

        ab = [0] * 4

        ab[0] = a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3
        ab[1] = a0 * b1 + a1 * b0 + a2 * b3 - a3 * b2
        ab[2] = a0 * b2 - a1 * b3 + a2 * b0 + a3 * b1
        ab[3] = a0 * b3 + a1 * b2 - a2 * b1 + a3 * b0

        return ab

    # ROTMAT2EULER Converts a rotation matrix orientation to ZYX Euler angles
    #
    #   euler = rotMat2euler(R)
    #
    #   Converts a rotation matrix orientation to ZYX Euler angles where phi is
    #   a rotation around X, theta around Y and psi around Z.
    #
    #   For more information see:
    #   http://www.x-io.co.uk/node/8#quaternions
    #
    #   Date          Author          Notes
    #   27/09/2011    SOH Madgwick    Initial release
    #	25/11/2017	  Billy Phillips  MATLAB to Python

    ##
    # @brief Converts a rotation matrix orientation to ZYX Euler angles where phi is
    # a rotation around X, theta around Y and psi around Z.
    # @param R A rotation matrix of size 3 by 3
    # @return euler A list of size 3 of the resulting ZYX Euler angles.
    def rotMat2euler(self, R):
        phi = np.arctan2(R[2][1], R[2][2])
        theta = -np.arctan(R[2][0] / np.sqrt(1 - R[2][0] ** 2))
        psi = np.arctan2(R[1][0], R[0][0])

        euler = [phi, theta, psi]

        return euler

    # ROTMAT2QUATERN Converts a rotation matrix orientation to a quaternion
    #
    #   q = rotMat2quatern(R)
    #
    #   Converts a rotation matrix orientation to a quaternion.
    #
    #   For more information see:
    #   http://www.x-io.co.uk/node/8#quaternions
    #
    #	Date          Author          Notes
    #	27/09/2011    SOH Madgwick    Initial release
    #	25/11/2017	  Billy Phillips  MATLAB to Python

    ##
    # @brief Converts a rotation matrix orientation to a quaternion.
    # @param R A rotation matrix of size 3 by 3
    # @return q A list of size 4 of the resulting quaternion.
    def rotMat2quatern(self, R):
        K = [[0] * 4] * 4

        K0 = [0] * 4
        K1 = [0] * 4
        K2 = [0] * 4
        K3 = [0] * 4

        K0[0] = (1 / 3) * (R[0][0] - R[1][1] - R[2][2])
        K0[2] = (1 / 3) * (R[2][0] + R[0][2])
        K0[3] = (1 / 3) * (R[1][2] - R[2][1])
        K0[1] = (1 / 3) * (R[1][0] + R[0][1])
        K1[0] = (1 / 3) * (R[1][0] + R[0][1])
        K1[1] = (1 / 3) * (R[1][1] - R[0][0] - R[2][2])
        K1[2] = (1 / 3) * (R[2][1] + R[1][2])
        K1[3] = (1 / 3) * (R[2][0] - R[0][2])
        K2[0] = (1 / 3) * (R[2][0] + R[0][2])
        K2[1] = (1 / 3) * (R[2][1] + R[1][2])
        K2[2] = (1 / 3) * (R[2][2] - R[0][0] - R[1][1])
        K2[3] = (1 / 3) * (R[0][1] - R[1][0])
        K3[0] = (1 / 3) * (R[1][2] - R[2][1])
        K3[1] = (1 / 3) * (R[2][0] - R[0][2])
        K3[2] = (1 / 3) * (R[0][1] - R[1][0])
        K3[3] = (1 / 3) * (R[0][0] + R[1][1] + R[2][2])

        K = np.array([K0, K1, K2, K3])

        # print("look her fucker")
        # print(K)
        D, V = np.linalg.eig(K)
        # print("this is d")
        # print(D)
        # print("")
        # print("")
        # print("this is V")
        # print(V)
        q = [-V[3][1], -V[0][1], -V[1][1], -V[2][1]]

        return q

    ##
    # @brief Takes the transpose of a 3 by 3 rotation matrix.
    # @param R A rotation matrix of size 3 by 3
    # @return R A list of size 3 by 3 of the resulting transposed rotation matrix.
    def matlabTranspos(self, R):
        Rout = np.array([[R[0][0], R[1][0], R[2][0]],
                         [R[0][1], R[1][1], R[2][1]],
                         [R[0][2], R[1][2], R[2][2]]])
        return Rout



