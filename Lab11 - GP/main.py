from controller import geneticSearch

CLASSES = {
    'Slight-Left-Turn': 0,
    'Move-Forward': 1,
    'Slight-Right-Turn': 2,
    'Sharp-Right-Turn': 3
}

def readData():
    data, labels = [], []
    with open("data/input.data", 'r') as file:
        for line in file.readlines():
            row = line.strip().split(',')
            row, label = row[:-1], row[-1]
            row = [float(x) for x in row]
            data.append(row)
            labels.append(CLASSES[label])
    return data, labels

if __name__ == '__main__':
    # populationSize= int(input("Input population size: "))
    # replacePerGenerationPercentage = float(input("Input replacement percent: "))
    # tournamentPercentage = float(input("Input tournament percent: "))
    # mutationChance = float(input("Input mutation percent: "))
    # epsilon = float(input("Input epsilon target: "))
    data, labels = readData()
    geneticSearch(
        # populationSize=populationSize,
        # replacePerGenerationPercentage=replacePerGenerationPercentage,
        tournamentPercentage=0.2,
        mutationChance=0.4,
        # epsilon=epsilon,
        data=data,
        labels=labels
    )