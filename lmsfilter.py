import numpy as np
import matplotlib.pyplot as plt
#import time
#start = time.time()

'''----------FIR Filter----------'''
class FIRfilter:
    def __init__(self, fs, fc):
        self.fs = fs
        self.M = fs
        self.fc = fc
        self.buffer = []
        self.coeff()


    def coeff(self):
        k1 = int(self.M * (self.fc - 5)/self.fs)
        k2 = int(self.M * (self.fc + 5)/self.fs)
        h = np.ones(self.M)
        h[k1:k2+1] = 0
        h[self.M-k2:self.M-k1+1] = 0
        hf = np.real(np.fft.ifft(h))
        x = np.zeros(self.M)
        x[0:int(self.M/2)] = hf[int(self.M/2):self.M]
        x[int(self.M/2):self.M] = hf[0:int(self.M/2)]
        x[0] = 0
        self.h = x*np.blackman(self.M)


    def filtering(self, data):
        if len(self.buffer) >= self.M:
            self.buffer = np.roll(self.buffer, 1)
            self.buffer[0] = data
            return self.buffer @ self.h
        else:
            self.buffer.append(data)
            return 0
'''---------------------------------'''

'''----------LMS Filter----------'''
class LMSfilter:
    def __init__(self, coeff):
        self.M = len(coeff)
        self.buffer = np.zeros(self.M)
        self.h = coeff


    def filtering(self, data):
        self.buffer = np.roll(self.buffer, 1)
        self.buffer[0] = data
        return self.buffer @ self.h


    def Adaptive(self, error, mu):
            for i in range(self.M):
                self.h[i] = self.h[i] + error * mu * self.buffer[i]
'''---------------------------------'''

'''-----Real-time FIR filtering for ecg1.dat-----'''
data = np.loadtxt('ecg1.dat')
fs = 1000
fc = 50
numbers = data[:,1]
numbers /= max(numbers)
fir = FIRfilter(fs, fc)
output = []
for j in range(0, len(numbers), 1):
    output.append(fir.filtering(numbers[j]))
output /= max(output)
'''---------------------------------------------'''

'''----------LMS filtering-----------'''
data = np.loadtxt('ecg1.dat')
fs = 1000
fc = 50
ntaps = 1000
l_rate = 0.001
numbers = data[:,1]
numbers /= max(numbers)
lms = LMSfilter(np.zeros(ntaps))
output2 = np.zeros(len(numbers))
for j in range(0, len(numbers), 1):
    noise = np.cos(2.0 * np.pi * (fc / fs) * j)
    D = lms.filtering(noise)
    error = numbers[j] - D
    lms.Adaptive(error, l_rate)
    output2[j] = error
output2 /= max(output2)
'''---------------------------------'''

'''----------Plot----------'''
plt.figure(1, figsize=(20, 5))

plt.subplot(131)
plt.plot(numbers)
plt.xlim(10500, 11000)
plt.title("Original ECG")

plt.subplot(132)
plt.plot(output2)
plt.xlim(10500, 11000)
plt.ylim(0.5, 1)
plt.title("LMS Filtered ECG")

plt.subplot(133)
plt.plot(output)
plt.xlim(10400, 10900)
plt.ylim(0.5, 1)
plt.title("FIR Filtered ECG")

plt.tight_layout()
plt.savefig("Task3.eps")
#print(f"time: {time.time() - start}")
plt.show()
'''------------------------'''
