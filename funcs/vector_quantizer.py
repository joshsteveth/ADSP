import numpy as np
import threading
import math

from random import randint
from util import *


#create initial codebook vectors
#use random library for this one in xmin and xmax range
def randomIntCodebook(M, N, xMin, xMax):
	cb = []

	for n in range(0, M):
		tup = []
		for t in range(0,N):
			tup.append(randint(xMin, xMax))

		cb.append(tuple(tup))

	return cb

#use values from data stream x instead of random integer
def randomCodebook(x, M, N):
	ts = generateTupleArray(x,N)

	cb = []
	for n in range(0, M):
		cb.append(ts[randint(0,len(ts))])

	return cb

#calculate new codevector 
#from a list of tuple
#e.g. [(4,5), (7,8)] -> ( (4+7)/2, (5+8)/2  )
def calculateCodeVector(x):	
	if len(x) == 1: return x[0]

	tupleLength = len(x[0])

	temp = []
	for _ in range(0, tupleLength):
		temp.append(0.0)

	for val in x:
		for idx, val2 in enumerate(val):
			temp[idx] += float(val2)

	return tuple([val/len(x) for val in temp])

#1 iteration function
#ts is the training data and y is the current codebook 
def iterateCodebook(ts, y):
	#create empty array according to codebook's length
	#this array will be populated with the training datas 
	#with the least euclidian distance
	temp = []
	for x in range(0, len(y)):
		temp.append([])

	#loop through the training set
	#as well as each codebook
	#put the training set into best matched codebook's index in temp
	for t in ts:
		bestMatch = ()
		for idx, val in enumerate(y):
			dist = calculateDist(t,val)
			
			try:
				if bestMatch[1] > dist:
					bestMatch = (idx, dist)
			except: bestMatch = (idx, dist)

		temp[bestMatch[0]].append(t)			

	#now calculate new codebook
	newY = []
	for idx,val in enumerate(temp):
		#use the old value if val is empty
		if len(val) == 0:
			newY.append(y[idx])
			continue

		newY.append(calculateCodeVector(val))

	return newY

#encode the stream based on the codebook
#result is array of indices
def encodeLBG(str, cb):
	ts = generateTupleArray(str, len(cb[0]))

	indices = []

	threshold = 60.0

	#loop through all tuple from data steam
	#calculate best match 
	#best match is the point that has the least distance
	#append indices of the best match to the result
	for t in ts:
		bestMatch = ()
		for idx, val in enumerate(cb):
			dist = calculateDist(t, val)

			if dist <= threshold:
				bestMatch = (idx, dist)
				break

			try:
				if bestMatch[1] > dist:
					bestMatch = (idx,dist)
			except: bestMatch = (idx, dist)

		indices.append(bestMatch[0])

	return indices

#multithreading approach to do LBH
#the principial is exactly the same here
#create new class as subclass of threading.Thread
class encodeThread(threading.Thread):
	def __init__(self, startIndex, dataStream, codebook, indices):
		threading.Thread.__init__(self)
		self.startIndex = startIndex
		self.dataStream = dataStream
		self.codebook = codebook
		self.indices = indices



	def run(self):
		for idx1, t in enumerate(self.dataStream):
			bestMatch = ()
			for idx2, val in enumerate(self.codebook):
				dist = calculateDist(t, val)
				try: 
					if bestMatch[1] > dist:
						bestMatch = (idx2,dist)
				except: bestMatch = (idx2,dist)

			
			try:
				self.indices[self.startIndex + idx1] = bestMatch[0]
			except: continue

#multi threading approach
#in this case M is the number of tuple involved in 1 thread
def encodeLBGMT(str, cb, M):
	strLength = int(math.ceil(len(str)/2.0))
	indices = []
	for i in range(0, strLength):
		indices.append(0)

	threads = []
	threadNum = int(math.ceil(strLength/float(M)))

	vectorStream = generateTupleArray(str, len(cb[0]))

	for i in range(0, threadNum):
		#separate the stream into N parts
		startIndex = i * M
		endIndex = startIndex + M

		try:
			newDS = (vectorStream[startIndex:endIndex])
		except:
			newDS = (vectorStream[startIndex:])

		#initiating the threads
		threads.append(encodeThread(startIndex, newDS, cb, indices))

	#start the threads
	for t in threads: t.start()
	for t in threads: t.join()

	return indices

#decode the indices back to "analog" signal
#simply match the indices to the index in codebook
def decodeLBG(indices, cb):
	strek = []

	for i in indices:
		for val in cb[i]:
			strek.append(val)

	return strek

def LBG(str, cb):
	indices = encodeLBG(str, cb)

	return decodeLBG(indices, cb)

def LBGMT(str, cb, M):
	indices = encodeLBGMT(str, cb, M)
	return decodeLBG(indices, cb)