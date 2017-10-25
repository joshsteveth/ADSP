import matplotlib.pyplot as plt
import numpy as np


#generate triangle wave based on a time vector
#tmax = the max value of time axis
#fs = the sampling frequency
#f = the triangle signal frequency
def triangleWave(ts, f, Amplitude=1.0):
	#create first the time and amplitude range
	y = np.zeros(ts.shape)

	#period of the triangular wave
	T = 1.0/f

	#define slope of one triangle signal
	#qt is 1/4 of one period
	#it is important since we divide 1 period of tri signal
	#into 4 triangle signals
	qt = T/4
	slope = Amplitude / qt

	#divide the function in 4 cases
	#based on the modulus of period
	for idx, t in enumerate(ts):
		#the rest of the value from the time period
		r = t%T
		#the slope multiplied with r%qt
		#important to determine the position of the point in this time point
		#basically a simple line function
		lr = (r%qt) * slope

		if r < qt:
			val = lr
		elif r < qt * 2:
			val = Amplitude - lr
		elif r < qt * 3:
			val = -lr
		else:
			val = lr - Amplitude

		y[idx] = val

	return y

def triangleWave2(ts, f):
	#create first the time and amplitude range
	y = np.zeros(ts.shape)

	#period of the triangular wave
	T = 1.0/f
	qt = T/2

	#divide the function in 4 cases
	#based on the modulus of period
	for idx, t in enumerate(ts):
		r = t%T
		if r < qt:
			val = 1 - (r / qt)
		else:
			val = ( (r%qt) /qt)

		#y.append(val)
		y[idx] = val

	return y

def triangle(length, amplitude, num):
	section = length // 4
	for n in range(num):
		for direction in (1, -1):
			for i in range(section):
				yield i * (amplitude / section) *  direction
			for  i in range(section):
				yield (amplitude - (i * (amplitude / section))) *direction
