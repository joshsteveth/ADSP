import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np 

#animate 2 diagrams in 2 subplots
#1 is original data and 1 already processed
def animateSubplots(origData, procData, interval=25, repeat=False ):
	fig, (plOrig, plProc) = plt.subplots(2, 1)

	origX, origY = [], []
	procX, procY = [], []

	lnOrig, = plOrig.plot([], [], animated=True)
	lnProc, = plProc.plot([], [], animated=True)

	def init(plot, data, title):
		plot.set_xlim(min(data[0]), max(data[0]))
		plot.set_ylim(min(data[1]), max(data[1]))
		plot.grid(True)
		plot.set_title(title)

	init(plOrig, origData, 'Original Data')
	init(plProc, procData, 'Processed Data')

	# plOrig.set_xlim(min(origData[0]), max(origData[0]))
	# plOrig.set_ylim(min(origData[1]), max(origData[1]))
	# plProc.set_xlim(min(procData[0]), max(procData[0]))
	# plProc.set_ylim(min(procData[1]), max(procData[1]))

	def update(frame):
		frame = int(frame)
		origX.append(origData[0][frame])
		origY.append(origData[1][frame])
		lnOrig.set_data(origX, origY)

		procX.append(procData[0][frame])
		procY.append(procData[1][frame])
		lnProc.set_data(procX, procY)

		return [lnOrig, lnProc]

	ani = animation.FuncAnimation(fig, update, frames=np.arange(len(origData[0])),
		blit=True, interval=interval, repeat=repeat)

	plt.show()