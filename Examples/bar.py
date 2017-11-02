# def bar():
# 	money = 2.0


# 	def foo(val):
# 		global money
# 		money += val

# 	foo(3.0)


# 	print money


# bar()

def foo():
	x = [[],[]]	
	bar(x, 3.0)
	print x

def bar(y, val):
	y[0].append(val)

foo()
