import scipy.io.wavfile as wavfile
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl

from util import *
from quantizer import *

filename = 'Track48.wav'
rate,data = wavfile.read(filename)

def playFile(audio, samplingRate, channels):
    p = pyaudio.PyAudio()

    # open audio stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=samplingRate,
                    output=True)
    # play. May repeat with different volume values (if done interactively)

    sound = (audio.astype(np.int16).tostring())
    stream.write(sound)

    # close stream and terminate audio object
    stream.stop_stream()
    stream.close()
    p.terminate()
    return
