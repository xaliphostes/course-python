from Model import Model
from plots import plotCostFunctions


if __name__ == '__main__':
    model = Model()
    model.addFromFile("../data/matelles-joints.txt", 'joint')
    model.addFromFile("../data/matelles-stylolites.txt", 'stylolite')
    model.run(10000)
    model.plotDomain(50)

    plotCostFunctions()
