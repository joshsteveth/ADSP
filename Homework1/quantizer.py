import numpy as np
import struct

def midTread(x, bitNum, xMax=0.0, xMin=0.0):
	#define peak to peak distance
	#if it's lesser or equal 0 then use the min and max value of x instead
	p2p = xMax - xMin
	if p2p <= 0.0:
		p2p = float(max(x)) - float(min(x))

	#stepsize is the range from max to min signal
	#divided by 2 in the power of bit number
	stepSize = p2p / pow (2, bitNum) 
	#index is simply the actual signal divided by stepsize
	#and for mid tread quantizer it is rounded
	index = np.round(x/stepSize)

	#return the reconstructed signal
	return index * stepSize


def midRise(x, bitNum, xMax=0.0, xMin=0.0):
	p2p = xMax - xMin
	if p2p <= 0.0:
		p2p = float(max(x)) - float(min(x))

	#stepsize is basically the same as mid tread
	stepSize = p2p / pow (2, bitNum) 

	#instead of round we use floor
	index = np.floor(x/stepSize)

	#add the half stepsize for the reconstruction
	return index * stepSize + (stepSize/2)

def muLaw(x, bitNum, quantizer=midTread):
	xMax, xMin = float(max(x)), float(min(x))

	mu = 255.0

	###mu-Law compression:###
	y=np.sign(x)*(np.log(1+mu*np.abs(x/xMax)))/np.log(1 + mu)
    
	# ####Quantization, ####
	
	#select which quantizer we want to use
	#use yrek = y if no quantizer is used
	yrek = quantizer(y, bitNum)
	#yrek = midRise(y, bit)
	#yrek = y

    #### mu-law expanding function: ###
    #we use: exp(log(256)*yrek)=256^yrek
	samples=np.sign(yrek)*(np.exp(np.log(1 + mu)*np.abs(yrek))-1)/mu *xMax
    #end signal processing
	return np.clip(samples,xMin, xMax)

def muLawMidRise(x, bitNum):
	return muLaw(x, bitNum, quantizer=midRise)

#quantization error between a signal and its quantified signal
#e = quantized value - original value
#use category to define which quantizer is used
def quantificationError(x, xq, returnMeanError=False):
	e = []
	for idx, val in enumerate(x):
		e.append(xq[idx] - val) 

	#also return the average error
	#use the absolute value of the error
	if returnMeanError:
		return e, float(sum([np.abs(err) for err in e]))/len(e)

	return e

#SNR definition is 10. log10(signal energy / quantization error energy)
def signalToNoiseRatio(x, bitNum, quantizer):
	#first do the quantization on the input signal
	xq = quantizer(x, bitNum)

	#calculate the error
	e = quantificationError(x,xq)

	#signalEnergy = getEnergy(xq)
	#quantErrEnergy = getEnergy(e)
	signalEnergy = sum([x**2 for x in xq])
	quantErrEnergy = sum([x**2 for x in e])

	return 10 * np.log10(signalEnergy/quantErrEnergy)