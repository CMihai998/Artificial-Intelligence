from copy import deepcopy

import numpy

from models.ant import Ant


class Controller:
    def __init__(self, antSize, colonySize):
        self._antSize = antSize
        self._colonySize = colonySize
        self._colony = []
        self._trace = []
        self._bestSolution = None

    def epoca(self, alpha, beta, q0, rho):
        self._colony = [Ant(self._antSize) for i in range(self._colonySize)]
        for step in range(self._antSize):
            for ant in self._colony:
                ant.move(q0, self._trace, alpha, beta)

        newTrace = []
        for ant in self._colony:
            if ant.fitness() == 0:
                newTrace.append(1)
            else:
                newTrace.append(1.0 / ant.fitness())

        for i in range(len(self._trace)):
            self._trace[i][1] = (1 - rho) * self._trace[i][1]

        for i in range(self._colonySize):
            index = None
            for j in range(len(self._trace)):
                if self._trace[j][0] == self._colony[i].getRepresentation():
                    index = j

            if index != None:
                self._trace[index][1] += newTrace[i]
            else:
                self._trace.append([deepcopy(self._colony[i].getRepresentation()), newTrace[i]])

        antsEvaluation = [[self._colony[i].fitness(), i] for i in range(self._colonySize)]
        antsEvaluation = min(antsEvaluation, key=lambda elem:elem[0])

        return self._colony[antsEvaluation[1]]

    def ACO(self, allowedIterations, alpha, beta, q0, rho):
        solution = []
        iteration = 1
        while iteration <= allowedIterations:
            solution.append(self.epoca(alpha, beta, q0, rho))
            if self._bestSolution == None or solution[-1].fitness() < self._bestSolution.fitness():
                self._bestSolution = solution[-1]
                print(self._bestSolution)
                print(self._bestSolution.fitness())
                if self._bestSolution.fitness() == 0:
                    return self._bestSolution
            iteration += 1
        return self._bestSolution

    def populationFitness(self):
        return [individual.fitness() for individual in self._colony]

    def mean(self):
        return numpy.mean(self.populationFitness())

    def variance(self):
        mean = self.mean()
        sum = 0
        for fitness in self.populationFitness():
            sum += (fitness - mean) ** 2
        return sum / self._colonySize

    def standardDeviation(self):
        return numpy.sqrt(self.variance())