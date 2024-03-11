from RemoteStress import RemoteStress
from Joint import Joint
from Stylolite import Stylolite
import matplotlib.pyplot as plt
import math


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
