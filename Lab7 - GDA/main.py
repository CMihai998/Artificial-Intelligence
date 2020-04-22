import concurrent.futures
import timeit

import matplotlib.pyplot as plt
import numpy

from controller import Controller


def mainUtil():
	result = []
	for i in range(50):
		c = Controller(300)
		c.GradientDescendAlgorithm(0.000006, 1000)
		result.append(c.testWhatYouHaveDone())
	return result


if __name__ == '__main__':
	start = timeit.default_timer()
	with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
		print('This takes anywhere from 5 to 12 minutes to run (depending on how powerful your machine is).\n\tGo grab some popcorn')
		Q1 = executor.submit(mainUtil)
		Q2 = executor.submit(mainUtil)
		Q3 = executor.submit(mainUtil)
		Q4 = executor.submit(mainUtil)
		Q5 = executor.submit(mainUtil)
		errorList = Q1.result() + Q2.result() + Q3.result() + Q4.result() + Q5.result()
		print('In 250 runs you have achieved:')
		print('\tMaximum Error: ', max(errorList))
		print('\tMinimum Error: ', min(errorList))
		print('\tAverage Error: ', numpy.average(errorList))
		plt.plot(errorList, 'ro')
		plt.show()
	end = timeit.default_timer()
	print('Time: ', (end - start) / 60)