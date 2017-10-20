import numpy as np
import struct

def midTread(x, bitNum):
	#stepsize is the range from max to min signal
	#divided by 2 in the power of bit number
	stepSize = (float(max(x)) - float(min(x))) / pow (2, bitNum) 
	#index is simply the actual signal divided by stepsize
	#and for mid tread quantizer it is rounded
	index = np.round(x/stepSize)

	#return the reconstructed signal
	return index * stepSize


def midRise(x, bitNum):
	#stepsize is basically the same as mid tread
	stepSize = (float(max(x)) - float(min(x))) / pow (2, bitNum) 

	#instead of round we use floor
	index = np.floor(x/stepSize)

	#add the half stepsize for the reconstruction
	return index * stepSize + (stepSize/2)

def uLaw(x, bitNum):
	xMax, xMin = float(max(x)), float(min(x))

	u = 255.0

	###mu-Law compression:###
	y=np.sign(x)*(np.log(1+u*np.abs(x/xMax)))/np.log(1 + u)
    
	# ####Quantization, ####
	
	#select which quantizer we want to use
	#use yrek = y if no quantizer is used
	yrek = midTread(y, bitNum)
	#yrek = midRise(y, bit)
	#yrek = y

    #### mu-law expanding function: ###
    #we use: exp(log(256)*yrek)=256^yrek
	samples=np.sign(yrek)*(np.exp(np.log(1 + u)*np.abs(yrek))-1)/u *xMax
    #end signal processing
	samples=np.clip(samples,xMin, xMax)
	return samples

#quantization error between a signal and its quantified signal
#e = quantized value - original value
#use category to define which quantizer is used
def quantificationError(x, xq):
	e = []
	for idx, val in enumerate(x):
		e.append(xq[idx] - val) 

	#also return the average error
	#use the absolute value of the error
	avg = 0.0
	for err in e:
		avg += np.abs(err)

	return e, avg/len(e) 

def getEnergy(x):
	sum = 0.0

	for elem in x:
		sum += elem**2

	return sum

#SNR definition is 10. log10(signal energy / quantization error energy)
def signalToNoiseRatio(x, bitNum, quantizer):
	#first do the quantization on the input signal
	xq = quantizer(x, bitNum)

	#calculate the error
	e, _ = quantificationError(x,xq)

	signalEnergy = getEnergy(xq)
	quantErrEnergy = getEnergy(e)

	return 10 * np.log10(signalEnergy/quantErrEnergy)