''' imu.py -- Is the parent class for all of the ius and contains all of the
information that is common between them all.
'''


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
# @post allDataAvalable  getAllAvalableData will return allDataAvalable once completed






class imu:

    #Veriables
    def __init__(self):
        # does it have accelerometers, groscopes, magnometers
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

    # Returns all data available
    def getAllAvalableData(self):  # all data
        allDataAvalable = (self.XAaccelData, self.YAaccelData, self.ZAaccelData, self.XRotGyroData,
                           self.YRotGyroData, self.ZRotGyroData, self.XMagnoData, self.YMagnoData, self.ZMagnoData)
        return allDataAvalable