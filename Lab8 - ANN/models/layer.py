from models.neuron import *

class Layer:
	def __init__(self, noOfInputs, activationFunction, noOfNeurons):
		self._noOfNeurons = noOfNeurons
		self._neurons = [Neuron(noOfInputs, activationFunction) for i in
		                 range(self._noOfNeurons)]

	def forward(self, input):
		return [neuron.activate(input) for neuron in self._neurons]

	def __str__(self):
		result = ''
		for i in range(self._noOfNeurons):
			result += ' neuron: ' + str(i) + ' ' + str(self._neurons[i]) + '\n'
		return result


class FirstLayer(Layer):
	def __init__(self, noNeurons, bias=False):
		if bias:
			noNeurons += 1
		Layer.__init__(self, 1, identical, noNeurons)
		for neuron in self._neurons:
			neuron.setWeights([1])

	def forward(self, input):
		return [self._neurons[i].activate([input[i]]) for i in range(len(self._neurons))]
