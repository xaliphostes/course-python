import Data
import random as rnd
import functools
from RemoteStress import RemoteStress
from tools import lerp


# Simulation aléatoire pour trouver la solution
def monteCarlo(data: list[Data], n: int = 5000):
    """ Monte Carlo simulation (random)

    Args:
        data (list[Data]): a list of Data
        n (int, optional): The number of random simulations. Defaults to 5000.
    """
    cost, theta, k = 1e9, 0, 0
    remote = RemoteStress()
    for i in range(0, n):
        theta_, k_ = lerp(0, 180, rnd.random()), lerp(0, 1, rnd.random())
        remote.set(theta_, k_)
        c = functools.reduce(lambda a, b: a + b, [x.cost(remote) for x in data], 0) / len(data)
        if c < cost:
            cost, theta, k = c, theta_, k_
            print(theta, k, c)
