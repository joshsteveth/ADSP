import numpy as np
import scipy.io.wavfile as wav
import sys
import matplotlib.pyplot as plt
import pickle
import time
sys.path.append('../funcs')

from quantizer import *
from playwav import *
from vector_quantizer import *

with open('newCodebookNorm.txt', 'r') as a:
	codebook = pickle.load(a)

print 'codebook length: ', len(codebook)

# plt.scatter(*zip(*codebook), color="r", marker="^")
# plt.show()

rateAudio, audio = wav.read('Track48.wav')
audioMusic = audio[:,0]
audioSinging = audio[:,1]

#apply normalization
#lenSinging = getAbsoluteMax(audioSinging)
#audioSinging = [float(x) / lenSinging for x in audioSinging]

#start_time = time.time()
#audioSinging = audioSinging[:300000]

#audioLBG = LBG(audioSinging, codebook, threshold=0.0)

#tuplePerThread = 25000
#audioLBG = LBGMT(audioSinging, codebook, tuplePerThread)
#print 'iteration time: ', time.time() - start_time

#denormalize signal to its original value
# audioLBG = [float(x) * lenSinging for x in audioLBG]

# with open('resultNorm2.txt', 'w') as a:
# 	pickle.dump(audioLBG, a)

# plt.plot(audioLBG)
# plt.show()

with open('resultNorm.txt', 'r') as a:
	audioLBG = pickle.load(a)

print 'playing audio file'
playFile(np.array(audioLBG), rateAudio, 1)