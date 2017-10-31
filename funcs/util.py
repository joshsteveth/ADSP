import numpy as np

#the formula is db = 20. log10(c)
#so c = 10 ^ (db/20)
def calculateC(db):
	return pow(10.0, db/20.0)