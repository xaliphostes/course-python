import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, tan, pi
import random as rnd


def fct(x):
    return x * sin(x * pi / 180) + cos(2 * x * pi / 180)

def findMax(f):
    solution = -10000000
    max = 0
    for i in range(0, 10000):
        x = rnd.uniform(0,720)
        y = f(x)
        if y > max:
            max = y
            solution = x

    print(solution)


x = []
y = []

for i in np.arange(0, 720, 0.1):
    x.append(i)
    y.append(fct(i))

findMax(fct)

fig, ax = plt.subplots()
ax.plot(x, y, label='Joint')
plt.show()

