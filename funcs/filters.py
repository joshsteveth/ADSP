import scipy.signal as signal
import numpy as np 

#FIR filter with predefined coeffs
def FIR(x):
	b = [0.3235, 0.2665, 0.2940, 0.2655, 0.3235]
	a = [1.0]

	return signal.lfilter(b,a,x)


# def NobleIdentityDownsampling(x, N, 
# 	B=[0.3235, 0.2665, 0.2940, 0.2655, 0.3235], A=1):
# 	#upsample the filter coefficient B by N
# 	Bu = np.zeros(len(B) * N)
# 	Bu[::N] = B

# 	#filter the signal and then downsample it
# 	y = signal.lfilter(Bu, A, x)
# 	return y[::N]

def NobleIdentityDownsampling(x, N, 
	B=[0.3235, 0.2665, 0.2940, 0.2655, 0.3235], A=1):

	result = np.zeros(len(x) / N)

	#take signal in different phase
	#also use filter (B) in that phase
	#the increment result with that
	for i in range(N):
		b = B[i::N]
		x2 = x[i::N]

		result += signal.lfilter(b, A, x2)

	return result

def NobleIdentityUpsampling(x, N, 
	B=[0.3235, 0.2665, 0.2940, 0.2655, 0.3235], A=1):

	result = np.zeros(len(x) * N)

	#filter the signal with filter(B) in different phase
	#then assign the result accordingly in result
	for i in range(N):
		b = B[i::N]
		y = signal.lfilter(b, A, x)
		result[i::N] = y
	return result

def IIR(x):
	b = [0.256, 0.0512, 0.256]
	a = [1.0, -1.3547, 0.6125]
	return signal.lfilter(b,a,x)

def downSample(signal, factor, filter=FIR):
	s = np.zeros(len(signal))
	s[::factor] = 1.0
	signal = signal * s
	signal = filter(signal)
	return signal[::factor]

# def downSample(signal, factor, filter=FIR):
# 	signal = filter(signal)
# 	return signal[::factor]


def downSampleNoFilter(signal, factor):
	return signal[::factor]

def downSamplePlay(signal, factor, filter=FIR):
	s = (np.arange(0, len(signal)) % factor) == 0
	return filter(signal * s)

def upSample(signal, factor, filter=FIR):
	result = np.zeros(len(signal) * factor)

	for idx,val in enumerate(signal):
		result[idx * factor] = val

	return filter(result)

def upSampleNoFilter(signal, factor):
	result = np.zeros(len(signal) * factor)

	for idx,val in enumerate(signal):
		result[idx * factor] = val

	return result

def toDB(h): return 20 * np.log10(np.abs(h) + 1e-3)

# def downSample(signal, factor,filter=FIR):
# 	return signal[::factor]

# def upSample(signal, factor, filter=FIR):
# 	result = np.zeros(len(signal) * factor)

# 	for idx,val in enumerate(signal):
# 		result[idx * factor] = val

# 	return result


def Remez(x):
	N_f = 32

	# F = [0.0, 0.025, 0.05, 0.1, 0.15, 0.5]
	# A = [0.0, 3.0, 0.0]
	# W = [1.0, 0.5, 1.0]

	# F = [0.0, 0.025, 0.05, 0.08, 0.2, 0.5]
	# A = [3.25, 3.0, 0.0]
	# W = [0.7, 1.0, 1.0]

	F = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5]
	A = [0.0, 3.0, 0.0]
	W = [1.0, 1.0, 1.0]

	# F = [0.0,  0.05, 0.25, 0.5]
	# A = [3.25, 0.0]
	# W = [1.0, 0.1]

	bpass = signal.remez(N_f, F, A, weight=W)

	return signal.lfilter(bpass, 1.0, x)

def noFilter(x): return x