import numpy as np
import matplotlib.pyplot as plt

#generate sin func with normalized frequenz 0.1
#x axis is the time from -1 to 1
#you can either set the signal frequency f or the sampling frequency fs
#by changing the category argument to 'f' or 'fs'
#then the function will automatically plot the result
def sinfunc(cat, val):
	fn = 0.1

	fs, f = 0.0, 0.0
	if cat == 'f':
		fs, f = val / fn, val
	elif cat == 'fs':
		fs, f = val, val * fn
	else: return

	x = np.arange(-1, 1 + 1.0/fs, 1.0/fs)
	y = np.sin(2 * np.pi * f * x)

	return x,y