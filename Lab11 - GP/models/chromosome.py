import math
import random

UNARY_FUNCTIONS = ['sin', 'cos']
BINARY_FUNCTIONS = ['+', '-', '*']

class Chromosome:
    def __init__(self, maxDepth, terminals, functions, constants):
        self._constants = constants
        self._maxDepth = maxDepth
        self._terminals = terminals
        self._functions = functions
        self._fitness = 0
        self._accuracy = 0
        self._size = 0
        self._representation = [0 for i in range(2 ** (maxDepth + 1) - 1)]
        self.generateTree()
        self._representation = [x for x in self._representation if x != 0]

    def generateTree(self, position=0, depth=0):
        if position == 0 or depth < self._maxDepth:
            if position != 0 and random.random() < 0.4:
                self._representation[position] = random.randint(1, len(self._terminals))
                self._size = position + 1
                return position + 1
            else:
                self._representation[position] = -random.randint(1, len(self._functions))
                if self._functions[-self._representation[position] - 1] in ['sin', 'cos']:
                    childIndex = self.generateTree(position + 1, depth + 1)
                    return childIndex
                else:
                    firstBornIndex = self.generateTree(position + 1, depth + 1)
                    secondAirIndex = self.generateTree(firstBornIndex, depth + 1)
                    return secondAirIndex
        else:
            self._representation[position] = random.randint(1, len(self._terminals))
            self._size = position + 1
            return position + 1

    def getFunctionWithIndex(self, index):
        return self._functions[-self._representation[index] - 1]

    def getTerminalWithIndex(self, index):
        return self._terminals[self._representation[index] - 1]

    def evaluateExpression(self, position, data):
        position = min(position, len(self._representation) - 1)

        if self._representation[position] > 0:
            return data[self._representation[position] - 1], position
        elif self._representation[position] < 0:
            currentFunction = self.getFunctionWithIndex(position)
            if currentFunction == '+':
                aux1 = self.evaluateExpression(position + 1, data)
                aux2 = self.evaluateExpression(aux1[1] + 1, data)
                return aux1[0] + aux2[0], aux2[1]
            elif currentFunction == '-':
                aux1 = self.evaluateExpression(position + 1, data)
                aux2 = self.evaluateExpression(aux1[1] + 1, data)
                return aux1[0] - aux2[0], aux2[1]
            elif currentFunction == '*':
                aux1 = self.evaluateExpression(position + 1, data)
                aux2 = self.evaluateExpression(aux1[1] + 1, data)
                return aux1[0] * aux2[0], aux2[1]
            elif currentFunction == 'sin':
                aux = self.evaluateExpression(position + 1, data)
                return math.sin(aux[0]), aux[1]
            elif currentFunction == 'cos':
                aux = self.evaluateExpression(position + 1, data)
                return math.cos(aux[0]), aux[1]

    def computeFitness(self, data, labels):

        def computeOutputClass(row):
            output = self.evaluateExpression(0, row)[0]
            if output < 2:
                return 1
            if output < 4:
                return 2
            if output < 6:
                return 3
            if output < 8:
                return 4
            return 5

        totalError = 0.0
        hit, total = 0, 0
        examplesCount = len(data)

        for index in range(examplesCount):
            error = abs(labels[index] - computeOutputClass(row=data[index]))
            totalError += error
            hit += 1 if error == 0 else 0
            total += 1
        self._accuracy = hit /total
        self._fitness = totalError

    def traverse(self, position):
        if self._representation[position] > 0:
            return min(position + 1, len(self._representation) - 1)
        else:
            return self.traverse(self.traverse(position + 1))

    @property
    def representation(self):
        return self._representation

    @representation.setter
    def representation(self, newRepresentation):
        self._representation = newRepresentation

    def getSize(self):
        return self._size

    def setSize(self, newSize):
        self._size = newSize

    def getFitness(self):
        return self._fitness

    def getAccuracy(self):
        return self._accuracy

    def __str__(self):
        result = ''
        for i, position in enumerate(self._representation):
            if self._representation[position] < 0:
                result += self.getFunctionWithIndex(position) + ' '
            else:
                result += self.getTerminalWithIndex(position) + ' '
        return result

    def __getitem__(self, key):
        return self._representation[key]

    def __setitem__(self, key, value):
        self._representation[key] = value

    def __add__(self, other): # aka crossover
        child = Chromosome(maxDepth=self._maxDepth, terminals=self._terminals, functions=self._functions, constants=self._constants)

        startCutMother = random.randint(0, self._size - 1)
        endCutMother = self.traverse(startCutMother)

        startCutFather = random.randint(0, other.getSize() - 1)
        endCutFather = other.traverse(startCutFather)

        child.representation = [0 for i in range(len(self._representation) + len(other.representation))]

        while len(child.representation) < len(self._representation) + len(other.representation):
            child.representation += [0]
        i = -1
        for i in range(startCutMother):
            child[i] = self[i]
        for j in range(startCutFather, endCutFather):
            i += 1
            child[i] = other[j]
        for j in range(endCutMother, self._size):
            i += 1
            child[i] = self[j]
        child.representation = [x for x in child.representation if x != 0]
        child.setSize(len(child.representation))
        return child

    def mutate(self):
        mutant = Chromosome(maxDepth=self._maxDepth, terminals=self._terminals, functions=self._functions, constants=self._constants)
        position = random.randint(0, self._size - 1)
        mutant.representation = self[:]
        mutant.setSize(self._size)

        if mutant[position] > 0:
            mutant[position] = random.randint(1, len(self._terminals))
        else:
            currentFunction = mutant.getFunctionWithIndex(position)
            if currentFunction in UNARY_FUNCTIONS:
                while True:
                    mutant[position] = -random.randint(1, len(self._functions))
                    newFunction = mutant.getFunctionWithIndex(position)
                    if newFunction in UNARY_FUNCTIONS and newFunction != currentFunction:
                        break
            else:
                while True:
                    mutant[position] = -random.randint(1, len(self._functions))
                    newFunction = mutant.getFunctionWithIndex(position)
                    if newFunction in BINARY_FUNCTIONS and newFunction != currentFunction:
                        break
        return mutant
