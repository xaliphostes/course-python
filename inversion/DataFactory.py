import Data
from Joint import Joint
from Stylolite import Stylolite
from myTypes import Vector


def create(name: str, n: Vector) -> Data:
    if name == 'joint' or name == 'dike' or name == 'dyke':
        return Joint(n)
    elif name == 'stylolite':
        return Stylolite(n)
    else:
        raise Exception('data type {dataType} is unknown!')
