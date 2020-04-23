import numpy

from models.network import Network


class Controller:
	def __init__(self, trainingDataSize):
		self._data, self._result = self.readData()
		self._trainingDataSize = trainingDataSize
		self._network = Network(5, 1)

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

	def trainNetwork(self, iterationsAllower):
		stop = False
		iteration = 0
		while not stop and iteration < iterationsAllower:
			index = 0
			while not stop and index < self._trainingDataSize:
				self._network.feedForward(self._data[index])
				error = self._network.getError(self._result[index])
				self._network.propagateErrorBackward(error)
				self._network.modifyWeights()
				if error == 0:
					stop = True
				index += 1
			iteration += 1

	def testNetwork(self):
		error = []
		for index in range(self._trainingDataSize, len(self._data)):
			self._network.feedForward(self._data[index])
			error.append(abs(self._network.getError(self._result[index])))
		return numpy.mean(error)