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
from util import *

#1 
#use two audio signals
#read in the same audio file
#and read another music fragment, 10s long

rateAudio, audio = wav.read('Track48.wav')
audioMusic = audio[:,0]
audioSinging = audio[:,1]

rateSpeech, speech = wav.read('speech.wav')

#change the speech audio file into 10s long only
#the desired new length in s
length = 10
#new number of elements
elemNum = int(length * rateSpeech)
speech = speech[:elemNum]

#print 'Playing speech file'
#playFile(speech, rateSpeech, 1)


#2
#use scalar quantizer 
#mid tread with M=16 (4bits)
#the result should be awful!
bitNum = 4
audioSingingMT = midTread(audioSinging, bitNum)
print 'Audio singing midtread with %dbit' % bitNum
playFile(audioSingingMT, rateAudio, 1)

#3 LBG algorithm
N = 2
M = LBGVectorLength(bitNum)

start_time = time.time()
#cb = iterateCodebook(ts,cb)
#cb = iterate(ts, cb, 0.1)

#normalization
# lenSpeech, lenSinging = getAbsoluteMax(speech), getAbsoluteMax(audioSinging)
# speech = [float(x) / lenSpeech for x in speech]
# audioSinging = [float(x) / lenSinging for x in audioSinging]

ts = generateTupleArray(speech, N)
cb = randomCodebook(audioSinging, M, N)

# f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
# ax1.scatter(*zip(*ts), marker="+")
# ax1.set_title('training set')
# ax2.scatter(*zip(*cb), color="r", marker="^")
# ax2.set_title('Initial random codebook')


# cb = generateNewCodebook(audioSinging, speech, 
# 	bitNum, N, epsilon=0.03)
eps = 0.05
cb, cbs = trainCodebookForPlot(ts, cb, epsilon=eps)


print 'iteration time: ', time.time() - start_time

with open('newCodebookNorm2.txt', 'w') as a:
	pickle.dump(cb, a)

print len(cbs)
f, axarr = plt.subplots(len(cbs), sharex=True)
for idx, val in enumerate(cbs):
	axarr[idx].scatter(*zip(*val))
	axarr[idx].set_title('after %d. iteration' % idx)

# ax3.scatter(*zip(*cb), color="r", marker="^")
# ax3.set_title('Codebook after training with epsilon=%.2f' %eps)
#plt.plot(speech, 'k^')




plt.show()

