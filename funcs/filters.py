import scipy.signal as signal
import numpy as np 

#FIR filter with predefined coeffs
def FIR(x):
	b = [0.3235, 0.2665, 0.2940, 0.2655, 0.3235]
	a = [1.0]

	return signal.lfilter(b,a,x)


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

def downSamplePlay(signal, factor, filter=FIR):
	s = (np.arange(0, len(signal)) % factor) == 0
	return filter(signal * s)

def upSample(signal, factor, filter=FIR):
	result = np.zeros(len(signal) * factor)

	for idx,val in enumerate(signal):
		result[idx * factor] = val

	return filter(result)

def toDB(h): return 20 * np.log10(np.abs(h) + 1e-3)

# def downSample(signal, factor,filter=FIR):
# 	return signal[::factor]

# def upSample(signal, factor, filter=FIR):
# 	result = np.zeros(len(signal) * factor)

# 	for idx,val in enumerate(signal):
# 		result[idx * factor] = val

# 	return result
