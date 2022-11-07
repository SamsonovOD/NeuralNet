from NeuralNet import NeuralNet

if __name__ == '__main__':
    net = NeuralNet()
    net.add_node(net.template_not())
    net.binary_test()
    print("NOT net:", net)

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

    # net5 = NeuralNet()
    # net5.add_node(net5.template_and())
    # net5.add_node(net5.template_or())
    # net5.net[0].load_singular(1, net5.net[1])
    # net5.setup_net_inputs()
    #
    # net6 = NeuralNet()
    # net6.add_node(net6.template_and())
    # net6.add_node(net6.template_not())
    # net6.net[1].load_singular(0, net6.net[0])
    # net6.setup_net_inputs()

    # net6.merge_to_input(net5, 0)
    # net6.add_node(net6.tempate_pass())
    # net6.add_node(net6.tempate_pass())
    # net6.node_load(net6.net[2], [net6.net[4], net6.net[5]])
    # net6.node_load(net6.net[3], [net6.net[4], net6.net[5]])
    # print("XOR net:", net6, net6.exits)
    # net5.merge_to_outut(net6, 0)

    # import cv2
    # import numpy as np
    # import matplotlib.pyplot as plt
    #
    # canvas = 255 * np.ones(shape=[512, 512, 3], dtype=np.uint8)
    # cv2.rectangle(canvas, pt1=(200, 200), pt2=(232, 232), color=(0, 0, 0), thickness=1)
    # cv2.putText(canvas, 'OpenCV', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
    # plt.imshow(canvas)
    # plt.show()