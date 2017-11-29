import thread
import time


def print_time(threadName, delay):
	count = 0
	while tcount < 5:
		time.sleep(delay)
		count += 1
		print '%s: %s' % (threadName, time.ctime(time.time()))


		
try:
	thread.start_new_thread(print_time, ("Thread-1", 1, ))
	thread.start_new_thread(print_time, ("Thread-2", 3, ))
except:
	print 'Error: unable to start thread'


while 1:
	pass

