import numpy


class Controller:
    def __init__(self, problem):
        self._problem = problem

    def Greedy(self, root):
        visited = []
        toVisit = [root.getValues()[0]]

        while len(toVisit) > 0:
            node = toVisit.pop(0)
            visited.append(node)
            self._problem._initialState.addValue(node)
            if node.getQueens() == node.getSize():
                return node

            #I put all children with the same heuristics in this list and I choose one randomly, to diversify the solutions of Greedy (it would be boring otherwise)
            aux = []
            minHeureistics = node.getSize() ** 4
            for child in self._problem.expand(node):
                if child not in visited and self._problem.heuristics(child)  <= minHeureistics:
                    aux.append(child)
                    minHeureistics = self._problem.heuristics(child)
            if len(aux) > 0:
                nextChild = numpy.random.randint(0, len(aux))
                toVisit.append(aux[nextChild])

    def DFS(self, root):
        visited = []
        toVisit = [root.getValues()[0]]
        while len(toVisit) > 0:
            node = toVisit.pop()
            visited.append(node)
            self._problem._initialState.addValue(node)
            if self._problem.isSolution(node) and node != root.getValues()[0]:
                return node

            for child in self._problem.expand(node):
                if child not in visited:
                    toVisit.append(child)