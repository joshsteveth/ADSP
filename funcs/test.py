from util import *
from vector_quantizer import *
from operator import itemgetter
import time

start_time = time.time()

x1 = (1,2)
x2 = (3,2)

ecldDist = calculateDist(x1,x2)
wanted = 2.0
if ecldDist == wanted:
	print 'result is correct (%.2f)' %ecldDist
else:
	print 'wanted: %.2f get %.2f' %(wanted, ecldDist)

Y = [(1,2), (5,6)]	
X = [(3,2), (4,5), (7,8), (8,9)]


for x in X:
	foo = ()
	for idx, y in enumerate(Y):
		dist = calculateDist(x,y)
		try:
			if foo[1] > dist:
				foo = (idx, dist)
		except:
			foo = (idx, dist)

	print foo

Z = [(4,5), (7,8)]
bar = calculateCodeVector(Z)
print bar

fooz = iterateCodebook(X, Y)
print fooz

# import json

# with open('test.txt', 'w') as a:
# 	a.write(json.dumps(fooz))

import pickle

with open('test2.txt', 'w') as a:
	pickle.dump(fooz, a)

# with open('test.txt', 'r') as a:
# 	foozz = pickle.load(a)

# print foozz

str = [1,2,10,11, 5,6, 9,10, 0,1]

indices = encodeLBG(str, fooz)
print indices
	

print 'time lapsed: ', time.time() - start_time


y1, y2 = (2.0, 5.0), (3.0, 6.0)
print 'epsilon: ', calculateEpsilon(y1,y2)

foo = [(1,2), (2,3)]
print multipleTupleArray(foo, 2)

def foozz(N):
	x = 10
	if x - N < 0: return N
	else: print N;return foozz(N+1)

zzz = foozz(1)
print 'result: ', zzz