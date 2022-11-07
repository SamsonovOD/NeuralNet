import NeuralNode
from NeuralNode import *


class NeuralNet:
    net: List[NeuralNode] = []
    inputs: List[NeuralVar] = []
    exits: List[NeuralNode] = []

    def __init__(self):
        pass

    def __str__(self) -> str:
        string = "Net ("
        for node in self.net:
            string += str(node) + ", "
        string += ")"
        return string

    def reset(self) -> None:
        for node in self.net:
            node.reset()
        self.setup_net_inputs()

    def add_node(self, node) -> NeuralNode:
        self.net.append(node)
        self.reset()
        return node

    def get_input_size(self) -> int:
        return len(self.inputs)

    def setup_net_inputs(self):
        self.inputs.clear()
        self.exits = self.net.copy()
        for node in self.net:
            node_list_inputs = node.get_inputs()
            for potential_input in node_list_inputs:
                if isinstance(potential_input, NeuralVar):
                    self.inputs.append(potential_input)
                if isinstance(potential_input, NeuralNode):
                    if potential_input in self.exits:
                        self.exits.remove(potential_input)

    def load(self, x_input: List[int]):
        if len(x_input) != self.get_input_size():
            raise SizeException
        self.reset()
        for ix, x in enumerate(x_input):
            if isinstance(x, int):
                self.inputs[ix].__val__ = x
            elif isinstance(x, NeuralVar):
                self.inputs[ix] = x

    def node_load(self, node: NeuralNode, x_input: Union[List[int], List[NeuralVar], List[NeuralNode]]) -> None:
        node.set_inputs(x_input)
        self.setup_net_inputs()

    def tempate_pass(self) -> NeuralNode:
        node = NeuralNode([1], 0)
        return node

    def template_not(self) -> NeuralNode:
        node = NeuralNode([-1], 1)
        node.label = "NOT"
        return node

    def template_or(self) -> NeuralNode:
        node = NeuralNode([1, 1], 0)
        node.label = "OR"
        return node

    def template_and(self) -> NeuralNode:
        node = NeuralNode([1, 1], -1)
        node.label = "AND"
        return node

    def template_xor(self) -> List[NeuralNode]:
        x1 = self.add_node(self.tempate_pass())
        x2 = self.add_node(self.tempate_pass())
        n1 = self.add_node(NeuralNode([-1, 1], 0))
        n2 = self.add_node(NeuralNode([1, -1], 0))
        n3 = self.add_node(self.template_or())
        x1.label = "X1"
        x2.label = "X2"
        self.node_load(n1, [x1, x2])
        self.node_load(n2, [x1, x2])
        self.node_load(n3, [n1, n2])
        return self.net

    def process(self):
        process_check = [False] * len(self.net)
        while False in process_check:
            process_check = [node.is_processed for node in self.net]
            for node in self.net:
                if not node.is_processed:
                    node.process()

    def binary_test(self) -> None:
        for combo in itertools.product([0, 1], repeat=self.get_input_size()):
            self.load(combo)
            self.process()
            print("Input:", combo, "Output:", self.get_output())

    def get_output(self) -> List[float]:
        string = [node.output.__val__ for node in self.exits]
        return string

    def merge_to_output(self, second_net, pos):
        self.net += second_net.net
        self.exits[0].output = second_net.inputs[pos]
        self.reset()
        second_net.net.clear()
        return self.net

    def merge_to_input(self, second_net, pos):
        self.net += second_net.net
        second_net.exits[0].output = self.inputs[pos]
        self.reset()
        second_net.net.clear()
        return self.net
