import scipy.io.wavfile as wavfile
import scipy.signal as signal
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import cv2
import threading
import sys

from filters import *

#part played determines how much the audio should be played
#e.g. 0.5 means that only 50% of the duration will be played
def playFile(audio, samplingRate, channels, partPlayed=1.0):
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

        if channels > 1:

        	newAudio = np.zeros((newLength, channels))

        	for chan in range(0, channels):
        		newAudio[:newLength, chan] = audio[:newLength,chan]
        else:
            newAudio = audio[:newLength]    
    else:
    	newAudio = audio

    # play. May repeat with different volume values (if done interactively)
    sound = (newAudio.astype(np.int16).tostring())

    stream.write(sound)

    # close stream and terminate audio object
    stream.stop_stream()
    stream.close()
    p.terminate()
    return

def resetStream(p, stream, samplingRate, channels, CHUNK):
    stream.stop_stream()
    stream.close()
    return p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=samplingRate,
                    output=True,
                    frames_per_buffer=CHUNK)


class plotThread(threading.Thread):
    def __init__(self, frame, CHUNK, samplingRate):
        threading.Thread.__init__(self)
        self.frame = frame
        self.CHUNK = CHUNK
        self.samplingRate = samplingRate

    def run(self):
        plt.clf()
        try:
            spec_x = np.fft.fftfreq(self.CHUNK, d = 1.0/self.samplingRate)
            y = np.fft.fft(self.frame)
            spec_y = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in y]
            plt.plot(spec_x, spec_y)
            plt.xlabel("frequency [Hz]")
            plt.ylabel("amplitude spectrum")
            #Pause
            plt.pause(0.1)
        except:
            print 'error while plotting'

class playThread(threading.Thread):
    def __init__(self, stream, sound, CHUNK):
        threading.Thread.__init__(self)
        self.stream = stream
        self.sound = sound
        self.CHUNK = CHUNK

    def run(self):
        self.stream.write(self.sound, self.CHUNK)

def PlayFileChunk(audio, samplingRate, channels, 
        CHUNK, samplingFactor = 4):
    framesNum = len(audio) // CHUNK

    #add options for down/upsampling the signal
    activeFilter = FIR
    activeSampling = 'NA'
    activeSamplingRate = samplingRate
    activeAudio = audio

    print 'active filter = FIR'
    print 'sampling factor: %d' % samplingFactor

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=activeSamplingRate,
                    output=True,
                    frames_per_buffer=CHUNK)

    n = 0

    while(True):
        if (n+2) * CHUNK >= len(activeAudio):
            n = 0
        else: n += 1

        try:
            frame = activeAudio[n * CHUNK : (n+1) * CHUNK]
        except:
            frame = activeAudio[n * CHUNK:]
        sound = (frame.astype(np.int16).tostring())
        

        # stream.write(sound)
        t1 = playThread(stream, sound,CHUNK)
        t1.start();t1.join()

        key=cv2.waitKey(1) & 0xFF;
        if key == ord('f'):
            if activeFilter == FIR:
                print 'New active filter: IIR'
                activeFilter = IIR
            else:
                print 'New active filter: FIR'
                activeFilter = FIR
        elif key == ord('d'): 
            print 'Downsampling audio'
            # activeSampling = 'down'
            activeAudio = downSample(activeAudio[:], samplingFactor, 
                filter=activeFilter)
            activeSamplingRate = activeSamplingRate / samplingFactor
            stream = resetStream(p, stream, activeSamplingRate, 
                channels, CHUNK)
            n = n / samplingFactor
        elif key == ord('u'):
            print 'Upsampling audio'
            # activeSampling = 'up'
            activeAudio = upSample(activeAudio[:], samplingFactor, 
                filter=activeFilter)
            activeSamplingRate = activeSamplingRate * samplingFactor
            stream = resetStream(p, stream, activeSamplingRate, 
                channels, CHUNK)
            n = n * samplingFactor
        elif key == ord('r'):
            print 'Reset to original audio'
            activeAudio = audio[:]
            activeSamplingRate = samplingRate
            stream = resetStream(p, stream, activeSamplingRate, 
                channels, CHUNK)
            n = 0
        elif key == ord('s'):
            print 'Stop playing audio'
            break

        plt.clf()
        try:
            spec_x = np.fft.fftfreq(CHUNK, d = 1.0/activeSamplingRate)
            y = np.fft.fft(frame)
            spec_y = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in y]
            plt.plot(spec_x, spec_y)
            plt.xlabel("frequency [Hz]")
            plt.ylabel("amplitude spectrum")
            #Pause
            plt.pause(.001)
        except ValueError as e:
            print n, "Value error:", e
        except:
            print "Unexpected error:", sys.exc_info()[0]

    plt.clf()
    stream.stop_stream()
    stream.close()
    p.terminate()
    return activeFilter, activeSamplingRate, activeAudio[:]
