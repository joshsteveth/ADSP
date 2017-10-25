import scipy.io.wavfile as wavfile
import scipy.stats as stats
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl

from quantizer import *
from playwav import *

filename = 'Track48.wav'
rate,data = wavfile.read(filename)

def quantize(samplingRate, audio, quantizer, numberOfBits):
	newAudio = np.zeros(audio.shape)

	#use quantizer for all channel
	for chan in range(0, audio.shape[1]):
		newAudio[:, chan] = quantizer(audio[:, chan], numberOfBits)

	return newAudio

mtAudio = quantize(rate, data, midTread, 8)
mrAudio = quantize(rate, data, midRise, 8)
muLawAudio = quantize(rate, data, muLaw, 8)

playFile(mtAudio, rate, 2, partPlayed=0.25, 
	printText='playing mid tread quantized audio')
playFile(mrAudio, rate, 2, partPlayed=0.25,
	printText='playing mid rise quantized audio')
playFile(muLawAudio, rate, 2, partPlayed=0.25,
	printText='playing mu law (mid tread) quantized audio')

#### ERROR PLOT ####
#get the error only for the first channel
mtError, _ = quantificationError(data[:,0], mtAudio[:,0])
mrError, _ = quantificationError(data[:,0], mrAudio[:,0])
muLawError, _ = quantificationError(data[:,0], muLawAudio[:,0])

#create the time vector
t = np.arange(len(data)) / float(rate)

#change the default value 
#to avoid overflow while plotting
plt.rcParams['agg.path.chunksize'] = 20000

f, ax = plt.subplots(3, sharex=True)
f.suptitle('Quantization Errors')
ax[0].plot(t, mtError)
ax[0].set_title('Mid Tread')
ax[1].plot(t, mrError)
ax[1].set_title('Mid Rise')
ax[2].plot(t,muLawError)
ax[2].set_title('Mu Law')
ax[2].set_xlabel('time[s]')
plt.show()

