''' imu.py - Extend this class through inheritance when adding different
imu's.  If the imu needs calibration during initialization, then
add that to the __init__ function inside the extended imu class.
For compliance with the framework, the extended imu class MUST
implement at least the getAllAvalableData function and call the parent __init__
function during its __init__ call
'''

class imu:
    ##
    # @brief Parent class for all imus
    # @param self.hasAccel  Initializes hasAccel to False, used for malfunction check
    # @param self.hasGyro  Initializes hasGyro to False, used for malfunction check
    # @param self.hasMagno  Initializes hasMagno to False, used for malfunction check
    # @param self.XAaccelData  Initializes XAaccelData to 0, used for raw data storage
    # @param self.YAaccelData  Initializes YAaccelData to 0, used for raw data storage
    # @param self.ZAaccelData  Initializes ZAaccelData to 0, used for raw data storage
    # @param self.XRotGyroData  Initializes XRotGyroData to 0, used for raw data storage
    # @param self.YRotGyroData  Initializes YRotGyroData to 0, used for raw data storage
    # @param self.ZRotGyroData  Initializes ZRotGyroData to 0, used for raw data storage
    # @param self.XMagnoData  Initializes XMagnoData to 0, used for raw data storage
    # @param self.YMagnoData  Initializes YMagnoData to 0, used for raw data storage
    # @param self.ZMagnoData  Initializes ZMagnoData to 0, used for raw data storage
    # @param getAllAvalableData  Function that gathers all available data
    # @param allDataAvalable  Stores all all data for getAllAvalableData function
    # @pre The imu must be alive, connected and accepting requests
    # @post allDataAvalable  getAllAvalableData will return allDataAvalable once completed
    def __init__(self):
        self.hasAccel = False
        self.hasGyro = False
        self.hasMagno = False

        self.XAaccelData = 0
        self.YAaccelData = 0
        self.ZAaccelData = 0

        self.XRotGyroData = 0
        self.YRotGyroData = 0
        self.ZRotGyroData = 0

        self.XMagnoData = 0
        self.YMagnoData = 0
        self.ZMagnoData = 0

        self.timeStamp = 0


    ##
    # @brief Returns all available imu data
    # @return allDataAvalable  Returns list of xyz acceleration, gyroscope, and magnetometer
    def getAllAvalableData(self):  # Returns all data available
        allDataAvalable = (self.XAaccelData, self.YAaccelData, self.ZAaccelData, self.XRotGyroData,
                           self.YRotGyroData, self.ZRotGyroData, self.XMagnoData, self.YMagnoData, self.ZMagnoData,
                           self.timeStamp)
        return allDataAvalable

    ##
    # @brief Connects the computer to the imu, and is overwritten by every extended imu class
    # @return None  This function has no return value
    def connect(self):
        return None

    ##
    # @brief Disconnects the computer from the imu, and is overwritten by every extended imu class
    # @return None  This function has no return value
    def disconnect(self):
        return None
