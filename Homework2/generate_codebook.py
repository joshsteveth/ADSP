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
#audioSingingMT = midTread(audioSinging, bitNum)
#print 'Audio singing midtread with %dbit' % bitNum
#playFile(audioSingingMT, rateAudio, 1, partPlayed=0.25)

#3 LBG algorithm
N = 2

start_time = time.time()
#cb = iterateCodebook(ts,cb)
#cb = iterate(ts, cb, 0.1)
ts = generateTupleArray(speech, N)
cb = generateNewCodebook(audioSinging, speech, 
	bitNum, N, epsilon=0.1)

print 'iteration time: ', time.time() - start_time

with open('newCodebook2.txt', 'w') as a:
	pickle.dump(cb, a)


f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
ax1.scatter(*zip(*cb), color="r", marker="^")
ax2.scatter(*zip(*ts), marker="+")
ax2.scatter(*zip(*cb), color="r", marker="^")
#plt.plot(speech, 'k^')
plt.show()
