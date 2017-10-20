from sin_func import *
from triangle_func import *
from util import *
from playwav import *

import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
import numpy as np

#the under full range in db
#calculate c using formula from util.py
underRange = 25
c = calculateC(underRange)

#create 6 subplots
#left side is full range signal and right is under 25db
#share the y axis to compare the amplitude
f,ax = plt.subplots(3,2)

##### TRIANGLE WAVE #####
fs = 500.0
tmax = 10.0
ff = 0.25
t1 = np.arange(0, tmax, 1.0/fs)
# y1 = triangleWave2(t1, ff)

y1 = triangleWave(t1, ff)
ax[0,0].plot(t1,y1, 'k')
ax[0,0].set_title('Triangle full range')

y2 = [x / c for x in y1]
ax[0,1].plot(t1,y1, 'k')
ax[0,1].plot(t1,y2, 'r')
ax[0,1].set_title('Triangle 25db under full range (red)')

##### SIN WAVE #####
t3,y3 = sinfunc('fs', 20)
ax[1,0].stem(t3,y3, 'g', )
ax[1,0].plot(t3,y3, 'k')
ax[1,0].set_title('Sin full range')
y4 = [x / c for x in y3]
ax[1,1].stem(t3,y3, 'g', )
ax[1,1].plot(t3,y3, 'k')
ax[1,1].stem(t3,y4, 'b', )
ax[1,1].plot(t3,y4, 'r')
ax[1,1].set_title('Sin 25db under full range (red)')

##### WAV FILE #####
filename = 'Track48.wav'
rate,audio = wavfile.read(filename)

#create the time axis based on sampling rate
t5 = np.arange(len(audio)) / float(rate)
ax[2,0].fill_between(t5, audio[:,0], audio[:,1], color='k')
ax[2,0].set_title('Track48.wav full range')
audio2 = audio / c
ax[2,1].fill_between(t5, audio[:,0], audio[:,1], color='k')
ax[2,1].fill_between(t5, audio2[:,0], audio2[:,1], color='r')
ax[2,1].set_title('Track48.wav 25db under full range (red)')

plt.show()

#playFile(audio, rate, 2)
#playFile(audio2, rate, 2)