from copy import deepcopy
from texttable import Texttable
import numpy


class Configuration:
    def __init__(self, size):
        self._size = size
        self._matrix = numpy.zeros((size, size), dtype=int)
        self._available = [(i,j) for i in range(size) for j in range(size)]
        self._queens = 0

    def getQueens(self):
        return self._queens

    def getValues(self):
        return self._matrix[:]

    def getSize(self):
        return self._size

    def setValues(self, newValues):
        self._matrix = newValues[:]
        self._available = []
        for i in range(0, self._size):
            for j in range(0, self._size):
                if int(newValues[i][j]) == 0:
                    self._available.append((i,j))
                if int(newValues[i][j]) == 1:
                    self._queens += 1

    def getAvailable(self):
        return self._available[:]

    def nextConfig(self, coordinates):
        row = coordinates[0]
        column = coordinates[1]

        nextC = deepcopy(self.getValues())
        if nextC[row][column] != 1:
            nextC[row][column] = 1

            for i in range(self._size):
                if nextC[row][i] == 0:
                    nextC[row][i] = -1
                if nextC[i][column] == 0:
                    nextC[i][column] = -1

            diagX = row - 1
            diagY = column - 1
            while diagX >= 0 and diagY >=0:
                nextC[diagX][diagY] = -1
                diagX -= 1
                diagY -= 1

            diagX = row + 1
            diagY = column + 1
            while diagX < self._size and diagY < self._size:
                nextC[diagX][diagY] = -1
                diagX += 1
                diagY += 1

            diagX = row + 1
            diagY = column - 1
            while diagX < self._size and diagY >= 0:
                nextC[diagX][diagY] = -1
                diagX += 1
                diagY -= 1

            diagX = row - 1
            diagY = column + 1
            while diagX >= 0 and diagY < self._size:
                nextC[diagX][diagY] = -1
                diagX -= 1
                diagY += 1

            newConfig = Configuration(self._size)
            newConfig.setValues(deepcopy(nextC))
            return newConfig
        return None

    def __str__(self):
        table = Texttable()
        for row in self._matrix:
            tableRow = []
            for elem in row:
                if elem == 1:
                    tableRow.append('X')
                else:
                    tableRow.append(' ')
            table.add_row(tableRow)
        return table.draw()

    def __eq__(self, other):
        if isinstance(other, Configuration):
            otherMatrix = other.getValues()
            for i in range(self._size):
                for j in range(self._size):
                    if otherMatrix[i][j] != self._matrix[i][j]:
                        return False
            return True