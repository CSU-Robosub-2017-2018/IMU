''' plotting_tools.py - Use this class to plot live x, y, z acceleration data. This function can be modularized to allow
for velocity and positional data.
'''

import time
from collections import deque
from matplotlib import pyplot as plt


class plottingTools():

    ##
    # @brief Initializes the the global variables and sets up a figure with three plots for 3 dimensions of acceptation.
    # @param max_entries The maximum number of entries that are plotted on the graphs
    def __init__(self, max_entries=50):

        fig, axes = plt.subplots(3, 1, sharex=True)

        self.axis_x0 = deque(maxlen=max_entries)
        self.axis_y0 = deque(maxlen=max_entries)

        self.axis_x1 = deque(maxlen=max_entries)
        self.axis_y1 = deque(maxlen=max_entries)

        self.axis_x2 = deque(maxlen=max_entries)
        self.axis_y2 = deque(maxlen=max_entries)

        self.axes = axes
        self.max_entries = max_entries

        self.lineplot0, = axes[0].plot([1], [1], "ro-")
        self.lineplot1, = axes[1].plot([1], [1], "ro-")
        self.lineplot2, = axes[2].plot([1], [1], "ro-")

        self.axes[0].set_autoscaley_on(True)
        self.axes[1].set_autoscaley_on(True)
        self.axes[2].set_autoscaley_on(True)

    ##
    # @brief Updates the previously created graphs with new data.
    # @param time The time or iteration of data
    # @param x The x direction of acceleration
    # @param y The y direction of acceleration
    # @param z The z direction of acceleration
    def add(self, time, x, y, z):
        self.axis_x0.append(time)
        self.axis_y0.append(x)

        self.axis_x1.append(time)
        self.axis_y1.append(y)

        self.axis_x2.append(time)
        self.axis_y2.append(z)

        self.lineplot0.set_data(self.axis_x0, self.axis_y0)
        self.lineplot1.set_data(self.axis_x1, self.axis_y1)
        self.lineplot2.set_data(self.axis_x2, self.axis_y2)

        self.axes[0].set_xlim(self.axis_x0[0], self.axis_x0[-1] + 1e-15)
        self.axes[1].set_xlim(self.axis_x1[0], self.axis_x1[-1] + 1e-15)
        self.axes[2].set_xlim(self.axis_x1[0], self.axis_x1[-1] + 1e-15)

        self.axes[0].relim()
        self.axes[1].relim()
        self.axes[2].relim()

        self.axes[0].autoscale_view()  # rescale the y-axis
        self.axes[1].autoscale_view()  # rescale the y-axis
        self.axes[2].autoscale_view()  # rescale the y-axis

        self.axes[0].set_ylabel('X Accel')
        self.axes[1].set_ylabel('Y Accel')
        self.axes[2].set_ylabel('Z Accel')

        plt.xlabel('time')
        plt.pause(0.1)
