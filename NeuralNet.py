import NeuralNode
from NeuralGraph import NeuralGraph
from NeuralNode import *


class NeuralNet:

    def __init__(self):
        self.net: List[NeuralNode] = []
        self.inputs: List[NeuralVar] = []
        self.exits: List[NeuralNode] = []
        self.graph = NeuralGraph()
        self.layers = []

    def __str__(self) -> str:
        string = "Net ("
        for node in self.net:
            string += str(node) + ", "
        string += ")"
        return string

    def clear(self):
        self.net.clear()
        self.inputs.clear()
        self.exits.clear()
        self.layers = []

    def reset(self) -> None:
        for node in self.net:
            node.reset()
        self.setup_net_inputs()

    def get_input_size(self) -> int:
        return len(self.inputs)

    def add_new_layer(self, node):
        self.layers.append([])
        self.net.append(node)
        self.layers[-1].append(node)
        self.reset()
        return node

    def add_to_layer(self, node, layer):
        while layer >= len(self.layers):
            self.layers.append([])
        self.net.append(node)
        self.layers[layer].append(node)
        self.reset()
        return node

    def setup_net_inputs(self):
        self.inputs.clear()
        for n in self.layers[0]:
            for i in n.get_inputs():
                self.inputs.append(i)
        self.exits.clear()
        for n in self.layers[-1]:
            self.exits.append(n.output)

    def load(self, x_input: List[int]):
        if len(x_input) != self.get_input_size():
            raise SizeException
        self.reset()
        for ix, x in enumerate(x_input):
            if isinstance(x, int):
                self.inputs[ix].val = x
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
        x1 = self.add_to_layer(self.tempate_pass(), 0)
        x2 = self.add_to_layer(self.tempate_pass(), 0)
        n1 = self.add_to_layer(NeuralNode([-1, 1], 0), 1)
        n2 = self.add_to_layer(NeuralNode([1, -1], 0), 1)
        n3 = self.add_to_layer(self.template_or(), 2)
        x1.label = "X1"
        x2.label = "X2"
        self.node_load(n1, [x1, x2])
        self.node_load(n2, [x1, x2])
        self.node_load(n3, [n1, n2])
        return self.net

    def get_output(self) -> List[float]:
        string = [node.output.val for node in self.exits]
        return string

    def process(self):
        process_check = [False] * len(self.net)
        while False in process_check:
            process_check = [node.is_processed for node in self.net]
            for node in self.net:
                if not node.is_processed:
                    node.process()

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

    def binary_test(self):
        for combo in itertools.product([0, 1], repeat=self.get_input_size()):
            self.load(combo)
            self.process()
            self.graph.graph_test(self)
            print("Input:", combo, "Output:", self.exits)
