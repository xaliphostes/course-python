from Model import Model


if __name__ == '__main__':
    model = Model()
    model.addFromFile("../matelles-joints.txt", 'joint')
    model.addFromFile("../matelles-stylolites.txt", 'stylolite')
    model.run(10000)

    model.plotDomain(50)
    Model.plotCostFunctions()
