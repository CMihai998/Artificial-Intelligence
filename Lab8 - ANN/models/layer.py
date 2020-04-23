from texttable import Texttable

from models.neuron import Neuron


class Layer:
	def __init__(self, neuronsCount, neuronSize):
		self._noNeurons = neuronsCount
		self._neurons = [Neuron(neuronSize) for i in range(neuronsCount)]

	def getNeuron(self, index):
		return self._neurons[index]

	def getNeurons(self):
		return self._neurons

	def getLayerSize(self):
		return self._noNeurons

	def __str__(self):
		result = ''
		for neuron in self._neurons:
			auxTable = Texttable()
			auxTable.set_precision(14)
			row = []
			for i in range(neuron.getNoInputs()):
				row.append(neuron.getWeight(i))
			auxTable.add_row(row)
			result = result + auxTable.draw() + '\n\n'
		return result
