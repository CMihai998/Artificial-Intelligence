from random import random

import numpy
from copy import deepcopy

from texttable import Texttable


class Ant:
    def __init__(self, size):
        self._size = size
        self._representation = [[] for i in range(size * 2)]
        self._graph = [self._representation]
        self._freeSpots = size - 1

    def getFreeSpotsCount(self):
        return self._freeSpots

    def getRepresentation(self):
        return self._representation

    def getGraph(self):
        return self._graph[:]

    def setRepresentation(self, newRepresentation):
        if len(self._representation[-1]) > len(newRepresentation[-1]):
            self.decreaseFreeSpots()
        self._representation = deepcopy(newRepresentation)

    def decreaseFreeSpots(self):
        self._freeSpots -= 1

    def nextPossibilities(self):
        possibilities = []
        for i in range(self._size * 2 * (self._freeSpots)):
            newPossibility = deepcopy(self._representation)
            for row in range(self._size * 2):
                possibleNumbers = [i for i in range(1, self._size + 1)]
                for elem in self._representation[row]:
                    possibleNumbers.remove(elem)

                # if row >= self._size and newPossibility[row - self._size][-1] in possibleNumbers:
                #     possibleNumbers.remove(newPossibility[row - self._size][-1])

                choice = numpy.random.choice(possibleNumbers)
                newPossibility[row].append(choice)
                possibleNumbers.remove(choice)
            possibilities.append(newPossibility)
        return possibilities

    def move(self, q0, trace, alpha, beta):
        nextPossibilities = self.nextPossibilities()
        distances = []
        if len(nextPossibilities) == 0:
            return False

        auxAnt = Ant(self._size)
        for position in nextPossibilities:
            auxAnt.setRepresentation(position)
            distances.append([position, auxAnt.fitness() - self.fitness()])

        for i in range(len(distances)):
            index = [0, False]
            while index[0] < len(trace) or index[1]:
                if trace[index[0]] == distances[i][0]:
                    index[1] = True
                index[0] += 1
            if index[1]:
                distances[i][1] = (distances[i][1] ** beta) * (trace(index[0]) ** alpha)

        if numpy.random.random() < q0:
            distances = min(distances, key=lambda elem:elem[1])
            self.setRepresentation(distances[0])
            self._graph.append(self._representation)
        else:
            suma = 0
            for elem in distances:
                suma += elem[1]
            if suma == 0:
                choice = numpy.random.randint(0, len(distances))
                self.setRepresentation(distances[choice][0])
                self._graph.append(self._representation)
                return
            distances = [[distances[i][0], distances[i][1] / suma] for i in range(len(distances))]

            for i in range(len(distances)):
                sum = 0
                for j in range(i+1):
                    sum += distances[j][1]
                distances[i][1] = sum

            choice = numpy.random.random()
            i = 0
            while choice > distances[i][1]:
                i += 1
            self.setRepresentation(distances[i][0])
            self._graph.append(self._representation)
        return True

    def __str__(self):
        table = Texttable()
        for i in range(self._size):
           row = []
           for j in range(len(self._representation[i])):
              row.append((self._representation[i][j], self._representation[i + self._size][j]))
           table.add_row(row)
        return table.draw()

    def fitness(self):
        fitness = 0
        for i in range(self._size):
            for j in range(len(self._representation[i])):
                if self._representation[i][j] == self._representation[i + self._size][j]:
                    fitness += 1
                if i < len(self._representation[i]) and self._representation[j][i] == self._representation[j + self._size][i]:
                    fitness += 1

        for i in range(self._size - 1):
            for j in range(i + 1, self._size):
                fitness += numpy.count_nonzero(
                    numpy.equal(self._representation[i + self._size], self._representation[j + self._size]))
                fitness += numpy.count_nonzero(numpy.equal(self._representation[i], self._representation[j]))

        for i in range(len(self._representation[-1]) - 1):
            column11 = [self._representation[j][i] for j in range(self._size)]
            column12 = [self._representation[j + self._size][i] for j in range(self._size)]
            for j in range(i + 1, len(self._representation[i])):
                column21 = [self._representation[k][j] for k in range(self._size)]
                column22 = [self._representation[k + self._size][j] for k in range(self._size)]

                fitness += numpy.count_nonzero(numpy.equal(column11, column21))
                fitness += numpy.count_nonzero(numpy.equal(column12, column22))

        return fitness