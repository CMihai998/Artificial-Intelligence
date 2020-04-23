from math import floor

import numpy
from texttable import Texttable


class Neuron:
	def __init__(self, n):
		self._noOfInputs = n
		self._weights = [numpy.random.random() for i in range(n)]
		self._output = 0.0
		self._error = 0.0

	def activate(self, input):
		result = sum([input[i] * self._weights[i] for i in range(self._noOfInputs)])
		self._output = result

	def setError(self, newValue):
		self._error = newValue

	def setOutput(self, newValue):
		self._output = newValue

	def setWeight(self, index, newValue):
		self._weights[index] = newValue

	def getError(self):
		return self._error

	def getOutput(self):
		return self._output

	def getWeight(self, index):
		return self._weights[index]

	def getNoInputs(self):
		return self._noOfInputs

	def __str__(self):
		table = Texttable()
		table.set_precision(20)
		table.add_row(self._weights)
		auxRow = []
		outputRow = []
		if self._noOfInputs % 2 == 1:
			for i in range(floor(self._noOfInputs / 2)):
				auxRow.append('\\')
				outputRow.append(' ')
			auxRow.append('|')
			outputRow.append(self._output)
			for i in range(floor(self._noOfInputs / 2)):
				auxRow.append('/')
				outputRow.append(' ')
		else:
			for i in range(floor(self._noOfInputs / 2)):
				auxRow.append('\\')
				outputRow.append(' ')
			outputRow.append(self._output)
			for i in range(floor(self._noOfInputs / 2)):
				auxRow.append('/')
				outputRow.append(' ')
		auxRow2 = ['|' for i in range(self._noOfInputs)]
		table.add_row(auxRow2)
		table.add_row(auxRow)
		table.add_row(outputRow)
		return table.draw()
