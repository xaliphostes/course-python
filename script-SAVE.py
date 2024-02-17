# At least pythpn 3.12 !!!

import numpy as np
from numpy import linalg as LA
from functools import reduce
from typing import Tuple
import random as rnd
import math
import matplotlib.pyplot as plt

# Define for Python >= 3.12
# type Vector2 = Tuple[float, float]

def lerp(v0: float, v1: float, t: float) -> float :
    return (1 - t) * v0 + t * v1

class Stress:
    def __init__(self, xx: float, xy: float, yy: float) -> None:
        self.xx = xx
        self.xy = xy
        self.yy = yy
    def __str__(self) -> str:
        return f'[{self.xx}, {self.xy}, {self.yy}]'

class RemoteStress:
    __k = 0     # param
    __theta = 0 # param
    __s = 0     # tmp
    __c = 0     # tmp
    xx = 0
    xy = 0
    yy = 0
    S1 = [0,0]
    S2 = [0,0]
    
    @staticmethod
    def rand(mag: float = 1):
        s = RemoteStress()
        s.randomize(mag)
        return s
    
    @property
    def k(self):
        return self.__k
    
    @k.setter
    def k(self, v):
        self.__k = v
        self.__update()
        
    @property
    def theta(self):
        return self.__theta
    
    @theta.setter
    def theta(self, v):
        self.__theta = v
        a = v * math.pi / 180
        self.__c = math.cos(a)
        self.__s = math.sin(a)
        self.__update()
    
    def randomize(self, mag: float = 1) -> Stress :
        self.theta = rnd.randint(1, 180)
        self.k = lerp(0, mag, rnd.random()) # mag * rnd.random()
        return self.stress()
    
    def stress(self) -> Stress:
        k = self.__k
        c = self.__c
        s = self.__s
        return Stress(k*c*c + s*s, (k - 1)*c*s, k*s*s + c*c) # (xx, xy, yy)
    
    def __update(self):
        k = self.__k
        c = self.__c
        s = self.__s
        self.xx = k*c*c + s*s
        self.xy = (k - 1)*c*s
        self.yy = k*s*s + c*c
        eigenvalues, eigenvectors = LA.eig([[self.xx, self.xy],[self.xy, self.yy]])
        self.S1 = eigenvectors[0]
        self.S2 = eigenvectors[1]

class IData:
    def __init__(self, n: Tuple[float, float]) -> None:
        l = LA.norm(n)
        self.__n = n
        self.__n[0] /= l
        self.__n[1] /= l
        
    def normal(self) -> Tuple[float, float]:
        return self.__n
    
    def cost(self, stress: Stress) -> float: return 0
    
    def type(self) -> str: return ""

class Joint(IData):
    def cost(self, stress: Stress) -> float:
        eigenvalues, eigenvectors = LA.eig([[stress.xx, stress.xy],[stress.xy, stress.yy]])
        return 1.0 - abs(np.dot(self.normal(), eigenvectors[0]))
    def type(self) -> str:
        return "joint"

class Stylolite(IData):
    def cost(self, stress: Stress) -> float:
        eigenvalues, eigenvectors = LA.eig([[stress.xx, stress.xy],[stress.xy, stress.yy]])
        return 1.0 - abs(np.dot(self.normal(), eigenvectors[1]))
    def type(self) -> str:
        return "stylolite"

class DataFactory:
    @staticmethod
    def get(name: str, n: Tuple[float, float]) -> IData:
        if name== 'joint': return Joint(n)
        if name== 'stylolite': return Stylolite(n)
        return None

class ISolver:
    datas = list()
    def addData(self, d: IData) -> None:
        self.datas.append(d)
    def run(self): pass # abstract
    
class MC(ISolver):
    __iter: int = 0
    def __init__(self, n: int = 1000) -> None:
        super().__init__()
        self.__iter = n
    def setNbIter(self, n: int): self.__iter = n
    def addData(self, d: IData) -> None:
        self.datas.append(d)
    def run(self):
        remote = RemoteStress()
        cost = 1e9
        theta = 0
        k = 0
        iter = 0
        for i in range(self.__iter):
            s = remote.randomize()
            c = reduce(lambda prev, data: prev + data.cost(remote.stress()), self.datas, 0) / len(self.datas)
            if c < cost:
                cost = c
                theta = remote.theta
                k = remote.k
                iter = i
                print(iter, cost, theta, k)

class Grid(ISolver):
    __n = 3
    minR = 0
    maxR = 1
    def __init__(self, n: int) -> None:
        self.__n = n
    def run(self):
        remote = RemoteStress()
        cost = 1e9
        theta = 0
        k = 0
        iter = 0
        delta = 1/(self.__n-1)
        for i in range(0, self.__n):
            remote.k = lerp(self.minR, self.maxR, i*delta) # i / (self.__n - 1)
            for j in range(0, self.__n):
                remote.theta = lerp(0, 180, j *delta) # j * 180 / (self.__n - 1)
                c = reduce(lambda prev, data: prev + data.cost(remote.stress()), self.datas, 0) / len(self.datas)
                if c < cost:
                    cost = c
                    theta = remote.theta
                    k = remote.k
                    iter = i*self.__n + j
                    print(iter, cost, theta, k)
    def plot(self):
        remote = RemoteStress()
        Z = np.zeros(shape=(self.__n,self.__n))
        delta = 1/(self.__n-1)
        
        for i in range(0, self.__n):
            remote.k = lerp(self.minR, self.maxR, i*delta)
            for j in range(0, self.__n):
                remote.theta = lerp(0, 180, j *delta)
                print(remote.stress())
                Z[j][i] =  reduce(lambda prev, data: prev + data.cost(remote.stress()), self.datas, 0) / len(self.datas) 
        
        X, Y = np.meshgrid(np.linspace(self.minR, self.maxR, self.__n), np.linspace(0, 180, self.__n))
        levels = np.linspace(Z.min(), Z.max(), 10)
        
        cmap = 'jet'
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.contourf(np.linspace(self.minR, self.maxR, self.__n), np.linspace(0, 180, self.__n), Z, levels=levels, cmap=cmap)
        ax.set_xlabel('R')
        ax.set_ylabel('Theta')
        ax.margins(0.2)
        ax.set_title("Domain")
        
        fig.colorbar(plt.cm.ScalarMappable(cmap=cmap), ax=ax, orientation='vertical', label='Cost')
        plt.show()

# ----------------------------------------------------------

# solver = MC(5000)
solver = Grid(50)

f = open("matelles-joints.txt", "r")
for line in f: # each line
    toks = line.removesuffix('\n').split(' ')
    solver.addData( DataFactory.get('joint', [float(toks[0]), float(toks[1])]) )
    
f = open("matelles-stylolites.txt", "r")
for line in f: # each line
    toks = line.removesuffix('\n').split(' ')
    solver.addData( DataFactory.get('stylolite', [float(toks[0]), float(toks[1])]) )

# solver.run()
solver.plot()
