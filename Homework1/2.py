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

def quantizeWithFilter(fileName, filter, numberOfBits, playAudio=False, channel = 2, printError = True):
	rate, audio = wavfile.read(fileName)
	newAudio = np.zeros(audio.shape)
	newAudio[:,0] = filter(audio[:,0], numberOfBits)
	newAudio[:,1] = filter(audio[:,1], numberOfBits)

	if playAudio == True:
		playFile(newAudio, rate, channel)

	if printError == True:
		error, meanError = quantificationError(audio[:,0], newAudio[:,0])
		print meanError

quantizeWithFilter(filename, midTread, 8, playAudio = False)
quantizeWithFilter(filename, midRise, 8)
quantizeWithFilter(filename, uLaw, 8, playAudio=False)

#ts = np.arange(len(data[:,0])) / float(rate)
# audioMT = data
# audioMT[:,0] = midTread(audioMT[:,0], 8)
# audioMT[:,1] = midTread(audioMT[:,1], 8)
#playFile(audioMT, rate, 2)
# errorMT, meanErrorMT = quantificationError(data[:,0], audioMT[:,0])
# print 'Quantization error for mid tread quantizer: ', meanErrorMT

#norm = audioMT[:,0] / (max(np.amax(audioMT[:,0]), -1 * np.amin(audioMT[:,0])))
#snrMT = stats.signaltonoise(norm)
#print 'SNR for MT: ', snrMT

# audioMR = data
# audioMR[:,0] = midRise(audioMR[:,0], 8)
# audioMR[:,1] = midRise(audioMR[:,1], 8)
#playFile(audioMR, rate, 2)
#errorMR, meanErrorMR = quantificationError(data[:,0], audioMR[:,0])
#print 'Quantization error for mid rise quantizer: ', meanErrorMR

# audioULaw = data
# audioULaw[:,0] = uLaw(audioULaw[:,0], 8)
# audioULaw[:,1] = uLaw(audioULaw[:,1], 8)
# playFile(audioULaw, rate, 2)
#errorULaw, meanErrorULaw = quantificationError(data[:,0], audioULaw[:,0])
#print 'Quantization error for u law quantizer: ', meanErrorULaw

