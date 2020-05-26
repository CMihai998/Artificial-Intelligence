from functools import reduce
from math import floor
from random import seed

import numpy

from fileWriter import FileWriter
from models.chromosome import Chromosome

MAX_DEPTH = 7
TERMINALS = ['-165', '-150', '-135', '-120', '-105', '-90', '-75',
             '-60', '-45', '-30', '-15', '0', '15', '30', '45', '60', '75',
             '90', '105', '120', '135', '150', '165']
FUNCTIONS = ['+', '-', '*', 'sin', 'cos']
UNARY_FUNCTIONS = ['sin', 'cos']
BINARY_FUNCTIONS = ['+', '-', '*']
CONSTANTS = []
CLASSES = {
    'Slight-Left-Turn':     0,
    'Move-Forward':         1,
    'Slight-Right-Turn':    2,
    'Sharp-Right-Turn':     3
}

def geneticSearch(data, labels, populationSize=1000, replacePerGenerationPercentage=0.2, tournamentPercentage=0.05, mutationChance=0.1, epsilon=0.65):
    data = [row + CONSTANTS for row in data]
    fileWriter = FileWriter.getFileWriter()
    seed(None)
    fileWriter.write("Generating everythin, might take a while :'(")

    individuals = [Chromosome(MAX_DEPTH, TERMINALS, FUNCTIONS, CONSTANTS) for i in range(populationSize)]
    for individual in individuals:
        individual.computeFitness(data=data, labels=labels)

    alphaIndividual = None
    tournamentSize = int(floor(populationSize * tournamentPercentage))
    populationReplacement = int(floor(populationSize * replacePerGenerationPercentage))

    fitter = lambda pretender1, pretender2: pretender1 if pretender1.getFitness() < pretender2.getFitness() else pretender2

    currentEpoch = 0
    while alphaIndividual is None or alphaIndividual.getAccuracy() < epsilon:
        fileWriter.write("START EPOCH " + str(currentEpoch))
        try:
            probabilityDistribution = [max(individual.getFitness() for individual in individuals)
                                       - individual.getFitness() for individual in individuals]
            probabilityDistribution = [p / sum(probabilityDistribution) for p in probabilityDistribution]
        except ZeroDivisionError:
            fileWriter("STUCK WITH LOCAL OPTIMUM:\n\tfitness:" + str(alphaIndividual.getFitness())+ "\n\taccuracy:" + str(alphaIndividual.getAccuracy()))
            assert False

        children = []
        for i in range(populationReplacement):
            selected = list(numpy.random.choice(individuals, size=tournamentSize, replace=False, p=probabilityDistribution))
            selected += list(numpy.random.choice(individuals, size=tournamentSize, replace=False, p=probabilityDistribution))

            mother = reduce(fitter, selected[:tournamentSize])
            father = reduce(fitter, selected[tournamentSize:])

            child = mother + father
            if numpy.random.random() < mutationChance:
                child = child.mutate()

            children.append(child)
        fileWriter.write("GENERATED OFFSPRINGS")

        for child in children:
            child.computeFitness(data=data, labels=labels)
        individuals += children

        fileWriter.write("COMPUTED FITNESS FOR OFFSPRINGS")

        individuals.sort(key=lambda individual: individual.getFitness())
        individuals = individuals[:populationSize]

        if alphaIndividual is None or alphaIndividual.getAccuracy() < individuals[0].getAccuracy():
            alphaIndividual = individuals[0]

        fileWriter.write("BEST INDIVIDUAL:\n\tfitness:" + str(alphaIndividual.getFitness())+ "\n\taccuracy:" + str(alphaIndividual.getAccuracy()))
        fileWriter.write("==============================================")
        currentEpoch += 1

    fileWriter.write("POPULATION SIZE: " + str(populationSize) +
                     "MUTATION: " + str(mutationChance) +
                     "REPLACE: " + str(replacePerGenerationPercentage) +
                     "TOURNAMENT: " + str(tournamentPercentage))
    fileWriter.write(str(alphaIndividual))
    fileWriter.write("fitness: " + alphaIndividual.getFitness() +
                     "accuracy: " + alphaIndividual.getAccuracy())

