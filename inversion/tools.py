from myTypes import Vector, Stress
import math


def dot(n1: Vector, n2: Vector) -> float:
    return n1[0] * n2[0] + n1[1] * n2[1]


def lerp(v0: float, v1: float, t: float) -> float:
    return (1 - t) * v0 + t * v1


def normalize(n: Vector) -> Vector:
    l = math.sqrt(n[0] ** 2 + n[1] ** 2)
    if l != 0:
        return [n[0] / l, n[1] / l]
    else:
        return n
