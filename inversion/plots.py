import Data
import math
import numpy as np
import matplotlib.pyplot as plt
import functools
from RemoteStress import RemoteStress
from Joint import Joint
from Stylolite import Stylolite
from tools import lerp


def plotCostFunctions():
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


def plotDomain(data: list[Data], n: int):
    Z = np.zeros(shape=(n, n))
    min_ = 0.001
    max_ = 0.99
    remote = RemoteStress()
    for i in range(0, n):
        k = lerp(min_, max_, i / (n - 1))
        for j in range(0, n):
            theta = lerp(0, 180, j / (n - 1))
            remote.set(theta, k)
            Z[j][i] = functools.reduce(lambda a, b: a + b, [x.cost(remote) for x in data]) / len(data)

    X, Y = np.meshgrid(np.linspace(min_, max_, n), np.linspace(0, 180, n))
    levels = np.linspace(Z.min(), Z.max(), 50)
    cmap = 'jet'
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.contourf(np.linspace(min_, max_, n), np.linspace(0, 180, n), Z, levels=levels, cmap=cmap)
    ax.set_xlabel('R')
    ax.set_ylabel('Theta')
    ax.margins(0.2)
    ax.set_title("Domain")
    fig.colorbar(plt.cm.ScalarMappable(cmap=cmap), ax=ax, orientation='vertical', label='Cost')
    plt.show()
