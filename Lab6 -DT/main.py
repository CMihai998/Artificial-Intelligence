import numpy

from Controller import Controller

if __name__ == '__main__':
    result = []
    runs = 3000
    print("This will take a second...")
    for i in range(runs):
        trainingData, testData = Controller.readData()
        c = Controller()
        c.generateTree(trainingData)
        tree = c.getTree()
        count = 0
        for i in range(len(testData)):
            if tree.clasify(testData[i]):
                count += 1
        result.append((count * 100)/len(testData))
    print('Maximum percentage: ', max(result), '%')

