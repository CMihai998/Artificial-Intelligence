from models.FuzzySystem import FuzzySystem

class Controller:
    def __init__(self, temperature, capacity, power, rules):
        self.system = FuzzySystem(rules)
        self.system.addDescription('texture', temperature)
        self.system.addDescription('capacity', capacity)
        self.system.addDescription('type', power, output=True)

    def compute(self, inputs):
        return "With:\t-capacity: " + str(inputs['capacity']) + '\n' + "\t-texture: " + str(inputs['texture']) + '\n' + "\t\t => needed cycle type: " + str(self.system.compute(inputs))