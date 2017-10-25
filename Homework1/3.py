import scipy.io.wavfile as wavfile
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

from quantizer import *
from triangle_func import *
from sin_func import *

numBit = 8

#t1,y1 = triangleWave(10.0, 500, 0.25)
fs = 500.0
tmax = 10.0
t1 = np.arange(-1 * tmax, tmax, 1.0/fs)
y1 = triangleWave(t1, 0.25)
snrTri = signalToNoiseRatio(y1, numBit, midTread)
print 'SNR for triangular wave with %dbit mid tread quantizer: %.2f' % (numBit, snrTri)

t2, y2 = sinfunc('f', 1)
snrSin = signalToNoiseRatio(y2, numBit, midTread)
print 'SNR for sinusoidal wave with %dbit mid tread quantizer: %.2f' % (numBit, snrSin)

filename = 'Track48.wav'
rate,data = wavfile.read(filename)
snrAudio = signalToNoiseRatio(data[:,0], numBit, midTread)
print 'SNR for audio file with %dbit mid tread quantizer: %.2f' % (numBit, snrAudio)
