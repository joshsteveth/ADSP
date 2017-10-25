import scipy.io.wavfile as wavfile
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl

#part played determines how much the audio should be played
#e.g. 0.5 means that only 50% of the duration will be played
def playFile(audio, samplingRate, channels, partPlayed=1.0, printText=''):
    p = pyaudio.PyAudio()

    # open audio stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=samplingRate,
                    output=True)

    #recreate new audio based on part played
    #does not have to do anything if value is invalid
    #valid value only between 0.0 and 1.0
    if 0.0 < partPlayed < 1.0:
    	newLength = int(np.floor(partPlayed * len(audio)))
    	newAudio = np.zeros((newLength, channels))

    	for chan in range(0, channels):
    		newAudio[:newLength, chan] = audio[:newLength,chan]
    else:
    	newAudio = audio

    # play. May repeat with different volume values (if done interactively)
    sound = (newAudio.astype(np.int16).tostring())

    #print something before playing
    #if printText is not empty
    if printText != '':
    	print printText
    	
    stream.write(sound)

    # close stream and terminate audio object
    stream.stop_stream()
    stream.close()
    p.terminate()
    return
