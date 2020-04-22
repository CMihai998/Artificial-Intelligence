class Node:
    def __init__(self, label, data=None):
        self._label = label
        self._data = data
        self._children = []
        self._value = None

    def addChildren(self, child, value):
        child.setValue(value)
        self._children.append(child)

    def setValue(self, value):
        self._value = value

    def removeChild(self, child):
        self._children.remove(child)

    def getValue(self):
        return self._value

    def getChildren(self):
        return self._children[:]

    def getLabel(self):
        return self._label

    def __str__(self):

        return 'l:' +str(self._label) + ' v:' + str(self._value) + ' children:'+ str(len(self._children))