import scipy.io.wavfile as wav
import scipy.signal as signal
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pyaudio
import sys

sys.path.append('../funcs')

from animations import *
from filters import *
from playwav import *

rate, audio = wav.read('sndfile.wav')
audio = audio[:,1]

#sampling factor 
N = 4

CHAN = 1

B = [0.3235, 0.2665, 0.2940, 0.2655, 0.3235]
A = 1


#downsample the signal without any filter
# audioDown = audio[::N]

# def noFilter(x): return x

# audioUp = upSample(audioDown, N, filter=noFilter)

# w,H = signal.freqz(audio)
# w_d, H_d = signal.freqz(audioDown)
# w_u, H_u = signal.freqz(audioUp)



# f, axarr = plt.subplots(3, sharex=True)
# axarr[0].plot(w,toDB(H))
# axarr[1].plot(w_d, toDB(H_d))
# axarr[2].plot(w_u, toDB(H_u))
# plt.show()

#aliasing components start at 8000 khz
#so stop band should start at that frequency
# 8000 kHz normalized -> 0.1
N_f = 32

# F = [0.0,  0.05, 0.25, 0.5]
# A = [3.0, 0.0]
# W = [1.0, 0.1]

# F = [0.0, 0.025, 0.05, 0.08, 0.2, 0.5]
# A = [3.25, 3.0, 0.0]
# W = [1.0, 1.0, 1.0]

F2 = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5]
A2 = [0.0, 3.0, 0.0]
W2 = [1.0, 1.0, 1.0]

#bpass = signal.remez(N_f, F, A, weight=W)

bpass2 = signal.remez(N_f, F2, A2, weight=W2)

# s = np.zeros(len(audio))
# s[::N] = 1.0
# audioDown = audio[:] * s
# audioDown = signal.lfilter(bpass, 1.0, audioDown)
# audioDown = audioDown[::N]
#playFile(audioDown, rate/N, 1)


rate = 1

#[freq,resp] = signal.freqz(bpass)
#plt.plot(freq/(2*np.pi) * rate, np.abs(resp))

plt.figure(1)

[freq2,resp2] = signal.freqz(bpass2)
plt.plot(freq2/(2*np.pi) * rate, np.abs(resp2), 'r')

plt.figure(2)
plt.plot(bpass2)

plt.show()



