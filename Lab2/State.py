class State:
    def __init__(self):
        self._values = []

    def addValue(self, newValue):
        self._values.append(newValue)

    def getValues(self):
        return self._values[:]