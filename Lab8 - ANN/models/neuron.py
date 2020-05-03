from math import exp

import numpy


def identical(x):
	return x


def dIdentical(x):
	return 1


def ReLU(x):
	return max(0, x)


def dReLU(x):
	if x > 0:
		return 1
	else:
		return 0


def threshold(x):
	if x > 0.2:
		return 1
	return 0


def dThreshold(x):
	# is just to have some function when we train the network
	return 1


def sigmoid(x):
	return (1.0 / (1.0 + exp(-x)))


def dSigmoid(x):
	return x * (1.0 - x)

class Neuron:
	def __init__(self, n, activationFunction):
		self._noOfInputs = n
		self._activationFunction = activationFunction
		self._weights = [numpy.random.random() for i in range(n)]
		self._output = 0.0

	def activate(self, input):
		aux = sum([x * y for x, y in zip(input, self._weights)])
		self._output = self._activationFunction(aux);
		return self._output

	def setWeights(self, newWeights):
		self._weights = newWeights

	def getOutput(self):
		return self._output

	def __str__(self):
		return str(self._weights)
