import numpy
import matplotlib.pyplot as plt


from models.network import Network
from models.neuron import *

def readData():
	data = []
	result = []
	with open("data/input.data", 'r') as file:
		index = 0
		for line in file:
			if index % 2 == 0:
				row = line.strip('\n').split(' ')
				row[0], row[1], row[2], row[3], row[4], row[5] = float(row[0]), float(row[1]), float(row[2]), float(
					row[3]), float(row[4]), float(row[5])
				data.append(row)

			index += 1
		numpy.random.shuffle(data)
		for i in range(len(data)):
			result.append([data[i][-1]])
			data[i].pop()
	return data, result

def mainUtil():
	network = Network([5,1,1], identical, dIdentical)
	inputData, outputData = readData()
	errors = []
	iterations = []
	for i in range(1000):
		iterations.append(i)
		error = []
		for j in range(len(inputData)):
			error.append(network.computeLoss(inputData[j], outputData[j])[0])
			network.backwardPropagate(network.computeLoss(inputData[j], outputData[j]), 0.00000001)
		errors.append(sum([(x**0.08) / len(error) for x in error]))
		for j in range(len(inputData)):
			network.feedForward(inputData[j])

	print(str(network))
	plt.plot(iterations, errors, label='loss value vs iteration')
	plt.xlabel('Iterations')
	plt.ylabel('loss function')
	plt.legend()
	plt.show()


if __name__ == '__main__':
	mainUtil()