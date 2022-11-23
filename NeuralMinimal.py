import numpy as np
import matplotlib.pyplot as plt

class NeuralNetMinimal:
    def __init__(self):
        self.layers = []

    def add_layer(self, nodes, pos):
        if pos == 0:
            w_mat = [{"w": [1] * 1, "b": 1} for i in range(nodes)]
            self.layers.insert(pos, w_mat)

            if len(self.layers) > 1:
                w_mat = [{"w": [1] * nodes, "b": 1} for i in range(len(self.layers[pos+1]))]
                self.layers[pos + 1] = w_mat

        elif pos != 0 and len(self.layers) != 0:
            w_mat = [{"w": [1] * len(self.layers[pos-1]), "b": 1} for i in range(nodes)]
            self.layers.insert(pos + 1, w_mat)

    def randomize(self):
        for layer in range(1, len(self.layers)):
            for node in self.layers[layer]:
                for w in range(len(node["w"])):
                    node["w"][w] = np.random.rand()
                node["b"] = np.random.rand()

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def der_sigmoid(self, x):
        return self.sigmoid(x)*(1-self.sigmoid(x))

    def act_func(self, w, x, b):
        m_x = np.matrix(x)
        m_w = np.matrix(w).T
        m_b = np.matrix(b)
        return self.sigmoid(np.dot(m_x, m_w) + m_b)

    def forward(self, x, layer):
        w = [node["w"] for node in self.layers[layer]]
        b = [node["b"] for node in self.layers[layer]]
        result = self.act_func(w, x, b)
        return result

    def process(self, x):
        y_pred = self.forward(x, 0)
        for layer in range(1, len(self.layers)):
            y_pred = self.forward(y_pred, layer)
        return y_pred

    def train(self, x_test, y_true, epochs):
        for i in range(epochs):
            y_pred_total = []
            for x, y in zip(x_test, y_true):
                print("EXPECT:", x, "=", y)
                y_pred = self.process(x)
                print("GET:", x, "=", y_pred)
                pass

                der = y_pred * (1-y_pred)
                loss = (y_pred - y) * der

                y_pred_total.append(y_pred)

                # for layer in range(1, len(self.layers)):
                #     for node in self.layers[layer]:
                #         for w in range(len(node["w"])):
                #             node["w"][w] -= 0.00001
                        # node["b"] = np.random.rand()
            #     y_pred.append(r)
            #
            #     s1 = np.power(r-y, 2)
            #     loss = np.sqrt(s1 / 2)
            #     # # loss = mse(y_true, results)
            #     print("LOSS:", loss)
            #     for layer in range(1, len(self.layers)):
            #         for node in self.layers[layer]:
            #             for w in range(len(node["w"])):
            #                 mean = loss * node["w"][w] / sum(node["w"])
            #                 node["w"][w] -= mean
            #             node["b"] /= loss
            #
            plt.scatter(x_test, y_pred_total)
            plt.show()


def mse(y_true, y_pred):
    y_true = [y+1 for y in y_true]
    y_pred = [y+1 for y in y_pred]
    loss = np.mean(np.sqrt(np.log(y_true) - np.log(y_pred)))
    return loss

def test_func(x):
#     return np.power(2*x-4, 3)+5
    return np.power(x, 4)

def math_test(input_count):
    value_limit = 10
    offset = 2
    test_inuput = [[np.random.uniform(-value_limit + offset, value_limit + offset)] for i in range(input_count)]
    test_output = test_func(test_inuput)
    return test_inuput, test_output

if __name__ == '__main__':
    input_count = 100
    x, y_true = math_test(input_count)

    # plt.scatter(x, y_true)
    # plt.show()

    net = NeuralNetMinimal()
    net.add_layer(1, 0)
    net.add_layer(3, 1)
    net.add_layer(3, 2)
    net.add_layer(1, 3)
    net.add_layer(1, 4)
    net.randomize()
    net.train(x, y_true, 10)
