import scipy.io.wavfile as wavfile
import scipy.stats as stats
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl

from quantizer import *
from playwav import *

filename = 'Track48.wav'
#rate,data = wavfile.read(filename)

def quantize(fileName, filter, numberOfBits, playAudio=False, channel = 2, printError = True):
	rate, audio = wavfile.read(fileName)
	newAudio = np.zeros(audio.shape)
	# newAudio[:,0] = filter(audio[:,0], numberOfBits)
	# newAudio[:,1] = filter(audio[:,1], numberOfBits)

	#use filter for all channel
	for chan in range(0, channel):
		newAudio[:, chan] = filter(audio[:, chan], numberOfBits)

	if playAudio == True:
		playFile(newAudio, rate, channel)

	if printError == True:
		error, meanError = quantificationError(audio[:,0], newAudio[:,0])
		print 'mean error: ', meanError

		#change the plot config to avoid the overflow error
		#plot the error
		plt.rcParams['agg.path.chunksize'] = 20000
		t = np.arange(len(audio)) / float(rate)
		plt.plot(t, error)
		plt.show()


quantize(filename, midTread, 8, playAudio = False)
#quantize(filename, midRise, 8)
#quantize(filename, muLaw, 8, playAudio=False)

#ts = np.arange(len(data[:,0])) / float(rate)
# audioMT = data
# audioMT[:,0] = midTread(audioMT[:,0], 8)
# audioMT[:,1] = midTread(audioMT[:,1], 8)
#playFile(audioMT, rate, 2)
# errorMT, meanErrorMT = quantificationError(data[:,0], audioMT[:,0])
# print 'Quantization error for mid tread quantizer: ', meanErrorMT

# audioMR = data
# audioMR[:,0] = midRise(audioMR[:,0], 8)
# audioMR[:,1] = midRise(audioMR[:,1], 8)
#playFile(audioMR, rate, 2)
#errorMR, meanErrorMR = quantificationError(data[:,0], audioMR[:,0])
#print 'Quantization error for mid rise quantizer: ', meanErrorMR

# audioMuLaw = data
# audioMuLaw[:,0] = uLaw(audioMuLaw[:,0], 8)
# audioMuLaw[:,1] = uLaw(audioMuLaw[:,1], 8)
# playFile(audioMuLaw, rate, 2)
#errorMuLaw, meanErrorMuLaw = quantificationError(data[:,0], audioMuLaw[:,0])
#print 'Quantization error for u law quantizer: ', meanErrorMuLaw

