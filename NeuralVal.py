from typing import Union

from NeuralExceptions import *


class NeuralVar:
    __val__: float = 0.0

    def __init__(self, val: Union[int, float] = 0):
        self.__val__ = val

    @property
    def val(self) -> float:
        """

        :rtype: object
        """
        return self.__val__

    @val.setter
    def val(self, val: Union[int, float]) -> None:
        """

        :param val:
        """
        if not isinstance(val, (int, float)):
            raise TypeException
        else:
            self.__val__ = float(val)

    def get_ptr(self) -> str:
        """

        :return:
        """
        return str(id(self))

    def __str__(self) -> str:
        """

        :return:
        """
        string = "V"
        string += "(" + str(self.val) + ")"
        # string += "<" + self.get_ptr() + ">"
        return string

    def __repr__(self) -> str:
        """

        :return:
        """
        string = "V(" + str(self.val) + ")"
        # string += "<" + self.get_ptr() + ">"
        return string
