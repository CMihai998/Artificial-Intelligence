class FuzzyRule:
    """
        Define a conjunctive fuzzy rule
        X and Y and ... => Z
    """
    def __init__(self, inputs, out):
        """
            Receives the set of inputs and expected output
        """
        self.output = out  # the name of the output variable
        self.inputs = inputs

    def evaluate(self, inputs):
        """
            Receives a dictionary of all the input values and returns the conjunction
            of their values
        """
        return [self.output, min([inputs[descriptionName][variableName] for descriptionName, variableName in self.inputs.items()])]
