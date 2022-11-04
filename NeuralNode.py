import itertools
import math
from typing import List, Union


class SizeException(Exception):
    def __str__(self):
        return "Load doesn't match input!"


class ReadyException(Exception):
    def __str__(self):
        return "Node is already processed!"


class TypeException(Exception):
    def __str__(self):
        return "Input is not int!"

class NeuralVar:
    def __init__(self, val: int = 0):
        if not isinstance(val, int):
            raise TypeException
        self.val: int = val

    def __str__(self):
        string = "NeuralVar"
        string += "(" + str(self.val) + ")"
        string += "<" + str(id(self)) + ">"
        return string

    def __repr__(self) -> str:
        string = "V(" + str(self.val)+ ")"
        string += "<" + str(id(self)) + ">"
        return string


class NeuralNode:
    def __init__(self, w_input: List[int], b_input: int):
        self.inputs: List[dict] = []
        for weight in w_input:
            self.add_input(NeuralVar(weight))
        self.bias: NeuralVar = NeuralVar(b_input)
        self.sum_value: NeuralVar = NeuralVar()
        self.is_processed: bool = False
        self.output: NeuralVar = NeuralVar()
        self.function = "Step"
        self.label = "NeuralNode"

    def __str__(self) -> str:
        x = self.get_input()
        w = self.get_weights()

        string = self.label
        if self.label != "NeuralNode":
            string += "(X:" + str(x) + ", Y:" + str(
                self.output) + ", S:" + str(self.is_processed) + ")"
        else:
            string += "(X:" + str(x) + ", W:" + str(w) + ", B:" + str(self.bias.val) + ", Y:" + str(
                self.output.val) + ", S:" + str(self.is_processed) + ")"
        # string += "<" + str(id(self)) + ">"
        return string

    def __repr__(self) -> str:
        string = self.label + "(" + str(self.output.val) + ")"
        # string += "<" + str(id(self)) + ">"
        return string

    def reset(self):
        for i in self.inputs:
            i["x"].val = 0
        self.sum_value.val = 0
        self.is_processed = False
        self.output.val = 0

    def get_input(self) -> List[NeuralVar]:
        return [i["x"] for i in self.inputs]

    def get_weights(self):
        return [i["w"] for i in self.inputs]

    def add_input(self, w_input: NeuralVar) -> None:
        self.inputs.append({"x": NeuralVar(0), "w": w_input})

    def get_size(self) -> int:
        return len(self.inputs)

    def load(self, x_input: Union[List[int], List[NeuralVar]]) -> None:
        if len(x_input) != self.get_size():
            raise SizeException
        self.reset()
        for ix, x in enumerate(x_input):
            self.inputs[ix]["x"] = self.validate(x)

    def load_singular(self, pos: int, x_input: Union[int, NeuralVar]) -> None:
        self.reset()
        self.inputs[pos]["x"] = self.validate(x_input)

    def validate(self, x):
        if isinstance(x, int):
            return NeuralVar(x)
        else:
            return x

    def sum(self) -> None:
        r = 0
        for i in self.inputs:
            if isinstance(i["x"], NeuralNode):
                r += i["x"].output.val * i["w"].val
            else:
                r += i["x"].val * i["w"].val
        r += self.bias.val
        self.sum_value = NeuralVar(r)

    def function_linear(self) -> None:
        self.output = self.sum_value

    def function_step(self) -> None:
        if self.sum_value.val <= 0:
            self.output.val = 0
        else:
            self.output.val = 1

    def function_exp(self) -> None:
        self.output.val = 1/(1 + math.exp(-self.sum_value.val))

    def process(self) -> None:
        if self.is_processed:
            raise ReadyException
        safe = True
        for i in self.inputs:
            if isinstance(i["x"], NeuralNode):
                if not i["x"].is_processed:
                    safe = False
        if safe:
            self.sum()
            if self.function == "Linear":
                self.function_linear()
            elif self.function == "Step":
                self.function_step()
            elif self.function == "Step":
                self.function_exp()
            self.is_processed = True

    def binary_test(self) -> None:
        for combo in itertools.product([0, 1], repeat=self.get_size()):
            self.load(combo)
            print("Input:", combo, "Output:", self.output.val)
