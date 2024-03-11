from myTypes import Vector
import RemoteStress
from abc import abstractmethod


class Data:
    n_: Vector

    def __init__(self, n: Vector) -> None: self.n_ = n

    @property
    def n(self):
        return self.n_

    @abstractmethod
    def cost(self, r: RemoteStress) -> float: pass
