#
# PROCEDURAL programming in Python
#

import math
import random as rnd
import functools
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable

type Vector = list[float]
type Stress = list[Vector]


def normalize(n: Vector) -> Vector:
    l = math.sqrt(n[0] ** 2 + n[1] ** 2)
    if l != 0:
        return [n[0] / l, n[1] / l]
    else:
        return n


def deg2rad(a: float) -> float:
    return a * math.pi / 180


def dot(n1: Vector, n2: Vector) -> float:
    return n1[0] * n2[0] + n1[1] * n2[1]


def lerp(v0: float, v1: float, t: float) -> float:
    return (1 - t) * v0 + t * v1


class PrincipalDirections:
    S1: Vector
    S3: Vector

    def __init__(self, S1: Vector, S3: Vector) -> None:
        self.S1, self.S3 = S1, S3


class Data:
    cost: Callable
    n: Vector

    def __init__(self, n: Vector, cost: Callable) -> None:
        self.cost = cost
        self.n = n


def principalDirections(theta: float, k: float) -> PrincipalDirections:
    a = deg2rad(theta)
    c, s = math.cos(a), math.sin(a)
    xx, xy, yy = k * s * s, k * c * s, k * c * c
    trace = xx + yy
    discri = math.sqrt(trace * trace - 4 * (xx * yy - xy * xy))
    # Decreasing order according to the eigen values
    S1 = normalize([xy, (trace + discri) / 2 - xx])
    S3 = normalize([xy, (trace - discri) / 2 - xx])
    return PrincipalDirections(S1, S3)


def costJoint(n: Vector, r: PrincipalDirections) -> float:
    return 1.0 - math.fabs(dot(n, r.S3))


def costStylo(n: Vector, r: PrincipalDirections) -> float:
    return 1.0 - math.fabs(dot(n, r.S1))


# Monte Carlo simulation (random)
def mc(data: list[Data], n: int = 5000):
    cost, theta, k = 1e9, 0, 0
    for i in range(0, n):
        THETA, K = lerp(0, 180, rnd.random()), lerp(0, 1, rnd.random())
        remote = principalDirections(THETA, K)
        c = functools.reduce(lambda a, b: a + b, [x.cost(x.n, remote) for x in data], 0) / len(data)
        if c < cost:
            cost, theta, k = c, THETA, K
            print(theta, k, c)


# Going further, plot the stress domain to check the solution
def plotDomain(data: list[Data], n: int):
    Z = np.zeros(shape=(n, n))
    min = 0.001
    max = 0.99
    for i in range(0, n):
        k = lerp(min, max, i / (n - 1))
        for j in range(0, n):
            theta = lerp(0, 180, j / (n - 1))
            remote = principalDirections(theta, k)
            Z[j][i] = functools.reduce(lambda a, b: a + b, [x.cost(x.n, remote) for x in data]) / len(data)

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

    for angle in range(0, 91, 1):
        x.append(angle)
        dirs = principalDirections(angle, 1)
        yj.append(costJoint([0, 1], dirs))
        ys.append(costStylo([0, 1], dirs))

    fig, ax = plt.subplots()
    ax.plot(x, yj, label='Joint')
    ax.plot(x, ys, label='Stylolite')
    ax.legend()
    px = 1 - math.sqrt(2) / 2
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


# -------------------------------------------

data: list[Data] = []


def addData(file: str, costFct: Callable):
    f = open(file, "r")
    for line in f:  # for each line
        tokens = line.removesuffix('\n').split(' ')
        nx = float(tokens[0])
        ny = float(tokens[1])
        data.append(Data([nx, ny], costFct))


addData("matelles-joints.txt", costJoint)
addData("matelles-stylolites.txt", costStylo)
mc(data, 10000)

plotDomain(data, 50)
plotRotateS3()