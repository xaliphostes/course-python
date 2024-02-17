# from numpy import linalg as LA
import numpy as np
from functools import reduce
from typing import Tuple
import random as rnd
import math
import matplotlib.pyplot as plt
import time

# Define for Python >= 3.12
# type Vector2 = Tuple[float, float]

def lerp(v0: float, v1: float, t: float) -> float :
    return (1 - t) * v0 + t * v1

def normalize(n: Tuple[float,float]) -> Tuple[float,float]:
    l = math.sqrt(n[0] ** 2 + n[1] ** 2)
    if l != 0:
        return [n[0] / l, n[1] / l]
    return n

def dot(n1: Tuple[float,float], n2: Tuple[float,float]) -> float:
    return n1[0]*n2[0] + n1[1]*n2[1]

def degToRad(a: float) -> float:
    return a * math.pi / 180

class RemoteStress:
    __k = 0.     # param
    __theta = 0. # param
    S1: Tuple[float,float] = [0,0]
    S2: Tuple[float,float] = [0,0]
    
    def __str__(self) -> str:
        return f'[{self.S1}, {self.S2}]'
    
    @staticmethod
    def rand(mag: float = 1):
        s = RemoteStress()
        s.randomize(mag)
        return s
    
    @property
    def k(self) -> float:
        return self.__k
    
    @k.setter
    def k(self, v: float):
        self.__k = v
        self.__update()
        
    @property
    def theta(self) -> float:
        return self.__theta
    
    @theta.setter
    def theta(self, v: float):
        self.__theta = v
        self.__update()
    
    def randomize(self, mag: float = 1) :
        self.theta = lerp(0, 180, rnd.random())
        self.k = lerp(0, mag, rnd.random())
        
    def __update(self):
        a = degToRad(self.__theta)
        k = self.__k
        
        c = math.cos(a)
        s = math.sin(a)
        xx = k*c*c + s*s
        xy = (k - 1)*c*s
        yy = k*s*s + c*c
        trace = xx + yy
        
        # eigenvalues, eigenvectors = LA.eig([[xx, xy],[xy, yy]])
        # self.S1 = eigenvectors[1]
        # self.S2 = eigenvectors[0]
        
        discri = math.sqrt(trace*trace - 4*(xx * yy - xy*xy))
        if discri != 0:
            # Decreasing order according to the eigen values
            self.S1 = normalize([xy, (trace + discri) / 2 - xx])
            self.S2 = normalize([xy, (trace - discri) / 2 - xx])
        else:
            self.S1 = [0,0]
            self.S2 = [0,0]

class IData:
    __n: Tuple[float,float] = [0,0]
    
    def __init__(self, n: Tuple[float, float]) -> None:
        self.__n = n
        normalize(self.__n)
        
    def normal(self) -> Tuple[float, float]:
        return self.__n
    
    def cost(self, stress: RemoteStress) -> float: return 0
    
    def type(self) -> str: return ""

class ISolver:
    datas = list()
    def addData(self, d: IData) -> None:
        self.datas.append(d)
    def run(self): pass # abstract
    
class Joint(IData):
    def cost(self, stress: RemoteStress) -> float:
        # eigenvalues, eigenvectors = LA.eig([[stress.xx, stress.xy],[stress.xy, stress.yy]])
        return 1.0 - math.fabs(dot(self.normal(), stress.S1))
    def type(self) -> str:
        return "joint"

class Stylolite(IData):
    def cost(self, stress: RemoteStress) -> float:
        # eigenvalues, eigenvectors = LA.eig([[stress.xx, stress.xy],[stress.xy, stress.yy]])
        return 1.0 - math.fabs(dot(self.normal(), stress.S2))
    def type(self) -> str:
        return "stylolite"

class DataFactory:
    @staticmethod
    def get(name: str, n: Tuple[float, float]) -> IData:
        if name== 'joint': return Joint(n)
        if name== 'stylolite': return Stylolite(n)
        return None

# This is how to define a "decorator" in Python
def stopwatch(f):
    def func(*args, **kwargs):
        tic = time.time()
        result = f(*args, **kwargs)
        t = time.time() - tic
        print(f"Elapsed time: {'{:.2}'.format(t)}s")
        return result
    return func
 
class MC(ISolver):
    __iter: int = 0
    def __init__(self, n: int = 1000) -> None:
        super().__init__()
        self.__iter = n
    def setNbIter(self, n: int): self.__iter = n
    def addData(self, d: IData) -> None:
        self.datas.append(d)
        
    def plot(self): pass
        
    @stopwatch
    def run(self):
        remote = RemoteStress()
        cost = 1e9
        theta = 0
        k = 0
        iter = 0
        for i in range(self.__iter):
            s = remote.randomize()
            c = reduce(lambda prev, data: prev + data.cost(remote), self.datas, 0) / len(self.datas)
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
    
    @stopwatch
    def run(self):
        remote = RemoteStress()
        cost = 1e9
        theta = 0
        k = 0
        iter = 0
        n = self.__n
        delta = 1/(n-1)
        
        for i in range(0, n):
            remote.k = lerp(self.minR, self.maxR, i*delta)
            for j in range(0, n):
                remote.theta = lerp(0, 180, j*delta)
                c = reduce(lambda prev, data: prev + data.cost(remote), self.datas, 0) / len(self.datas)
                if c < cost:
                    cost = c
                    theta = remote.theta
                    k = remote.k
                    iter = i*n + j
                    print(iter, cost, theta, k)

    def plot(self):
        remote = RemoteStress()
        n = self.__n
        Z = np.zeros(shape=(n,n))
        delta = 1/(n-1)
        for i in range(0, n):
            remote.k = lerp(self.minR, self.maxR, i*delta)
            for j in range(0, n):
                remote.theta = lerp(0, 180, j *delta)
                Z[j][i] = reduce(lambda prev, data: prev + data.cost(remote), self.datas, 0) / len(self.datas) 
        
        X, Y = np.meshgrid(np.linspace(self.minR, self.maxR, n), np.linspace(0, 180, n))
        levels = np.linspace(Z.min(), Z.max(), 20)
        
        cmap = 'jet'
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.contourf(np.linspace(self.minR, self.maxR, n), np.linspace(0, 180, n), Z, levels=levels, cmap=cmap)
        ax.set_xlabel('R')
        ax.set_ylabel('Theta')
        ax.margins(0.2)
        ax.set_title("Domain")
        
        fig.colorbar(plt.cm.ScalarMappable(cmap=cmap), ax=ax, orientation='vertical', label='Cost')
        plt.show()

# ----------------------------------------------------------

solver = MC(10000)
# solver = Grid(100)

def addData(file: str, dataType: str):
    f = open(file, "r")
    for line in f: # each line
        toks = line.removesuffix('\n').split(' ')
        solver.addData( DataFactory.get(dataType, [float(toks[0]), float(toks[1])]) )

addData("matelles-joints.txt", "joint")
addData("matelles-stylolites.txt", "stylolite")

solver.run()
# solver.plot()
