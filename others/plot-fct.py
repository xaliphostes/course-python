import matplotlib.pyplot as plt
import numpy as np

def fct(x): return x**4 - 2*x**2 - 5*x + 6

x = []
y = []

for i in np.arange(-3, 3, 0.1):
    x.append(i)
    y.append(fct(i))

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()
