from copy import deepcopy

from models.layer import Layer, FirstLayer

LEARNING_RATE = 0.0000007

class Network:
	def __init__(self, structure, activationFunction, derivate, bias=False):
		self._activationFunction = activationFunction
		self._derivate = derivate
		self._bias = bias
		self._structure = structure[:]
		self._noLayers = len(self._structure)
		self._layers = [FirstLayer(self._structure[0])]
		for i in range(1, len(self._structure)):
			self._layers = self._layers + [Layer(self._structure[i - 1],
			                                   activationFunction, self._structure[i])]

	def feedForward(self, input):
		signal = input[:]
		if self._bias:
			signal.append(1)
		for layer in self._layers:
			signal = layer.forward(signal)
		return signal

	def backwardPropagate(self, loss, learningRate):
		error = loss[:]
		delta = []
		currentLayer = self._noLayers - 1
		newConfiguration = Network(self._structure, self._activationFunction, self._derivate, self._bias)

		for i in range(self._structure[-1]):
			delta.append(error[i] * self._derivate(self._layers[-1]._neurons[i].getOutput()))
			for j in range(self._structure[currentLayer - 1]):
				newConfiguration._layers[-1]._neurons[i]._weights[j] = self._layers[-1]._neurons[i]._weights[j] + \
				                                                       learningRate * delta[i] * \
				                                                       self._layers[currentLayer - 1]._neurons[j].getOutput()

		for currentLayer in range(self._noLayers - 2, 0, -1):
			currentDelta = []
			for i in range(self._structure[currentLayer]):
				currentDelta.append(self._derivate(self._layers[currentLayer]._neurons[i].getOutput()) *
				                    sum([self._layers[currentLayer + 1]._neurons[j]._weights[i] * delta[j]
				                         for j in range(self._structure[currentLayer + 1])]))
		delta = currentDelta[:]
		for i in range(self._structure[currentLayer]):
			for j in range(self._structure[currentLayer - 1]):
				newConfiguration._layers[currentLayer]._neurons[i]._weights[j] = self._layers[currentLayer]._neurons[i]._weights[j] + \
				                                                                 learningRate * delta[i] * self._layers[currentLayer - 1]._neurons[j].getOutput()

		self._layers = deepcopy(newConfiguration._layers)

	def computeLoss(self, data, target):
		loss = []
		result = self.feedForward(data)
		for i in range(len(target)):
			loss.append(target[i] - result[i])
		return loss[:]

	def __str__(self):
		result = ''
		for i in range(1, len(self._layers) - 1):
			result = result + "\tLayer " + str(i) + ":\n" + str(self._layers[i])
		result = result + '\tOutput Layer:\n' + str(self._layers[-1])
		return result
