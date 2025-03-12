import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, pi


def fct(x):
    return x * sin(x * pi / 180) + cos(2 * x * pi / 180)

x = []
y = []

for i in np.arange(0, 720, 0.1):
    x.append(i)
    y.append(fct(i))

fig, ax = plt.subplots()
ax.plot(x, y, label='Joint')
plt.show()

