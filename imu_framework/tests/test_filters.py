''' test_filters.py - Use this program test the fft filters.

'''

import numpy as np
from imu_framework.tests.context import imu_tools
import pylab as plt



time   = np.linspace(0,10,2000)
signal = np.cos(3*np.pi*time) + np.cos(10*np.pi*time)
signalIN = np.array([signal, 2*signal, 3*signal]).transpose()

myTools = imu_tools(signal.size, deltaT=time[1]-time[0])
cut_signal_tools_10 = myTools.bandPassFilter(signalIN, 8, 11)
cut_signal_tools_3 = myTools.bandPassFilter(signalIN, 1, 5)

plt.subplot(331)
plt.plot(time,signalIN[:,0])
plt.xlim(0,1)
plt.subplot(332)
plt.plot(time,signalIN[:,1])
plt.xlim(0,1)
plt.subplot(333)
plt.plot(time,signalIN[:,2])
plt.xlim(0,1)

plt.subplot(334)
plt.plot(time,cut_signal_tools_10[:,0])
plt.xlim(0,1)
plt.subplot(335)
plt.plot(time,cut_signal_tools_10[:,1])
plt.xlim(0,1)
plt.subplot(336)
plt.plot(time,cut_signal_tools_10[:,2])
plt.xlim(0,1)

plt.subplot(337)
plt.plot(time,cut_signal_tools_3[:,0])
plt.xlim(0,1)
plt.subplot(338)
plt.plot(time,cut_signal_tools_3[:,1])
plt.xlim(0,1)
plt.subplot(339)
plt.plot(time,cut_signal_tools_3[:,2])
plt.xlim(0,1)

plt.show()