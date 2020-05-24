class FuzzySystem:
    """
    Receives variable descriptions and rules
    and outputs the defuzzified result of the system
    """

    def __init__(self, rules):
        self.inputDescriptions = {}
        self.outputDescriptions = None
        self.rules = rules

    def addDescription(self, name, description, output=False):
        if output:
            if self.outputDescriptions is None:
                self.outputDescriptions = description
            else:
                raise ValueError("Already assigned an output")
        else:
            self.inputDescriptions[name] = description

    def computeDescriptions(self, inputs):
        return {variableName: self.inputDescriptions[variableName].fuzzify(inputs[variableName]) for variableName, value in inputs.items()}

    def computeFuzzyRules(self, fuzzyValues):
        return [rule.evaluate(fuzzyValues) for rule in self.rules if rule.evaluate(fuzzyValues)[1] != 0]

    def compute(self, inputs):
        fuzzyValues = self.computeDescriptions(inputs)
        ruleValues = self.computeFuzzyRules(fuzzyValues)

        fuzzyOutputValues = [(list(description[0].values())[0], description[1]) for description in ruleValues]

        weightedTotal = sum(value[1] for value in fuzzyOutputValues)
        weightSum = sum(self.outputDescriptions.defuzzify(value[0], value[1]) * value[1] for value in fuzzyOutputValues)

        return weightedTotal / weightSum