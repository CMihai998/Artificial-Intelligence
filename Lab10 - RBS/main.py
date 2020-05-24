from controller import Controller
from models.FuzzyDescription import FuzzyDescription
from models.FuzzyRule import FuzzyRule


def trapezoidalRegion(a, b, c, d):
    return lambda x: max(0, min((x - a) / (b - a), 1, (d - x) / (d - c)))

def trianularRegion(a, b, c):
    return trapezoidalRegion(a, b, b, c)

def inverseLine(a, b):
    return lambda x: x * (b - a) + a

def inverseTriangular(a, b, c):
    return lambda x: (inverseLine(a, b)(x) + inverseLine(c, b)(x)) / 2

if __name__ == '__main__':
    texture = FuzzyDescription()
    capacity = FuzzyDescription()
    type = FuzzyDescription()
    rules = []

    texture.addRegion('verySoft', trapezoidalRegion(-1, -0, 0.2, 0.4))
    texture.addRegion('soft', trianularRegion(0.2, 0.4, 0.8))
    texture.addRegion('normal', trianularRegion(0.3, 0.7, 0.9))
    texture.addRegion('resistant', trapezoidalRegion(0.7, 0.9, 1, 2))

    capacity.addRegion('small', trapezoidalRegion(-1, 0, 1, 2))
    capacity.addRegion('medium', trianularRegion(1, 2.5, 4))
    capacity.addRegion('high', trapezoidalRegion(3, 4, 5, 6))

    type.addRegion('delicate', trapezoidalRegion(-1, 0, 0.2, 0.4), inverse=inverseLine(0, 0.4))
    type.addRegion('easy', trianularRegion(0.2, 0.5, 0.8), inverse=inverseTriangular(0.2, 0.5, 0.6))
    type.addRegion('normal', trianularRegion(0.3, 0.6, 0.9), inverse=inverseTriangular(0.3, 0.6, 0.9))
    type.addRegion('intense', trapezoidalRegion(0.7, 0.9, 1, 2), inverse=inverseLine(0.7, 2))

    rules.append(FuzzyRule({'texture': 'verySoft', 'capacity': 'small'},
                           {'type': 'delicate'}))
    rules.append(FuzzyRule({'texture': 'verySoft', 'capacity': 'medium'},
                           {'type': 'easy'}))
    rules.append(FuzzyRule({'texture': 'verySoft', 'capacity': 'high'},
                           {'type': 'normal'}))

    rules.append(FuzzyRule({'texture': 'soft', 'capacity': 'small'},
                           {'type': 'easy'}))
    rules.append(FuzzyRule({'texture': 'soft', 'capacity': 'medium'},
                           {'type': 'normal'}))
    rules.append(FuzzyRule({'texture': 'soft', 'capacity': 'high'},
                           {'type': 'normal'}))

    rules.append(FuzzyRule({'texture': 'normal', 'capacity': 'small'},
                           {'type': 'easy'}))
    rules.append(FuzzyRule({'texture': 'normal', 'capacity': 'medium'},
                           {'type': 'normal'}))
    rules.append(FuzzyRule({'texture': 'normal', 'capacity': 'high'},
                           {'type': 'intense'}))

    rules.append(FuzzyRule({'texture': 'resistant', 'capacity': 'small'},
                           {'type': 'easy'}))
    rules.append(FuzzyRule({'texture': 'resistant', 'capacity': 'medium'},
                           {'type': 'normal'}))
    rules.append(FuzzyRule({'texture': 'resistant', 'capacity': 'high'},
                           {'type': 'intense'}))

    controller = Controller(texture, capacity, type, rules)

    print(controller.compute({'capacity': 1.2, 'texture': 0.4}))
    print(controller.compute({'capacity': 3, 'texture': 0.77}))
