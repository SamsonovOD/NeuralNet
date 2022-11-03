import itertools

import NeuralNode
from NeuralNode import *

from typing import List, Dict


class NeuralNet():
    def __init__(self):
        self.net: List[NeuralNode] = []
        self.inputs: List[NeuralVar] = []
        self.exits: List[NeuralNode] = []
        self.is_processed: bool = False

    def __str__(self):
        str = "Net ("
        for node in self.net:
            str += node.__str__() + ", "
        str += ")"
        return str

    def reset(self):
        for node in self.net:
            node.reset()

    def add_node(self, node) -> NeuralNode:
        self.net.append(node)
        self.exits.append(node)
        self.setup_net_inputs()
        self.reset()
        return node

    def get_size(self) -> int:
        return len(self.inputs)

    def setup_net_inputs(self):
        self.inputs: List[NeuralVar] = []
        for node in self.net:
            node_list_inputs = [node_input["x"] for node_input in node.inputs]
            for potential_input in node_list_inputs:
                if isinstance(potential_input, NeuralVar):
                    self.inputs.append(potential_input)

    def load(self, x_input: List[int]):
        if len(x_input) != self.get_size():
            raise SizeException
        self.reset()
        for ix, x in enumerate(x_input):
            if isinstance(x, int):
                self.inputs[ix].val = x
            elif isinstance(x, NeuralVar):
                self.inputs[ix] = x
        self.is_processed = False

    def node_load(self, node: NeuralNode, x_input: Union[List[int], List[NeuralVar], List[NeuralNode]]) -> None:
        node.load(x_input)
        self.setup_net_inputs()
        for x in x_input:
            if isinstance(x, NeuralNode):
                if x in self.exits:
                    self.exits.remove(x)

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
                if node.is_processed == False:
                    node.process()

    def binary_test(self) -> None:
        for combo in itertools.product([0, 1], repeat=self.get_size()):
            self.load(combo)
            self.process()
            print("Input:", combo, "Output:", self.get_output())

    def get_output(self) -> str:
        str = [node.output.val for node in self.exits]
        return str

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

if __name__ == '__main__':
    # net = NeuralNet()
    # net.add_node(net.template_not())
    # net.binary_test()
    # print("NOT net:", net)
    #
    # net2 = NeuralNet()
    # net2.add_node(net2.template_or())
    # net2.binary_test()
    # print("OR net:", net2)
    #
    # net3 = NeuralNet()
    # net3.add_node(net3.template_and())
    # net3.binary_test()
    # print("AND net:", net3)
    #
    # net4 = NeuralNet()
    # net4.template_xor()
    # net4.binary_test()
    # print("XOR net:", net4)

    net5 = NeuralNet()
    net5.add_node(net5.template_and())
    net5.add_node(net5.template_or())
    net5.net[0].load_singular(1, net5.net[1])

    net6 = NeuralNet()
    net6.add_node(net6.template_and())
    net6.add_node(net6.template_not())
    net6.net[1].load_singular(0, net6.net[0])

    # net5.merge_to_input(net6, 0)
    # net5.add_node(net5.tempate_pass())
    # net5.add_node(net5.tempate_pass())
    # net5.node_load(net5.net[1], [net5.net[4], net5.net[5]])
    # net5.node_load(net5.net[2], [net5.net[4], net5.net[5]])
    print("XOR net:", net6, net6.exits)