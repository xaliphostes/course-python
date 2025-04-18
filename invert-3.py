#
# OBJECT ORIENTED programming in Python
# - Use types
# - Use class
# - Use abstract class and polymorphism
#

import math
import random as rnd
import functools
import numpy as np
import matplotlib.pyplot as plt
from abc import abstractmethod

def dot(n1, n2) -> float:
    return n1[0] * n2[0] + n1[1] * n2[1]


def lerp(v0: float, v1: float, t: float) -> float:
    return (1 - t) * v0 + t * v1


def normalize(n) :
    l = math.sqrt(n[0] ** 2 + n[1] ** 2)
    if l != 0:
        return [n[0] / l, n[1] / l]
    else:
        return n


# --------------------------------------------------


class RemoteStress:
    @property
    def S1(self) :
        return self.__S1

    @property
    def S3(self) :
        return self.__S3

    def set(self, theta: float, k: float) -> None:
        a = math.radians(theta)
        c, s = math.cos(a), math.sin(a)
        xx, xy, yy = k * s * s, k * c * s, k * c * c
        trace = xx + yy
        discri = math.sqrt(trace * trace - 4 * (xx * yy - xy * xy))
        # Decreasing order according to the eigen values
        self.__S1 = normalize([xy, (trace + discri) / 2 - xx])
        self.__S3 = normalize([xy, (trace - discri) / 2 - xx])


# --------------------------------------------------

# Class de base (abstraite car ne fait rien)
class Data:
    def __init__(self, n) -> None: self.n = n

    @abstractmethod
    def cost(self, r: RemoteStress) -> float: pass


# Class dérivée de Data
class Joint(Data):
    def cost(self, r: RemoteStress) -> float:
        return 1.0 - math.fabs(dot(self.n, r.S3))


# Class dérivée de Data
class Stylolite(Data):
    def cost(self, r: RemoteStress) -> float:
        return 1.0 - math.fabs(dot(self.n, r.S1))

# --------------------------------------------------


# Simulation aléatoire pour trouver la solution
def monteCarlo(data: list[Data], n: int = 5000):
    """ Monte Carlo simulation (random)

    Args:
        data (list[Data]): a list of Data
        n (int, optional): The number of random simulations. Defaults to 5000.
    """
    cost, theta, k = 1e9, 0, 0
    remote = RemoteStress()
    for i in range(0, n):
        THETA, K = lerp(0, 180, rnd.random()), lerp(0, 1, rnd.random())
        remote.set(THETA, K)
        c = functools.reduce(lambda a, b: a + b, [x.cost(remote) for x in data], 0) / len(data)
        if c < cost:
            cost, theta, k = c, THETA, K
            print(theta, k, c)


def plotDomain(data: list[Data], n: int):
    Z = np.zeros(shape=(n, n))
    min = 0.001
    max = 0.99
    remote = RemoteStress()
    for i in range(0, n):
        k = lerp(min, max, i / (n - 1))
        for j in range(0, n):
            theta = lerp(0, 180, j / (n - 1))
            remote.set(theta, k)
            Z[j][i] = functools.reduce(lambda a, b: a + b, [x.cost(remote) for x in data]) / len(data)

    X, Y = np.meshgrid(np.linspace(min, max, n), np.linspace(0, 180, n))
    levels = np.linspace(Z.min(), Z.max(), 50)
    cmap = 'jet'
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.contourf(np.linspace(min, max, n), np.linspace(0, 180, n), Z, levels=levels, cmap=cmap)
    ax.set_xlabel('R')
    ax.set_ylabel('Theta')
    ax.margins(0.2)
    ax.set_title("Domain")
    fig.colorbar(plt.cm.ScalarMappable(cmap=cmap), ax=ax, orientation='vertical', label='Cost')
    plt.show()


def plotRotateS3():
    x = []

    yj = []
    ys = []

    font = {'family': 'serif',
            'color': 'darkred',
            'weight': 'normal',
            'size': 16,
            }

    remote = RemoteStress()
    joint = Joint([0, 1])
    stylo = Stylolite([0, 1])

    for angle in range(0, 91, 1):
        x.append(angle)
        remote.set(angle, 1)
        yj.append(joint.cost(remote))
        ys.append(stylo.cost(remote))

    fig, ax = plt.subplots()
    ax.plot(x, yj, label='Joint')
    ax.plot(x, ys, label='Stylolite')
    ax.legend()
    px = 1 - math.sqrt(2)/2
    ax.axvline(x=45, linewidth=1, color='black', linestyle=(0, (5, 5)))
    ax.axhline(xmax=45, y=px, linewidth=1, color='black', linestyle=(0, (5, 5)))
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1)
    # ---
    plt.title('Cost functions for a vertical fracture', fontdict=font)
    plt.xlabel('$\sigma_3$ orientation', fontdict=font)
    plt.ylabel('Cost', fontdict=font)
    # ---
    plt.show()


def addData(file: str, dataType: str, data: list[Data]):
    f = open(file, "r")
    for line in f:  # for each line
        tokens = line.removesuffix('\n').split(' ')
        nx = float(tokens[0])
        ny = float(tokens[1])
        if dataType == 'joint':
            data.append(Joint([nx, ny]))
        elif dataType == 'stylolite':
            data.append(Stylolite([nx, ny]))
        else:
            raise Exception('data type {dataType} is unknown!')


# -------------------------------------------

def main():
    data: list[Data] = []
    addData("data/matelles-joints.txt", 'joint', data)
    addData("data/matelles-stylolites.txt", 'stylolite', data)

    monteCarlo(data, 10000)
    plotDomain(data, 20)
    # plotRotateS3()


# -------------------------------------------

main()
