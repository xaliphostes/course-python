import math

import matplotlib.pyplot as plt

import numpy as np

def costJoint(normal: tuple[float, float], S3: tuple[float, float]):
    return 1 - abs(normal[0]*S3[0] + normal[1]*S3[1])

def costStylolite(normal: tuple[float, float], S3: tuple[float, float]):
    return 1 - costJoint(normal, S3)

def deg2rad(angleInDeg: float) -> float:
    b = math.pi/180
    return angleInDeg * b

def printManyCosts(n: tuple[float, float]):
    for angle in range(0, 91, 5):
        a = deg2rad(angle)
        S3 = [math.cos(a), math.sin(a)]
        print( angle, costJoint(n, S3), costStylolite(n, S3) )


