from controller.controller import Controller, numpy
import matplotlib.pyplot as plt
import concurrent.futures


def testUtility():
    mean = []
    stdDev = []
    variance = []
    fitness = []
    solutions = []
    for i in range(10):
        c = Controller(4, 40)
        solutions.append(c.ACO(1000, 0.5, 0.75, 0.4, 0.25))
        stdDev.append(c.standardDeviation())
        variance.append(c.variance())
        mean.append(c.mean())
        fitness.append(c._bestSolution.fitness())
    return [mean, fitness, variance, stdDev, solutions]

mean = []
stdDeviation = []
variance = []
fitness = []
solutions = []
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    Q1 = executor.submit(testUtility)
    Q2 = executor.submit(testUtility)
    Q3 = executor.submit(testUtility)
    Res1 = Q1.result()
    Res2 = Q2.result()
    Res3 = Q3.result()
    mean = Res1[0] + Res2[0] + Res3[0]
    fitness = Res1[1] + Res2[1] + Res3[1]
    variance = Res1[2] + Res2[2] + Res3[2]
    stdDeviation = Res1[3] + Res2[3] + Res3[3]
    solutions = Res1[4] + Res2[4] + Res3[4]

plt.plot(fitness, 'ro')
plt.show()

print("Mean: " + str(numpy.mean(mean)))
print("Variance: " + str(numpy.mean(variance)))
print("StdDeviance: " + str(numpy.mean(stdDeviation)))
print("Fitness: " + str(numpy.mean(fitness)))