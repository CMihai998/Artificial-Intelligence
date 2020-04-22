from copy import deepcopy
from models.population import Population


class Problem:
    def __init__(self, size, individualSize):
        self._size = size
        self._individualSize = individualSize
        self._initialPopulation = Population(size, individualSize)
        self._graph = [self._initialPopulation]

    def getLastIteration(self):
        return self._graph[-1]

    def evolvePopulation(self):
        newPopulation = self._graph[-1].iterationEA()
        new = Population(self._size, self._individualSize)
        new.setPopulation(newPopulation)
        self._graph.append(deepcopy(new))

    def evolvePopulationPSO(self, w, c1, c2):
        newPopulation = self._graph[-1].iterationPSO(w, c1, c2)
        self._graph.append(deepcopy(newPopulation))
        return newPopulation.bestIndividual()

    def evaluateLastPopulationEA(self):
        mean = self._graph[-1].mean()
        variance = self._graph[-1].variance()
        stdDeviation = self._graph[-1].standardDeviation()
        bestIndividual, fitness = self._graph[-1].bestIndividual()[0], self._graph[-1].bestIndividual()[1]

        return mean, variance, stdDeviation, bestIndividual, fitness

    def evaluateSolutionPSO(self):
        mean = None
        variance = None
        stdDeviation = None
        bestIndividual = None
        fitness = None
        for population in self._graph:
            if fitness == None or fitness > population.bestIndividual()[1]:
                mean = population.mean()
                variance = population.variance()
                stdDeviation = population.variance()
                bestIndividual, fitness = population.bestIndividual()[0], population.bestIndividual()[1]

        return mean, variance, stdDeviation, bestIndividual, fitness