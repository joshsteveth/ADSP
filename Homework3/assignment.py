import scipy.io.wavfile as wav
import scipy.signal as signal
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import cv2
import pyaudio
import sys

sys.path.append('../funcs')

from animations import *
from filters import *
from playwav import *

rate, audio = wav.read('sndfile.wav')
audio=audio[:,1]
t = np.arange(len(audio)) / float(rate)

print 'Sampling rate: ', rate
print 'Audio shape: ', audio.shape

w,H = signal.freqz(audio)

#filter and downsample the signal no 8khz
# newSamplingRate = 8000
# downSamplingFactor = rate/newSamplingRate
samplingFactor = 4

rows=500
cols=512
frame=0.0*np.ones((rows,cols,3));
frametxt=frame.copy()

cv2.putText(frame,"f: change filter", (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,128,128))
cv2.putText(frame,"p: play audio file, s: stop", (20,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,128,128))
cv2.putText(frame,"a: animate original and processed signal", (20,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,128,128))
cv2.putText(frame,"d: downsample", (20,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,128,128))
cv2.putText(frame,"u: upsample", (20,250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,128,128))
cv2.putText(frame,"r: reset signal", (20,300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,128,128))
cv2.putText(frame,"i: plot impulse response", (20,350), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,128,128))
cv2.putText(frame,"q: quit", (20,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,128,128))
cv2.imshow("Real time audio reading processing playback framework",frame+frametxt)

activeFilter = FIR 

activeSamplingRate = rate
activeAudio = audio[:]
CHUNK = 1024 * 4

while(True):
	print 'waiting for command'
	k = cv2.waitKey(0)

	if k == ord('f'):
		#switch filter
		if activeFilter == FIR:
			print 'New active filter: IIR'
			activeFilter = IIR
		else: 
			print 'New active filter: FIR'
			activeFilter = FIR
	elif k == ord('p'):
		print 'playing audio file'
		activeFilter, activeSamplingRate, activeAudio = PlayFileChunk(activeAudio, activeSamplingRate, 
			1, CHUNK, samplingFactor = samplingFactor)
	elif k == ord('d'):
		activeSamplingRate = activeSamplingRate / samplingFactor
		activeAudio = downSample(activeAudio, samplingFactor,
			filter = activeFilter)
		print 'downsampling signal to %d sample/s' % activeSamplingRate
	elif k == ord('u'):
		activeSamplingRate = activeSamplingRate * samplingFactor
		activeAudio = upSample(activeAudio, samplingFactor,
			filter = activeFilter)
		print 'upsampling signal to %d sample/s' % activeSamplingRate
	elif k == ord('a'):
		w,H = signal.freqz(audio)
		w2,H2 = signal.freqz(activeAudio)
		animateSubplots([w,toDB(H)], [w2,toDB(H2)], interval=10)

		plt.show()
	elif k == ord('i'):
		limit = 50
		plt.plot(activeAudio[:limit])
		plt.show()
	elif k == ord('r'):
		activeSamplingRate = rate
		activeAudio = audio[:]
	elif k == ord('q'): break


cv2.destroyAllWindows()