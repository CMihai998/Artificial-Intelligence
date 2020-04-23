import numpy
import matplotlib.pyplot as plt
from controller import Controller
import concurrent.futures
import timeit
def mainUtil():
	result = []
	for i in range(50):
		c = Controller(400)
		c.trainNetwork(100)
		result.append(c.testNetwork())
	return result

if __name__ == '__main__':
	start = timeit.default_timer()
	with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
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