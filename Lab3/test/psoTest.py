import numpy

from controller.controller import Controller
import matplotlib.pyplot as plt

mean = []
stdDeviation = []
variance = []
fitness = []


for i in range(30):
    c = Controller(40, 4)
    c.particleSwarnOptimisation(1000)
    result = c._problem.evaluateSolutionPSO()
    mean.append(result[0])
    variance.append(result[1])
    stdDeviation.append(result[2])
    fitness.append(result[4])

plt.plot(fitness, 'ro')
plt.show()

print("Mean: " + str(numpy.mean(mean)))
print("Variance: " + str(numpy.mean(variance)))
print("StdDeviance: " + str(numpy.mean(stdDeviation)))
print("Fitness: " + str(numpy.mean(fitness)))

