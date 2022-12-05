#!/usr/bin/python3
import numpy as np
import pyusbdux as dux
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.signal as signal
import time


class butterworth:
    def __init__(self, fs, f1, f2, type, order, scale):
        self.fs = fs
        self.f1 = f1
        self.f2 = f2
        self.scale = 2**scale
        self.type = type
        self.order = order
        self.array_number = 0
        self.sos = 0

        # Delay Line
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0

        self.coeff()

    def coeff(self):
        if self.type == "lowpass" or self.type == "highpass":
            self.count = 0.5 * self.order - 1
            self.f1 = 2 * self.f1 / self.fs
            self.sos = signal.butter(self.order, self.f1 , self.type, output='sos')

        if self.type == "bandstop" or self.type == "bandpass":
            self.count = self.order - 1
            self.f1 = 2 * self.f1 / self.fs
            self.f2 = 2 * self.f2 / self.fs
            self.sos = signal.butter(self.order, [self.f1, self.f2], self.type, output='sos')

        self.sos *= self.scale
        self.sos = np.round(self.sos)

        self.b1 = self.sos[0][0:3]
        self.a1 = self.sos[0][3:6]

        print(f'Coefficients = {self.sos}')

    def filter(self, v):
        _out1 = 0
        _in1 = v
        _out1 = _in1 * self.b1[0] + self.b1[1] * self.x1 + self.b1[2] * self.x2 - self.a1[1] * self.y1 - self.a1[2] * self.y2
        _out1 /= self.scale
        self.x2 = self.x1
        self.y2 = self.y1
        self.x1 = _in1
        self.y1 = _out1
        if self.array_number == self.count:
            return _out1
        else:
            self.array_number += 1
            self.b1 = self.sos[self.array_number][0:3]
            self.a1 = self.sos[self.array_number][3:6]
            return self.filter(_out1)
        '''---------------------------------------------'''

'''---------------------------------------------'''
class plotting:
    def __init__(self):
        self._high = butterworth(1000, 1, 0, "highpass", 6, 14)
        self._stop = butterworth(1000, 45, 55, "bandstop", 6, 14)
        self._low = butterworth(1000, 499, 0, "lowpass", 6, 14)

        self.fig_1, self.ax_1 = plt.subplots()
        self.plotbuffer_1 = np.zeros(1000)
        self.line_1, = self.ax_1.plot(self.plotbuffer_1)
        self.ax_1.set_ylim(-1, 30)
        self.ax_1.axhline(y=50, xmin=0, xmax=1, c='red', linewidth=0.5, zorder=0)
        self.ringbuffer_1 = []
        self.ax_1.title.set_text('Original Signal')
        self.ani_1 = animation.FuncAnimation(self.fig_1, self.update_1, interval=100)

        self.fig_2, self.ax_2 = plt.subplots()
        self.plotbuffer_2 = np.zeros(1000)
        self.line_2, = self.ax_2.plot(self.plotbuffer_2)
        self.ax_2.set_ylim(-1, 30)
        self.ax_2.axhline(y=50, xmin=0, xmax=1, c='red', linewidth=0.5, zorder=0)
        self.ringbuffer_2 = []
        self.ax_2.title.set_text('Filtered Signal')
        self.ani_2 = animation.FuncAnimation(self.fig_2, self.update_2, interval=100)

        self.fig_3, self.ax_3 = plt.subplots()
        self.plotbuffer_3 = np.zeros(1000)
        self.line_3, = self.ax_3.plot(self.plotbuffer_3)
        self.ax_3.set_ylim(0, 2000)
        self.time = [0]
        self.ringbuffer_3 = []
        self.ax_3.title.set_text('Real-time Sampling rate')
        self.ani_3 = animation.FuncAnimation(self.fig_3, self.update_3, interval=100)

    def update_1(self, data_1):
        self.plotbuffer_1 = np.append(self.plotbuffer_1, self.ringbuffer_1)
        self.plotbuffer_1 = self.plotbuffer_1[-1000:]
        self.ringbuffer_1 = []
        self.line_1.set_ydata(self.plotbuffer_1)
        self.ax_1.title.set_text(f'Original Signal at sapling rate = {1/self.count} Hz')
        return self.line_1,

    def update_2(self, data_2):
        self.plotbuffer_2 = np.append(self.plotbuffer_2, self.ringbuffer_2)
        self.plotbuffer_2 = self.plotbuffer_2[-1000:]
        if np.mean(self.plotbuffer_2) > 50:
            print('muscle activated')
        self.ringbuffer_2 = []
        self.line_2.set_ydata(self.plotbuffer_2)
        self.ax_2.title.set_text(f'Filtered Signal at sapling rate = {1/self.count} Hz')
        return self.line_2,

    def update_3(self, data_3):
        self.plotbuffer_3 = np.append(self.plotbuffer_3, self.ringbuffer_3)
        self.plotbuffer_3 = self.plotbuffer_3[-1000:]
        self.ringbuffer_3 = []
        self.line_3.set_ydata(self.plotbuffer_3)
        return self.line_3,

    def addData(self, v1):
        self.count  = self.stamp()
        self.ringbuffer_1.append(100*(v1**2))
        self.ringbuffer_2.append(100*(self._low.filter(self._high.filter(self._stop.filter(v1)))**2))
        self.ringbuffer_3.append(1 / self.count)
        self.time = [time.time()]

    def stamp(self):
        self.time.append(time.time())
        return (self.time[1] - self.time[0])
'''---------------------------------------------'''

plotting = plotting()

'''---------------------------------------------'''
class DataCallback(dux.Callback):
    def hasSample(self,s):
        plotting.addData(s[0])
'''---------------------------------------------'''

cb = DataCallback()
dux.open()
dux.start(cb,8,1000)

plt.show()

dux.stop()
dux.close()
print("finished")