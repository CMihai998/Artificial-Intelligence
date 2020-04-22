from copy import deepcopy
import concurrent.futures
import numpy
from models.individual import Individual
from scipy.spatial import distance

class Population:
    def __init__(self, size, individualSize):
        self._size = size
        self._indiviualSize = individualSize
        self._population = [Individual(individualSize) for i in range(size)]
        self._bestIndividual = self.bestIndividual()

    def setPopulation(self, newPopulation):
        self._population = deepcopy(newPopulation)

    def getPopulation(self):
        return self._population[:]

    def getIndividualSize(self):
        return self._indiviualSize

    def getSize(self):
        return self._size



    def getDifferentParents(self, limit):
        mother = numpy.random.randint(0, limit)
        father = numpy.random.randint(0, limit)
        while father == mother:
            father = numpy.random.randint(0, limit)
        return mother, father

    def populationUtility(self, population):
        populationClone = deepcopy(population)
        nextGeneration = []
        while len(populationClone) > 1:
            parents = self.getDifferentParents(len(populationClone))
            mother = populationClone[parents[0]]
            father = populationClone[parents[1]]
            children = mother + father
            children[0].mutate()
            children[1].mutate()
            nextGeneration.append(deepcopy(children[0]))
            nextGeneration.append(deepcopy(children[1]))
            populationClone.remove(mother)
            populationClone.remove(father)
        return nextGeneration

    def iterationEA(self):
        numpy.random.shuffle(self._population)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            Q1 = executor.submit(self.populationUtility, self._population[:round(self._size / 4)])
            Q2 = executor.submit(self.populationUtility, self._population[round(self._size / 4) + 1: round(self._size / 2)])
            Q3 = executor.submit(self.populationUtility, self._population[round(self._size / 2) + 1:round(self._size / 2) + round(self._size / 4)])
            Q4 = executor.submit(self.populationUtility, self._population[round(self._size / 2) + round(self._size / 4) + 1:])
            return Q1.result() + Q2.result() + Q3.result() + Q4.result()

    def iterationPSO(self, w, c1, c2):
        for individual in self._population:
            individual.relocate()

        bestNeighbors = []
        for individual in self._population:
            bestNeighbors.append(self.bestOne(self.neighbors(individual)))


        for i in range(self._size):
            currentVelocity = self._population[i].getVelocity()
            newVelocity = []

            for j in range(len(currentVelocity)):
                newPermutation = []
                random1 = numpy.random.random()
                random2 = numpy.random.random()
                for k in range(len(currentVelocity[j])):
                    element = w * currentVelocity[j][k]
                    element += c1 * random1 * (bestNeighbors[i].getVelocity()[j][k] - currentVelocity[j][k])
                    element += c2 *  random2 * (self._bestIndividual[0].getVelocity()[j][k] - currentVelocity[j][k])

                    newPermutation.append(element)
                newVelocity.append(newPermutation)
            self._population[i].setVelocity(newVelocity)

        for i in range(self._size):
            currentPosition = self._population[i].getChromosome()
            currentVelocity = self._population[i].getVelocity()
            newPosition = []
            for k in range(len(currentPosition)):
                newPosition.append((currentPosition[k] + currentVelocity[k]))

            for j in range(len(newPosition)):
                for k in range(len(newPosition[j])):
                    newPosition[j][k] = int(round(newPosition[j][k]))
                    if newPosition[j][k] < 1:
                        newPosition[j][k] = 1
                    if newPosition[j][k] > self._indiviualSize:
                        newPosition[j][k] = self._indiviualSize
            self._population[i].setChromosome(newPosition)

        self._bestIndividual = self.bestIndividual()
        return deepcopy(self)

    def getIndividualIndex(self, individual):
        for i in range(self._size):
            if individual == self._population[i]:
                return i

    def distance(self, X, Y):
        dist = 0
        for i in range(len(X)):
            dist += distance.euclidean(X[i], Y[i])
        return dist

    def neighbors(self, individual):
        neighbors = []
        for element in self._population:
            if element != individual:
                neighbors.append((element, self.distance(individual.getChromosome(), element.getChromosome())))

        neighbors.sort(key=lambda elem: elem[1])
        return neighbors[:10]




    def bestOne(self, group):
        chosenOne = deepcopy(group[0][0])
        for i in range(1, len(group)):
            if chosenOne.fitness() > group[i][0].fitness():
                chosenOne = deepcopy(group[i][0])
        return chosenOne

    def populationFitness(self):
        return [individual.fitness() for individual in self._population]

    def mean(self):
        return numpy.mean(self.populationFitness())

    def variance(self):
        mean = self.mean()
        sum = 0
        for fitness in self.populationFitness():
            sum += (fitness - mean) ** 2
        return sum / self._size

    def standardDeviation(self):
        return numpy.sqrt(self.variance())

    def bestIndividual(self):
        bestIndividual = None
        for individual in self._population:
            if bestIndividual == None or bestIndividual[1] > individual.fitness():
                bestIndividual = (deepcopy(individual), individual.fitness())
        return bestIndividual