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
'''---------------------------------------------'''

'''-----Real-time FIR filtering for ecg2.dat-----'''
data2 = np.loadtxt('ecg2.dat')
fs = 1000
fc = 50
numbers2 = data2[:,1]
numbers2 /= max(numbers2)
fir2 = FIRfilter(fs, fc)
output2 = []
for j in range(0, len(numbers2), 1):
    output2.append(fir2.filtering(numbers2[j]))
'''---------------------------------------------'''

'''----------Plot----------'''
plt.figure(1, figsize=(16, 8))

plt.subplot(221)
plt.xlim(9000, 10000)
plt.plot(numbers)
plt.title("Original ecg1.dat")

plt.subplot(222)
plt.xlim(9000,10000)
plt.plot(output)
plt.title("Filtered ecg1.dat")

plt.subplot(223)
plt.xlim(9000,10000)
plt.plot(numbers2)
plt.title("Original ecg2.dat")

plt.subplot(224)
plt.xlim(9000,10000)
plt.plot(output2)
plt.title("Filtered ecg2.dat")

plt.tight_layout()
plt.savefig("Task2.eps")
plt.show()
'''------------------------'''