import itertools
import math
from typing import List, Union, Dict, Any

from NeuralExceptions import *
from NeuralVal import NeuralVar


class NeuralNode:
    def __init__(self, w_input: List[Union[int, float]], bias: Union[int, float]):
        self.inputs: List[Dict[str, NeuralVar]] = []
        self.bias: NeuralVar = NeuralVar()
        self.sum_value: NeuralVar = NeuralVar()
        self.is_processed: bool = False
        self.output: NeuralVar = NeuralVar()
        self.function: str = "Step"
        self.label: str = "NeuralNode"
        for w in w_input:
            self.add_input(w)
        self.set_bias(bias)

    def __str__(self) -> str:
        """

        :return:
        """
        x = self.get_inputs()
        w = self.get_weights()

        string = self.label
        if self.label == "NeuralNode":
            string += "(X:" + str(x)
            string += ", W:" + str(w)
            string += ", B:" + str(self.bias)
            string += ", Y:" + str(self.output)
            string += ", S:" + str(self.is_processed) + ")"
        else:
            string += "(X:" + str(x)
            string += ", Y:" + str(self.output) + ")"
        # string += "<" + str(id(self)) + ">"
        return string

    def __repr__(self) -> str:
        """

        :return:
        """
        string = self.label + "(" + str(self.output.val) + ")"
        # string += "<" + str(id(self)) + ">"
        return string

    @property
    def val(self) -> float:
        """

        :return:
        """
        return self.output.val

    def get_id(self) -> str:
        """

        :return:
        """
        return str(id(self))

    def reset(self) -> None:
        """

        """
        # for i in self.inputs:
        #     i["x"].set(0)
        self.sum_value.val = 0
        self.is_processed = False
        self.output.val = 0

    def get_input_size(self) -> int:
        """

        :return:
        """
        return len(self.inputs)

    def validate_var(self, x: Any) -> Union[NeuralVar]:
        """

        :param x:
        :return:
        """
        if isinstance(x, (int, float)):
            return NeuralVar(x)
        else:
            return x

    def validate_input_size(self, inputs: List) -> List:
        """

        :param inputs:
        :return:
        """
        if len(inputs) != self.get_input_size():
            raise SizeException
        else:
            return inputs

    def add_input(self, w_input: Union[int, float]) -> Dict[str, NeuralVar]:
        """

        :param w_input:
        :return:
        """
        input_p = {"x": NeuralVar(0), "w": NeuralVar(w_input)}
        self.inputs.append(input_p)
        return input_p

    def get_weights(self) -> List[NeuralVar]:
        """

        :return:
        """
        return [i["w"] for i in self.inputs]

    def get_weight(self, ix: int) -> NeuralVar:
        """

        :param ix:
        :return:
        """
        return self.inputs[ix]["w"]

    def set_weights(self, w_input: List[Union[int, float]]) -> None:
        """

        :rtype: object
        """
        self.validate_input_size(w_input)
        for ix, weight in enumerate(w_input):
            self.get_weights()[ix].val = w_input[ix]

    def set_weight(self, ix: int, w_input: Union[int, float]) -> None:
        """

        :rtype: object
        """
        self.get_weights()[ix] = NeuralVar(w_input)

    def adjust_weights(self, w_input: List[Union[int, float]]) -> None:
        """

        :rtype: object
        """
        self.validate_input_size(w_input)
        for ix, weight in enumerate(w_input):
            self.get_weights()[ix].val = w_input[ix]

    def adjust_weight(self, ix: int, w_input: List[Union[int, float]]) -> None:
        """

        :rtype: object
        """
        self.validate_input_size(w_input)
        self.get_weights()[ix].val = w_input[ix]

    def get_bias(self) -> NeuralVar:
        """

        :return:
        """
        return self.bias

    def set_bias(self, bias: Union[int, float]):
        """

        :rtype: object
        """
        self.bias = NeuralVar(bias)

    def adjust_bias(self, bias: Union[int, float]):
        """

        :rtype: object
        """
        self.bias.val = bias

    def get_inputs(self) -> List[NeuralVar]:
        """

        :return:
        """
        return [i["x"] for i in self.inputs]

    def get_input(self, ix: int) -> NeuralVar:
        """

        :rtype: object
        """
        return self.inputs[ix]["x"]

    def set_inputs(self, x_input: Union[List[int], List[NeuralVar]]) -> None:
        """

        :param x_input:
        """
        self.validate_input_size(x_input)
        for ix, x in enumerate(x_input):
            self.inputs[ix]["x"] = self.validate_var(x_input[ix])

    def set_input(self, ix: int, x_input: Union[int, NeuralVar]) -> None:
        """

        :param ix:
        :param x_input:
        """
        self.inputs[ix]["x"] = self.validate_var(x_input)

    def sum(self) -> None:
        """

        """
        r = 0
        for i in self.inputs:
            r += i["x"].val * i["w"].val
        r += self.bias.val
        self.sum_value.val = r

    def activation_function(self) -> None:
        """

        """
        n_sum = self.sum_value.val
        if self.function == "Linear":
            self.output.val = n_sum
        elif self.function == "Step":
            if n_sum <= 0:
                self.output.val = 0
            else:
                self.output.val = 1
        elif self.function == "Relu":
            if n_sum <= 0:
                self.output.val = 0
            else:
                self.output.val = n_sum
        elif self.function == "Tanh":
            n_tanh = math.tanh(n_sum)
            self.output.val = n_tanh
        elif self.function == "Sigmoid":
            n_exp = 1 / (1 + math.exp(-n_sum))
            self.output.val = n_exp

    def process(self) -> None:
        """

        """
        if self.is_processed:
            raise ReadyException
        self.sum()
        self.activation_function()
        self.is_processed = True

    def binary_test(self) -> None:
        """

        """
        for combo in itertools.product([0, 1], repeat=self.get_input_size()):
            self.set_inputs(combo)
            print("Input:", combo, "Output:", self.output.val)
