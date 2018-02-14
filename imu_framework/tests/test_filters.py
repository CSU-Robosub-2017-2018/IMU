import numpy as np
from scipy.fftpack import rfft, irfft, fftfreq
from imu_framework.tests.context import imu_tools
import pylab as plt



time   = np.linspace(0,10,2000)
signal = np.cos(3*np.pi*time) + np.cos(10*np.pi*time)
signalIN = np.array([signal, 2*signal, 3*signal]).transpose()

# plt.plot(signalIN[:,1])
# plt.show()

myTools = imu_tools(signal.size, deltaT=time[1]-time[0])

cut_signal_tools = myTools.highPassFilter(signalIN,6)

# plt.plot(time, cut_signal_tools[:,0])
# plt.show()
#
# plt.plot(time, cut_signal_tools[:,1])
# plt.show()
#
# plt.plot(time, cut_signal_tools[:,2])
# plt.show()




cut_signal_tools = myTools.lowPassFilter(signalIN,6)

# plt.plot(time, cut_signal_tools[:,0])
# plt.show()
#
# plt.plot(time, cut_signal_tools[:,1])
# plt.show()
#
# plt.plot(time, cut_signal_tools[:,2])
# plt.show()


cut_signal_tools = myTools.bandPassFilter(signalIN, 8, 11)
plt.plot(time, cut_signal_tools[:,0])
plt.show()

plt.plot(time, cut_signal_tools[:,1])
plt.show()

plt.plot(time, cut_signal_tools[:,2])
plt.show()