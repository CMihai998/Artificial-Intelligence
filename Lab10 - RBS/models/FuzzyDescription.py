class FuzzyDescription:
    """
    Encapsulates description of fuzzy variable
    Contains set of functions for each fuzzy region
    """
    def __init__(self):
        self.regions = {}
        self.inverse = {}

    def addRegion(self, variableName, membershipFunction, inverse=None):
        """
        Adds region with given memebership function
        Inverse is an optional function for Sugeno or Tsukamoto models
        """
        self.regions[variableName] = membershipFunction
        self.inverse[variableName] = inverse

    def fuzzify(self, value):
        """
        Returns the fuzzified values for each region
        """
        return {name: membershipFunction(value) for name, membershipFunction in self.regions.items()}

    def defuzzify(self, variableName, value):
        """
        Returns the defuzzified value
        """
        return self.inverse[variableName](value)