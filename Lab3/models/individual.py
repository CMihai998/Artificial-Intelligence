from copy import deepcopy

import numpy
from texttable import Texttable

class Individual:
    def __init__(self, size):
        self._size = size
        self._chromosome = [numpy.random.permutation([i for i in range(1, size + 1)]) for i in range(size * 2)]
        self._velocity = [[numpy.random.random() * numpy.random.randint(-size + 1, size - 1) for i in range(size)] for i in range(size * 2)]
        self._bestChromosome = deepcopy(self._chromosome)

    def getChromosome(self):
        return self._chromosome[:]

    def getSize(self):
        return self._size

    def setBestChromosome(self, best):
        self._bestChromosome = deepcopy(best)

    def getBestChromosome(self):
        return self._bestChromosome[:]

    def setChromosome(self, newChromosome):
        self._chromosome = newChromosome
        if self.fitness() < self.bestFitness():
            self.setBestChromosome(newChromosome)

    def getVelocity(self):
        return self._velocity[:]

    def setVelocity(self, newVelocity):
        self._velocity = deepcopy(newVelocity)

    def __eq__(self, other):
        for gene1 in self._chromosome:
            for gene2 in other.getChromosome():
                for byte1 in gene1:
                    for byte2 in gene2:
                        if byte1 != byte2:
                            return False
        return True

    def mutate(self):
        probabilityOfMutation = 13
        luck = numpy.random.randint(0, 1000)
        if luck < probabilityOfMutation:
            affectedPart = numpy.random.randint(0, self._size * 2)
            self._chromosome[affectedPart] = numpy.random.permutation(self._chromosome[affectedPart])

    def relocate(self):
        probabilityOfRelocation = 300
        luck = numpy.random.randint(0, 1000)
        if luck < probabilityOfRelocation:
            self.setChromosome([numpy.random.permutation([i for i in range(1, self._size + 1)]) for i in range(self._size * 2)])
            self._velocity = [[numpy.random.random() * numpy.random.randint(-self._size + 1, self._size - 1) for i in range(self._size)] for i in range(self._size * 2)]

    def fitness(self):
        fitness = 0
        for i in range(self._size):
            for j in range(self._size):
                if self._chromosome[i][j] == self._chromosome[i + self._size][j]:
                    fitness += 1
                if self._chromosome[j][i] == self._chromosome[j + self._size][i]:
                    fitness += 1
        for i in range(self._size - 1):
            for j in range(i + 1, self._size):
                fitness += numpy.count_nonzero(numpy.equal( self._chromosome[i + self._size], self._chromosome[j + self._size]))
                fitness += numpy.count_nonzero(numpy.equal( self._chromosome[i], self._chromosome[j]))

        for i in range(self._size - 1):
            column11 = [self._chromosome[j][i] for j in range(self._size)]
            column12 = [self._chromosome[j + self._size][i] for j in range(self._size)]
            for j in range(i + 1, self._size):
                column21 = [self._chromosome[k][j] for k in range(self._size)]
                column22 = [self._chromosome[k + self._size][j] for k in range(self._size)]

                fitness += numpy.count_nonzero(numpy.equal(column11, column21))
                fitness += numpy.count_nonzero(numpy.equal(column12, column22))

        return fitness

    def bestFitness(self):
        fitness = 0
        for i in range(self._size):
            for j in range(self._size):
                if self._bestChromosome[i][j] == self._bestChromosome[i + self._size][j]:
                    fitness += 1
                if self._bestChromosome[j][i] == self._bestChromosome[j + self._size][i]:
                    fitness += 1
        for i in range(self._size - 1):
            for j in range(i + 1, self._size):
                fitness += numpy.count_nonzero(numpy.equal( self._bestChromosome[i + self._size], self._bestChromosome[j + self._size]))
                fitness += numpy.count_nonzero(numpy.equal( self._bestChromosome[i], self._bestChromosome[j]))

        for i in range(self._size - 1):
            column11 = [self._bestChromosome[j][i] for j in range(self._size)]
            column12 = [self._bestChromosome[j + self._size][i] for j in range(self._size)]
            for j in range(i + 1, self._size):
                column21 = [self._bestChromosome[k][j] for k in range(self._size)]
                column22 = [self._bestChromosome[k + self._size][j] for k in range(self._size)]

                fitness += numpy.count_nonzero(numpy.equal(column11, column21))
                fitness += numpy.count_nonzero(numpy.equal(column12, column22))

        return fitness




    def neighbors(self):
        neighbors = []
        for index, permutation in enumerate(self._chromosome):
            for i in range(self._size):
                for j in range(self._size):
                    auxPermutation = deepcopy(permutation)
                    auxPermutation[i], auxPermutation[j] = auxPermutation[j], auxPermutation[i]
                    auxChromosome = deepcopy(self.getChromosome())
                    auxChromosome[index] = auxPermutation
                    neighbor = Individual(self._size)
                    neighbor.setChromosome(auxChromosome)
                    neighbors.append(deepcopy(neighbor))
        return neighbors

    def __add__(self, other):
        mother = other.getChromosome()
        father = self.getChromosome()
        child1 = []
        child2 = []
        cut = numpy.random.randint(1, self._size)
        for element in range(self._size * 2):
            if element % cut == 0:
                child1.append(deepcopy(father[element]))
                child2.append(deepcopy(mother[element]))
            else:
                child1.append(deepcopy(mother[element]))
                child2.append(deepcopy(father[element]))
        offspring1 = Individual(self._size)
        offspring1.setChromosome(deepcopy(child1))
        offspring2 = Individual(self._size)
        offspring2.setChromosome(deepcopy(child2))
        return offspring1, offspring2

    def __str__(self):
        table = Texttable()
        for i in range(self._size):
           row = []
           for j in range(self._size):
              row.append((self._chromosome[i][j], self._chromosome[i + self._size][j]))
           table.add_row(row)
        return table.draw()