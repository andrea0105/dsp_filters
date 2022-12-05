import numpy as np
import matplotlib.pyplot as plt


'''----------FIR Filter----------'''
class FIRfilter:
    def __init__(self, fs, fc):
        self.fs = fs
        self.M = 2*fs
        self.fc = fc
        self.buffer = []
        self.coeff()


    def coeff(self):
        k0 = int(self.M * (0.5)/self.fs)
        k1 = int(self.M * (self.fc - 5)/self.fs)
        k2 = int(self.M * (self.fc + 5)/self.fs)
        k3 = int(self.M * (150)/self.fs)
        h = np.ones(self.M)
        h[0:k0+1] = 0
        h[self.M-k0:self.M+1] = 0
        h[k1:k2+1] = 0
        h[self.M-k2:self.M-k1+1] = 0
        h[k3:self.M-k3+1] = 0
        hf = np.real(np.fft.ifft(h))
        x = np.zeros(self.M)
        x[0:int(self.M/2)] = hf[int(self.M/2):self.M]
        x[int(self.M/2):self.M] = hf[0:int(self.M/2)]
        x[0] = 0
        x[self.M-1] = 0
        self.h = x*np.blackman(self.M)


    def filtering(self, data):
        out = 0
        if len(self.buffer) >= self.M:
            self.buffer = np.roll(self.buffer, 1)
            self.buffer[0] = data
            out = self.buffer @ self.h
            return out
        else:
            self.buffer.append(data)
            return 0
'''---------------------------------'''

'''-----Real-time FIR filtering-----'''
data = np.loadtxt('ecg2.dat')
fs = 1000
fc = 50
numbers = data[:,1]
numbers /= max(numbers)
t = data[:,0]/fs
fir = FIRfilter(fs, fc)
output = []
for j in range(0, len(numbers), 1):
    output.append(fir.filtering(numbers[j]))
output /= max(output)
'''--------------------------------'''

'''----------Heart rate----------'''
template = output[10300:10900]
matched_coeff = template[::-1]
peaks = []
buffer = []
for k in range(0, len(output), 1):
    if output[k] is None:
        peaks.append(0)
    else:
        if len(buffer) >= len(matched_coeff):
            buffer = np.roll(buffer, 1)
            buffer[0] = output[k]
            peaks.append(buffer @ matched_coeff)
        else:
            buffer.append(output[k])
for z in range(len(peaks)):
    peaks[z] = peaks[z]**2
'''------------------------------'''

'''----------Plot----------'''
plt.figure(1, figsize=(10,3))
plt.plot(peaks)
plt.xlim(10000, 15000)
plt.title("Heart Rate Detection")
plt.savefig("Task4.eps")
plt.show()
'''------------------------'''