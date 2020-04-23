from models.layer import Layer

LEARNING_RATE = 0.00000001

class Network:
	def __init__(self, noInputs, noOutputs):
		self._noInputs = noInputs
		self._noOutputs = noOutputs
		self._noHiddenLayers = 1
		self._noHiddenNeurons = 1

		layers = [Layer(noInputs, 0)]
		layers.append(Layer(self._noHiddenNeurons, noInputs))
		layers.append(Layer(noOutputs, self._noHiddenNeurons))

		self._layers = layers[:]

	def __str__(self):
		result = ''
		for i in range(1, len(self._layers) - 1):
			result = result + "\tLayer " + str(i) + ":\n" + str(self._layers[i])
		result = result + '\tOutput Layer:\n' + str(self._layers[-1])
		return result

	def getError(self, expectedValue):
		return self._layers[-1].getNeuron(0).getOutput() - expectedValue

	def feedForward(self, data):
		for i in range(self._noInputs):
			self._layers[0].getNeuron(i).setOutput(data[i])

		for i in range(self._layers[1].getLayerSize()):
			self._layers[1].getNeuron(i).activate([neuron.getOutput() for neuron in self._layers[0].getNeurons()])

		for i in range(self._layers[-1].getLayerSize()):
			self._layers[-1].getNeuron(i).activate([neuron.getOutput() for neuron in self._layers[1].getNeurons()])

	def propagateErrorBackward(self, error):
		self._layers[-1].getNeuron(0).setError(error)
		for n in range(self._layers[1].getLayerSize()):
			self._layers[1].getNeuron(n).setError(sum([self._layers[1].getNeuron(n).getWeight(i) * error for i in
			                                           range(self._layers[1].getNeuron(n).getNoInputs())]))

	def modifyWeights(self):
		for s in range(self._layers[1].getNeuron(0).getNoInputs()):
			self._layers[1].getNeuron(0).setWeight(s, self._layers[1].getNeuron(0).getWeight(s) - (
						LEARNING_RATE * self._layers[1].getNeuron(0).getError() * self._layers[1].getNeuron(0).getOutput()))
		self._layers[-1].getNeuron(0).setWeight(0, self._layers[-1].getNeuron(0).getWeight(0) -
		                LEARNING_RATE * self._layers[-1].getNeuron(0).getError() * self._layers[-1].getNeuron(0).getOutput())
