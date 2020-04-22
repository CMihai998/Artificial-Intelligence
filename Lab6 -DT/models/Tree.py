class Tree:
    def __init__(self, root, data=None):
        self._data = data
        self._root = root

    def clasify(self, data):
        attributes = {'L1': 1,
                      'L2': 2,
                      'L3': 3,
                      'L4': 4}
        queue = [self._root]
        currentNode = None
        while len(queue) != 0:
            currentNode = queue.pop()
            children = currentNode.getChildren()
            for i in range(len(children)):
                if children[i].getValue() == data[attributes[currentNode.getLabel()]]:
                    queue.append(children[i])
        return currentNode.getLabel().find(data[0]) != -1