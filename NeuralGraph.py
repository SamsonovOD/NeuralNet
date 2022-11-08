import cv2
import numpy as np
from matplotlib import pyplot as plt

from NeuralNode import NeuralNode


class GraphNode:
    def __init__(self, node, position):
        self.node: NeuralNode = node
        self.position = position
        self.color = (0, 0, 0)

    def tuple_offest(self, tuple1: tuple, tulpe2: tuple) -> tuple:
        """

        :param tuple1:
        :param tulpe2:
        :return:
        """
        return tuple(map(lambda i, j: i + j, tuple1, tulpe2))

    def draw_rect(self, cv, pos, size) -> None:
        """

        :param cv:
        :param pos:
        :param size:
        """
        point2 = self.tuple_offest(pos, size)
        cv2.rectangle(cv, pt1=pos, pt2=point2, color=self.color, thickness=1)

    def draw_circle(self, cv, pos) -> None:
        """

        :param cv:
        :param pos:
        """
        cv2.circle(cv, pos, 4, self.color, 1)

    def draw_text(self, cv, pos, text) -> None:
        """

        :param cv:
        :param pos:
        :param text:
        """
        cv2.putText(cv, str(text), pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color, 1, cv2.LINE_AA)

    def get_input_port(self) -> tuple:
        """

        :return:
        """
        return self.tuple_offest(self.position, (0, 16))

    def get_output_port(self) -> tuple:
        """

        :return:
        """
        return self.tuple_offest(self.position, (32, 16))

    def draw_node(self, cv) -> None:
        """

        :rtype: object
        """
        # size = (32, 32 * self.node.get_input_size())
        size = (32, 32)
        self.draw_rect(cv, self.position, size)
        self.draw_text(cv, self.tuple_offest(self.position, (8, 0)), self.node.get_bias().val)
        self.draw_text(cv, self.tuple_offest(self.position, (-4, 16 + size[1])), self.node.label)

        # for ix, w in enumerate(self.node.get_weights()):
        #     self.draw_text(cv, self.tuple_offest(self.position, (-32, 8 + 32 * ix)), w.val)
        #     self.draw_circle(cv, self.tuple_offest(self.position, (0, 16 + 32 * ix)))
        self.draw_circle(cv, self.get_input_port())

        self.draw_text(cv, self.tuple_offest(self.position, (32, 8)), self.node.output.val)
        self.draw_circle(cv, self.get_output_port())


class NeuralGraph:

    def __init__(self):
        self.nodes = []

    def graph_test(self, net) -> None:
        """

        :param net:
        """
        canvas = 255 * np.ones(shape=[100 + 100 * len(net.layers), 100 + 100 * len(net.layers), 3], dtype=np.uint8)
        x_offset = 100
        for l in net.layers:
            y_offest = 100
            for n in l:
                gn = GraphNode(n, (x_offset, y_offest))
                gn.draw_node(canvas)
                y_offest += 100
            x_offset += 100

        # gn0 = GraphNode(net.net[0], (100, 200))
        # gn1 = GraphNode(net.net[1], (100, 300))
        # gn2 = GraphNode(net.net[2], (200, 200))
        # gn3 = GraphNode(net.net[3], (200, 300))
        # gn4 = GraphNode(net.net[4], (300, 200))
        # gn0.draw_node(canvas)
        # gn1.draw_node(canvas)
        # gn2.draw_node(canvas)
        # gn3.draw_node(canvas)
        # gn4.draw_node(canvas)
        #
        # fig = plt.figure()
        # plot = fig.add_subplot(111)
        #
        # def on_plot_hover(event):
        #     for l in plot.get_lines():
        #         if l.contains(event)[0]:
        #             print(l.get_gid())
        #             # annot.set_visible(True)
        #             annot = plot.annotate("Line", (gn2.position[0], gn2.position[1] + 16))
        #             fig.canvas.draw_idle()
        #         else:
        #             # annot.set_visible(False)
        #             fig.canvas.draw_idle()
        #
        # # annot.set_visible(False)
        # fig.canvas.mpl_connect('motion_notify_event', on_plot_hover)
        #
        # # plot.plot([gn0.position[0] + 32, gn2.position[0]], [gn0.position[1] + 16, gn2.position[1] + 16], 'o', color='black', linestyle="--", gid=1)
        # # plot.plot([gn0.position[0] + 32, gn3.position[0]], [gn0.position[1] + 16, gn3.position[1] + 16], 'o', color='black', linestyle="--", gid=2)
        # # plot.plot([gn1.position[0] + 32, gn2.position[0]], [gn1.position[1] + 16, gn2.position[1] + 16], 'o', color='black', linestyle="--", gid=3)
        # # plot.plot([gn1.position[0] + 32, gn3.position[0]], [gn1.position[1] + 16, gn3.position[1] + 16], 'o', color='black', linestyle="--", gid=4)
        # # plot.plot([gn2.position[0] + 32, gn4.position[0]], [gn2.position[1] + 16, gn4.position[1] + 16], 'o', color='black', linestyle="--", gid=5)
        # # plot.plot([gn3.position[0] + 32, gn4.position[0]], [gn3.position[1] + 16, gn4.position[1] + 16], 'o', color='black', linestyle="--", gid=6)
        #
        plt.imshow(canvas)
        plt.ion()
        plt.pause(1)
        # plt.close()
