import math
import random as rnd
import numpy as np


def deg2rad(a):
    return a * math.pi / 180


def normalize(n):
    l = math.sqrt(n[0] ** 2 + n[1] ** 2)
    if l != 0:
        return [n[0] / l, n[1] / l]
    else:
        return n


def dot(n1, n2):
    return n1[0] * n2[0] + n1[1] * n2[1]


def principalDirections(theta, k):
    a = deg2rad(theta)
    c, s = math.cos(a), math.sin(a)
    xx, xy, yy = k * s * s, k * c * s, k * c * c

    # # A la mano
    trace = xx + yy
    discri = math.sqrt(trace * trace - 4 * (xx * yy - xy * xy))
    # Decreasing order according to the eigen values
    s1 = normalize([xy, (trace + discri) / 2 - xx])
    s3 = normalize([xy, (trace - discri) / 2 - xx])
    return [s1, s3]





def costJoint(n, r):
    return 1.0 - math.fabs(dot(n, r[1]))

def costStylo(n, r):
    return 1.0 - costJoint(n,r[1])


allData = []


def readData(filename, typeOfData):
    """
    typeOfData: 0 for Joint, 1 for Stylolite, 2 for Dyke...
    """
    f = open(filename, "r")
    for line in f:
        tokens = line.split(' ')  # c'est un tableau de str
        nx = float(tokens[0])
        ny = float(tokens[1])
        data = [nx, ny, typeOfData]
        allData.append(data)


def monteCarlo(numberOfSimulations):
    theta = 0
    ratio = 0
    cost = 100000

    for i in range(0, numberOfSimulations):
        t = rnd.uniform(0, 180)
        k = rnd.uniform(0, 1)
        dirs = principalDirections(t, k)
        c = 0

        for fracture in allData:
            normal = [fracture[0], fracture[1]]
            fractureType = fracture[2]
            if fractureType == 0:  # it is a joint
                c = c + costJoint(normal, dirs)
            else:
                c = c + costStylo(normal, dirs)
        
        c = c / len(allData)
        if c < cost:
            theta = t
            ratio = k
            cost = c
    
    print('solution: ')
    print('  cost  =', round(cost, 4))
    print('  theta =', round(theta))
    print('  ratio =', round(ratio, 2))


# ------------------- code principal -------------------------------

readData("data/matelles-joints.txt", 0)
readData("data/matelles-stylolites.txt", 1)

monteCarlo(5000)
