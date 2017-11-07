#compare the snr of the results
#load the normal result from VQ, VQ with normalization, and with mid tread
import pickle
import sys
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
sys.path.append('../funcs')

from quantizer import *

file = 'result3.txt'
fileNorm = 'resultNorm.txt'

_, audio = wav.read('Track48.wav')
audioSinging = audio[:, 1]

with open(file, 'r') as a: result = pickle.load(a)
with open(fileNorm, 'r') as a: resultNorm = pickle.load(a)

snrVQ = snr(audioSinging, result)
print 'snr for %s is %.4f' % (file, snrVQ)
snrVQNorm = snr(audioSinging, resultNorm)
print 'snr for %s is %.4f' % (fileNorm, snrVQNorm)
snrMT = signalToNoiseRatio(audioSinging, 4, midTread)
print 'snr for mid tread is %.4f' % (snrMT)
