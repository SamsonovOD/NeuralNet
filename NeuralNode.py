import itertools
import math
from typing import List, Union, Dict

from NeuralExceptions import *
from NeuralVal import NeuralVar


class NeuralNode:
    inputs: List[Dict[str, NeuralVar]] = []
    bias: NeuralVar = NeuralVar()
    sum_value: NeuralVar = NeuralVar()
    is_processed: bool = False
    output: NeuralVar = NeuralVar()
    function: str = "Step"
    label: str = "NeuralNode"

    def __init__(self, w_input: List[Union[int, float]], bias: Union[int, float]):
        for w in w_input:
            self.add_input()
        self.set_weights(w_input)
        self.set_bias(bias)

    def __str__(self) -> str:
        x = self.get_inputs()
        w = self.get_weights()

        string = self.label
        if self.label != "NeuralNode":
            string += "(X:" + str(x) + ", Y:" + str(
                self.output) + ", S:" + str(self.is_processed) + ")"
        else:
            string += "(X:" + str(x) + ", W:" + str(w) + ", B:" + str(self.bias.__val__) + ", Y:" + str(
                self.output.__val__) + ", S:" + str(self.is_processed) + ")"
        # string += "<" + str(id(self)) + ">"
        return string

    def __repr__(self) -> str:
        string = self.label + "(" + str(self.output.__val__) + ")"
        # string += "<" + str(id(self)) + ">"
        return string

    def get_id(self) -> str:
        return str(id(self))

    def reset(self):
        for i in self.inputs:
            i["x"].__val__ = 0
        self.sum_value.__val__ = 0
        self.is_processed = False
        self.output.__val__ = 0

    def get_input_size(self) -> int:
        return len(self.inputs)

    def validate_input_size(self, inputs: List):
        if len(inputs) != self.get_input_size():
            raise SizeException
        else:
            return inputs

    def add_input(self) -> Dict[str, NeuralVar]:
        input_p = {"x": NeuralVar(0), "w": NeuralVar(0)}
        self.inputs.append(input_p)
        return input_p

    def get_weights(self) -> List[NeuralVar]:
        return [i["w"] for i in self.inputs]

    def get_weight(self, ix: int) -> NeuralVar:
        return self.inputs[ix]["w"]

    def set_weights(self, w_input: List[Union[int, float]]):
        self.validate_input_size(w_input)
        for ix, weight in enumerate(w_input):
            self.get_weights()[ix] = NeuralVar(w_input[ix])

    def set_weight(self, ix: int, w_input: Union[int, float]):
        self.get_weights()[ix] = NeuralVar(w_input)

    def adjust_weights(self, w_input: List[Union[int, float]]):
        self.validate_input_size(w_input)
        for ix, weight in enumerate(w_input):
            self.get_weights()[ix].set(w_input[ix])

    def adjust_weight(self, ix: int, w_input: List[Union[int, float]]):
        self.validate_input_size(w_input)
        self.get_weights()[ix].set(w_input[ix])

    def get_bias(self) -> NeuralVar:
        return self.bias

    def set_bias(self, bias: Union[int, float]):
        self.bias = NeuralVar(bias)

    def adjust_bias(self, bias: Union[int, float]):
        self.bias.set(bias)

    def validate_var(self, x):
        if isinstance(x, (int, float)):
            return NeuralVar(x)
        else:
            return x

    def get_inputs(self) -> List[NeuralVar]:
        return [i["x"] for i in self.inputs]

    def get_input(self, ix: int) -> NeuralVar:
        return self.inputs[ix]["x"]

    def set_inputs(self, x_input: Union[List[int], List[NeuralVar]]) -> None:
        self.validate_input_size(x_input)
        for ix, x in enumerate(x_input):
            self.inputs[ix]["x"] = self.validate_var(x_input[ix])

    def set_input(self, ix: int, x_input: Union[int, NeuralVar]) -> None:
        self.inputs[ix]["x"] = self.validate_var(x_input)

    def sum(self) -> None:
        r = 0
        for i in self.inputs:
            r += i["x"].get() * i["w"].get()
        r += self.bias.get()
        self.sum_value = NeuralVar(r)

    def function_linear(self) -> None:
        self.output = self.sum_value

    def function_step(self) -> None:
        if self.sum_value.get() <= 0:
            self.output.set(0)
        else:
            self.output.set(1)

    def function_exp(self) -> None:
        self.output.__val__ = 1 / (1 + math.exp(-self.sum_value.get()))

    def process(self) -> None:
        if self.is_processed:
            raise ReadyException
        self.sum()
        if self.function == "Linear":
            self.function_linear()
        elif self.function == "Step":
            self.function_step()
        elif self.function == "Step":
            self.function_exp()
        self.is_processed = True

    def binary_test(self) -> None:
        for combo in itertools.product([0, 1], repeat=self.get_input_size()):
            self.set_inputs(combo)
            print("Input:", combo, "Output:", self.output.__val__)