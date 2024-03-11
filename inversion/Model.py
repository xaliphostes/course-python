from Data import Data
from DataFactory import create
from myTypes import Vector
from MonteCarlo import monteCarlo
from plots import plotDomain


class Model:
    data: list[Data] = []

    def add(self, normal: Vector, dataType: str):
        self.data.append(create(dataType, normal))

    def addFromFile(self, filename: str, dataType: str):
        f = open(filename, "r")
        for line in f:  # for each line
            tokens = line.removesuffix('\n').split(' ')
            n = [float(tokens[0]), float(tokens[1])]
            self.add(n, dataType)

    def run(self, n: int):
        monteCarlo(self.data, n)

    def plotDomain(self, n: int):
        plotDomain(self.data, n)

