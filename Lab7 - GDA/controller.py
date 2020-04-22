import numpy

from models.neuron import Neuron


class Controller:
	def __init__(self, trainingDataSize):
		data, result = self.readData()
		self._trainingData = data[:trainingDataSize]
		self._trainingResult = result[:trainingDataSize]
		self._predictData = data[trainingDataSize:]
		self._predictResult = result[trainingDataSize:]
		self._neuron = Neuron(5)

	def readData(self):
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
				result.append(data[i][-1])
				data[i].pop()
		return data, result

	def GradientDescendAlgorithm(self, learningRate, iterationsAllowed):
		currentIteration = 0
		while currentIteration < iterationsAllowed:
			deltaWeight = [0 for i in range(self._neuron.getNoInputs() + 1)]
			for index in range(len(self._trainingData)):
				self._neuron.activate(self._trainingData[index])
				for i in range(self._neuron.getNoInputs()):
						deltaWeight[i] += learningRate * (self._neuron.getOutput() - self._trainingResult[index]) * self._trainingData[index][i]
				deltaWeight[-1] += learningRate * (self._neuron.getOutput() - self._trainingResult[index])
			for i in range(self._neuron.getNoInputs()):
				self._neuron.setWeight(i, self._neuron.getWeight(i) - deltaWeight[i])
			self._neuron.setExtraWeight(self._neuron.getExtraWeight() - deltaWeight[-1])
			currentIteration += 1

	def testWhatYouHaveDone(self):
		error = []
		for index in range(len(self._predictData)):
			self._neuron.activate(self._predictData[index])
			error.append(abs(self._neuron.getOutput() - self._predictResult[index]))
		return numpy.mean(error)

	def __str__(self):
		return str(self._neuron)