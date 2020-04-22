import math
from copy import deepcopy

import numpy

from models.Node import Node
from models.Tree import Tree


class Controller:
	def __init__(self):
		self._tree = None

	def getTree(self):
		return self._tree

	def generateTree(self, data):
		attributes = {'L1': 1,
		              'L2': 2,
		              'L3': 3,
		              'L4': 4}
		self._tree = Tree(self.generate(data, attributes))

	def generate(self, data, attributes):
		itemsPerClass = Controller.classCount(data)
		if len(itemsPerClass.keys()) == 1:
			return Node(data[0][0])

		elif len(attributes.keys()) == 0:
			decision = ''
			for key in itemsPerClass:
				decision += key
			print(decision)
			print(attributes.keys())
			return Node(decision)
		else:
			divisions = [[Controller.groupData(data, attributes[label]), label] for label in attributes]
			for pair in divisions:
				pair.append(Controller.entropy(data) - Controller.infoGain(pair[0]))
			divisions.sort(key=lambda e: e[2], reverse=True)
			choice = divisions[0]
			attributes = Controller.updateAttributes(attributes, choice[1])
			separationNode = Node(choice[1])
			if len(attributes.keys()) == 0:
				for row in data:
					separationNode.addChildren(Node(row[0]), row[1])
				return separationNode
			for value in choice[0]:
				separationNode.addChildren(self.generate(choice[0][value], deepcopy(attributes)), value)
			return separationNode

	@staticmethod
	def readData():
		data = []
		with open("data/balance-scale.data", 'r') as file:
			for line in file:
				row = line.strip('\n').split(',')
				row[1], row[2], row[3], row[4] = int(row[1]), int(row[2]), int(row[3]), int(row[4])
				data.append(row)

		numpy.random.shuffle(data)
		return data[:round(len(data)*0.91)], data[round(len(data)*0.91):]

	@staticmethod
	def groupData(data, pivot):
		groups = {}
		for row in data:
			if row[pivot] not in groups.keys():
				groups[row[pivot]] = []

			auxRow = deepcopy(row)
			auxRow.pop(pivot)
			groups[row[pivot]].append(auxRow)
		return groups

	@staticmethod
	def classCount(data):
		result = {}
		for row in data:
			label = row[0]
			if label not in result:
				result[label] = 0
			result[label] += 1
		return result

	@staticmethod
	def entropy(data):
		cc = Controller.classCount(data)
		return -sum(cc[label] / len(data) * math.log(cc[label] / len(data), 2) for label in cc)

	@staticmethod
	def infoGain(groups):
		e = 0
		aux = []
		size = sum(len(groups[key]) for key in groups)
		if size == 0:
			size = 0.0000001
		for value in groups:
			count = len(groups[value])
			auxDivision = Controller.groupData(groups[value], 0)
			eValue = -sum(
				(len(auxDivision[key]) / count) * math.log(len(auxDivision[key]) / count, 2) for key in auxDivision)
			aux.append(eValue)
		i = 0
		for value in groups:
			e += len(groups[value]) / size * aux[i]
			i += 1
		return e

	@staticmethod
	def updateAttributes(attributes, labelToRemove):
		deleted = False
		for key in list(attributes):
			if deleted:
				attributes[key] -= 1
			if key == labelToRemove:
				deleted = True
				del attributes[key]
		return attributes
