import numpy


def linear(x):
	return x


def derivativeLinear(_):
	return 1


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
