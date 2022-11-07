from typing import Union

from NeuralExceptions import *


class NeuralVar:
    __val__: float = 0.0

    def __init__(self, val: Union[int, float] = 0):
        self.set(val)

    def validate(self, val) -> float:
        if not isinstance(val, (int, float)):
            raise TypeException
        else:
            return float(val)

    def set(self, val: int) -> None:
        self.__val__ = self.validate(val)

    def get(self) -> float:
        return self.__val__

    def get_ptr(self) -> str:
        return str(id(self))

    def __str__(self) -> str:
        string = "NeuralVar"
        string += "(" + str(self.get()) + ")"
        string += "<" + self.get_ptr() + ">"
        return string

    def __repr__(self) -> str:
        string = "V(" + str(self.get()) + ")"
        string += "<" + self.get_ptr() + ">"
        return string
