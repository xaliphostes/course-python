import Data
from RemoteStress import RemoteStress
from tools import lerp
import numpy as np
import matplotlib.pyplot as plt
import functools


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
