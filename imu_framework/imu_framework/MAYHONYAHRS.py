from imu_framework.imu_framework.quatern_tools import quaternion_tools
import numpy as np

qTools = quaternion_tools()


class MahonyAHRS():
    def __init__(self, SamplePeriod=1 / 100,
                 quaternion=[1, 0, 0, 0],
                 Kp=1,
                 Ki=0,
                 eInt=[0, 0, 0]):
        self.SamplePeriod = SamplePeriod
        self.quaternion = quaternion
        self.Kp = Kp
        self.Ki = Ki
        self.eInt = eInt

        self.XAclData = 0
        self.YAclData = 0
        self.ZAclData = 0
        self.XGyrAData = 0
        self.YGyrAData = 0
        self.ZGyrAData = 0
        self.XMagData = 0
        self.YMagData = 0
        self.ZMagData = 0

        self.AclData = [self.XAclData, self.YAclData, self.ZAclData]
        self.GyrData = [self.XGyrAData, self.YGyrAData, self.ZGyrAData]
        # self.MagData = [self.XMagAData, self.YMagAData, self.ZMagAData]

        # self.XAclDataNorm = 0
        # self.YAclDataNorm = 0
        # self.ZAclDataNorm = 0
        # self.XGyrADataNorm = 0
        # self.YGyrADataNorm = 0
        # self.ZGyrADataNorm = 0
        # self.XMagDataNorm = 0
        # self.YMagDataNorm = 0
        # self.ZMagDataNorm = 0
        #
        # self.AclDataNorm = [self.XAclDataNorm, self.YAclDataNorm, self.ZAclDataNorm]
        # self.GyrDataNorm = [self.XGyrADataNorm, self.YGyrADataNorm, self.ZGyrADataNorm]
        # self.MagDataNorm = [self.XMagADataNorm, self.YMagADataNorm, self.ZMagADataNorm]

        self.AclDataNorm = [0, 0, 0]
        self.GyrDataUpdata = [0, 0, 0]
        self.MagDataNorm = [0, 0, 0]

    def quat(self):
        output = self.quaternion
        return output

    def update(self, XAclData,
               YAclData,
               ZAclData,
               XGyrAData,
               YGyrAData,
               ZGyrAData,
               XMagData=0,
               YMagData=0,
               ZMagData=0
               ):
        self.XAclData = XAclData
        self.YAclData = YAclData
        self.ZAclData = ZAclData
        self.XGyrAData = XGyrAData
        self.YGyrAData = YGyrAData
        self.ZGyrAData = ZGyrAData
        self.XMagData = XMagData
        self.YMagData = YMagData
        self.ZMagData = ZMagData

        self.AclData = [self.XAclData, self.YAclData, self.ZAclData]
        self.GyrData = [self.XGyrAData, self.YGyrAData, self.ZGyrAData]

        # Normalise self.AclData measurement
        if (np.linalg.norm(self.AclData) != 0):
            q = self.quaternion

            self.AclDataNorm = self.AclData / np.linalg.norm(self.AclData)  # normalise magnitude

            # Estimated direction of gravity and magnetic flux
            v = [2 * (q[1] * q[3] - q[0] * q[2]),
                 2 * (q[0] * q[1] + q[2] * q[3]),
                 q[0] ** 2 - q[1] ** 2 - q[2] ** 2 + q[3] ** 2]

            # Error is sum of cross product between estimated direction and measured direction of field
            e = np.cross(self.AclDataNorm, v)
            if (self.Ki > 0):
                self.eInt = self.eInt + e * self.SamplePeriod
            else:
                self.eInt = [0, 0, 0]

            # Apply feedback terms
            temp_GyroData = np.array(self.GyrData)

            feedbackTerms_e = e * self.Kp
            feedbackTerms_eInt = self.eInt * self.Kp

            feedbackTerms = [feedbackTerms_e[0] + feedbackTerms_eInt[0],
                             feedbackTerms_e[1] + feedbackTerms_eInt[1],
                             feedbackTerms_e[2] + feedbackTerms_eInt[2]]

            self.GyrDataUpdata = [temp_GyroData[0] + feedbackTerms[0],
                                  temp_GyroData[1] + feedbackTerms[1],
                                  temp_GyroData[2] + feedbackTerms[2]]

            # Compute rate of change of quaternion
            inputQDot = [0, self.GyrDataUpdata[0], self.GyrDataUpdata[1], self.GyrDataUpdata[2]]
            qDot = qTools.quaternProd(q, inputQDot)
            qDot = np.array(qDot)
            qDot = qDot * 0.5
            # qDot = 0.5 * qTools.quaternProd(q, inputQDot)

            # Integrate to yield quaternion
            q = q + qDot * self.SamplePeriod
            self.quaternion = q / np.linalg.norm(q)  # normalise quaternion
