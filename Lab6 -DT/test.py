import numpy


def updateAttributes(attributes, labelToRemove):
	deleted = False
	for key in list(attributes):
		if deleted:
			attributes[key] -= 1
		if key == labelToRemove:
			deleted = True
			del attributes[key]

	return attributes


data = {1: 5,
        2: 6,
        3: 7,
        4: 8}

print(data)
data = updateAttributes(data, 3)
print(data)
d = {}
print(len(d.keys()))

random = []
# while len(random) != 400:
s = (400 - len(random))
random = numpy.random.randint(low=0, high=625, size=400)
random = set(random)
random = numpy.random.choice([i for i in range(625)], size=400)
print(len(random))
