from copy import deepcopy

import numpy

from State import State

class Problem:
    def __init__(self, initial):
        self._initialConfig = initial
        self._initialState = State()
        self._initialState.addValue(deepcopy(self._initialConfig))

    def expand(self, currentState):
        expansion = []

        for coordinates in currentState.getAvailable():
            nextConfig = currentState.nextConfig(coordinates)
            if nextConfig != None:
                expansion.append(deepcopy(nextConfig))

        return expansion

    def isSolution(self, config):
        table = config.getValues()
        size = config.getSize()

        if config.getQueens() != size:
            return False

        for line in table:
            queens = 0
            for elem in line:
                if elem == 1:
                    queens += 1
            if queens != 1:
                return False

        for column in range(size):
            queens = 0
            for row in range(size):
                if table[row][column] == 1:
                    queens += 1
            if queens != 1:
                return False

        for offset in range(- size + 1, size):
            queens = 0
            for elem in table.diagonal(offset):
                if elem == 1:
                    queens += 1
            if queens > 1:
                return False

        table = numpy.rot90(table)
        for offset in range(- size + 1, size):
            queens = 0
            for elem in table.diagonal(offset):
                if elem == 1:
                    queens += 1
            if queens > 1:
                return False

        return True


    def getRoot(self):
        return self._initialState

    def heuristics(self, config):
        return (config.getSize() * config.getSize() - len(config.getAvailable()))
