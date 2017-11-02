import numpy as np

#the formula is db = 20. log10(c)
#so c = 10 ^ (db/20)
def calculateC(db):
	return pow(10.0, db/20.0)


#calculate a euclidean distance between 2 vectors
#the dimension of x1 and x2 must agree
def calculateDist(x1,x2):
	result = 0.0

	for idx, n in enumerate(x1):
		result += (x1[idx] - x2[idx]) ** 2
	return pow(result, 0.5)


#create the tuple array from an array
#e.g. if N = 2 and training set is [1,2,3,4]
#result is [(1,2), (3,4)]
def generateTupleArray(x, N):
	tuppleNum = len(x) // N
	ts = []

	for n in range(0, tuppleNum):
		#create new list to be modified into a tuple
		tup = []
		for t in range(0, N):
			tup.append(x[n * N + t])

		ts.append(tuple(tup))

	return ts

