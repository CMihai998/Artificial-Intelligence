import math
from copy import deepcopy

from models.individual import Individual
from models.problem import Problem
class Controller:
    def __init__(self, populationSize, individualSize):
        self._problem = Problem(populationSize, individualSize)

    def resize(self, populationSize, individualSize):
        self._problem = Problem(populationSize, individualSize)

    def evolutionaryAlgorithm(self, numberOfIterations):
        result = None
        for i in range(numberOfIterations):
            self._problem.evolvePopulation()
            intermediaryResult = self._problem.evaluateLastPopulationEA()
            if result == None or result[-1] > intermediaryResult[-1]:
                result = intermediaryResult
        return result

    def hillClimb(self, individualSize, maximumIterations):
        urAverageGuy = Individual(individualSize)
        theBestYouCanGet = urAverageGuy
        while maximumIterations > 0:
            neighborhood = urAverageGuy.neighbors()
            for maybeBetterGuy in neighborhood:
                if maybeBetterGuy.fitness() < urAverageGuy.fitness():
                    urAverageGuy = maybeBetterGuy
            if theBestYouCanGet == urAverageGuy or theBestYouCanGet.fitness() == 0:
                return theBestYouCanGet
            theBestYouCanGet = urAverageGuy
            maximumIterations -= 1
        return theBestYouCanGet

    def particleSwarnOptimisation(self, iterationsAllowed):
        w = 0.3
        c1 = 0.8
        c2 = 0.5
        currentBest = self._problem.getLastIteration().bestIndividual()
        currentIteration = 2
        while currentIteration < iterationsAllowed:
            possibleBest = self._problem.evolvePopulationPSO(w, c1, c2)
            if currentBest[0].fitness() > possibleBest[0].fitness():
                currentBest = deepcopy(possibleBest)
                print(currentBest[0])
                print(currentBest[1])
            if currentBest[0].fitness() == 0:
                return currentBest
            currentIteration += 1
        return currentBest

    def AdamAndEvas(self, fitnessTarget, individualSize):
        Adam = Individual(individualSize)
        bestSoFar = math.inf
        while bestSoFar > fitnessTarget:
            Evas = [Individual(individualSize) for i in range(20)]
            for Eva in Evas:
                children = Adam + Eva
                if children[0].fitness() < Adam.fitness():
                    Adam = deepcopy(children[0])
                elif children[1].fitness() < Adam.fitness():
                    Adam = deepcopy(children[1])
            if Adam.fitness() <= fitnessTarget:
                return Adam