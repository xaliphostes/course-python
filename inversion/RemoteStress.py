from myTypes import Vector
from tools import normalize
import math


class RemoteStress:
    __S1: Vector
    __S3: Vector

    @property
    def S1(self) -> Vector:
        return self.__S1

    @property
    def S3(self) -> Vector:
        return self.__S3

    def set(self, theta: float, k: float) -> None:
        a = math.radians(theta)
        c, s = math.cos(a), math.sin(a)
        xx, xy, yy = k * s * s, k * c * s, k * c * c
        trace = xx + yy
        discri = math.sqrt(trace * trace - 4 * (xx * yy - xy * xy))
        # Decreasing order according to the eigen values
        self.__S1 = normalize([xy, (trace + discri) / 2 - xx])
        self.__S3 = normalize([xy, (trace - discri) / 2 - xx])