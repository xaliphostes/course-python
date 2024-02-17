import math
import random as rnd
import functools
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Callable

def normalize(n: Tuple[float,float]) -> Tuple[float,float]:
    l = math.sqrt(n[0] ** 2 + n[1] ** 2)
    if l != 0:
        return [n[0] / l, n[1] / l]
    return n

def dot(n1: Tuple[float,float], n2: Tuple[float,float]) -> float:
    return n1[0]*n2[0] + n1[1]*n2[1]

def lerp(v0: float, v1: float, t: float) -> float :
    return (1 - t) * v0 + t * v1

class RemoteStress:
    def __init__(self, S1: Tuple[float,float], S3: Tuple[float,float]) -> None:
        self.S1, self.S3 = S1, S3

class Data:
    cost: Callable
    n: Tuple[float,float]
    def __init__(self, n: Tuple[float,float], cost: Callable) -> None:
        self.cost = cost
        self.n = n

def remoteStress(theta, k):
    a = theta*math.pi/180.0
    c, s = math.cos(a), math.sin(a)
    xx, xy, yy = k*c*c + s*s, (k - 1)*c*s, k*s*s + c*c
    trace = xx + yy
    discri = math.sqrt(trace*trace - 4*(xx * yy - xy*xy))
    # Decreasing order according to the eigen values
    S1 = normalize([xy, (trace + discri) / 2 - xx])
    S3 = normalize([xy, (trace - discri) / 2 - xx])
    return RemoteStress(S1, S3)
        
def costJoint(n: Tuple[float,float], r: RemoteStress) -> float:
    return 1.0 - math.fabs(dot(n, r.S1))

def costStylo(n: Tuple[float,float], r: RemoteStress) -> float:
    return 1.0 - math.fabs(dot(n, r.S3))

def mc(data: List[Data], n: int = 5000):
    cost, theta, k = 1e9, 0, 0
    for i in range(0, n):
        THETA, K = lerp(0, 180, rnd.random()), lerp(0, 1, rnd.random())
        remote = remoteStress(THETA, K)
        c = functools.reduce(lambda a, b: a+b, [x.cost(x.n, remote) for x in data]) / len(data)
        if c < cost:
            cost, theta, k = c, THETA, K
            print(theta, k, c)

def plot(data: List[Data], n: int):
    Z = np.zeros(shape=(n,n))
    min = 0
    max = 0.99
    for i in range(0, n):
        k = lerp(min, max, i/(n-1))
        for j in range(0, n):
            theta = lerp(0, 180, j/(n-1))
            remote = remoteStress(theta, k)
            Z[j][i] = functools.reduce(lambda a, b: a+b, [x.cost(x.n, remote) for x in data]) / len(data)
            
    X, Y = np.meshgrid(np.linspace(min, max, n), np.linspace(0, 180, n))
    levels = np.linspace(Z.min(), Z.max(), 20)
    cmap = 'jet'
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.contourf(np.linspace(min, max, n), np.linspace(0, 180, n), Z, levels=levels, cmap=cmap)
    ax.set_xlabel('R')
    ax.set_ylabel('Theta')
    ax.margins(0.2)
    ax.set_title("Domain")
    fig.colorbar(plt.cm.ScalarMappable(cmap=cmap), ax=ax, orientation='vertical', label='Cost')
    plt.show()
        
# -------------------------------------------

data: List[Data] = []

def addData(file: str, costFct: Callable):
    f = open(file, "r")
    for line in f: # each line
        toks = line.removesuffix('\n').split(' ')
        data.append( Data([float(toks[0]), float(toks[1])], costFct) )

addData("matelles-joints.txt", costJoint)
addData("matelles-stylolites.txt", costStylo)
mc(data, 10000)
plot(data, 50)