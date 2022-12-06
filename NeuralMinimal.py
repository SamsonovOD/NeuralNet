import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

import NeuralSample
import NeuralFunctions

def rand_f()  -> float:
    return np.random.rand()*2 -1

def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-x))

def d_sigmoid(x: float) -> float:
    return sigmoid(x) * (1 - sigmoid(x))

def mse_loss(y_true: list, y_pred: list) -> float:
    return ((y_true - y_pred) ** 2).mean()

class NeuralNetMinimal:
    def __init__(self):
        self.layers = []

    def add_layer(self, neurons: int, pos: int, function: str):
        neuron_array = [{"w": [1], "b": 1, "f": function} for _ in range(neurons)]
        self.layers.insert(pos, neuron_array)
        self.insert_adjust()
        self.randomize()

    def insert_adjust(self):
        for idx, layer in enumerate(self.layers):
            if idx != 0:
                prev_size = len(self.layers[idx-1])
                for neuron in layer:
                    if len(neuron["w"]) < prev_size:
                        while len(neuron["w"]) < prev_size:
                            neuron["w"].append(rand_f())
                    else:
                        neuron["w"] = neuron["w"][:prev_size]

    def randomize(self):
        for layer in self.layers[1:]:
            for neuron in layer:
                for w in range(len(neuron["w"])):
                    neuron["w"][w] = rand_f()
                neuron["b"] = rand_f()

    def forward(self, x, layer):
        w = [node["w"] for node in layer]
        b = [node["b"] for node in layer]
        m_x = np.vstack(x)
        m_w = np.matrix(w)
        m_b = np.vstack(b)
        m_sum = np.dot(m_w, m_x) + m_b
        y = sigmoid(m_sum)
        return y

    def predict(self, x_test):
        y_pred = []
        for x in x_test:
            y = x
            for layer in self.layers[1:]:
                y = self.forward(y, layer)
            y_pred.append(y)
        return y_pred

    def backward(self, loss, lr, x, layer):
        w = [node["w"] for node in layer]
        m_x = np.matrix(x)
        m_w = np.matrix(w)
        input_error = np.dot(loss, m_w)
        weights_error = np.dot(m_x.T, loss)
        for idx, node in enumerate(layer):
            for w in range(len(node["w"])):
                node["w"][w] -= lr * weights_error.tolist()[0][idx]
            node["b"] -= lr * loss.tolist()[0][idx]
        return input_error

    def train(self, x_train, y_true, epochs, lr):
        for e in range(epochs):
            for x, y in zip(x_train, y_true):
                print(x)
                y_pred = self.predict(x)
                dy = -2 * (y - y_pred)
                for layer in reversed(self.layers[1:]):
                    for node in layer:
                        print(node)
            # print(x_train, y_pred)
            # print(x_train, y_true)
            err = 0
            #     output = x
            #     for layer in self.layers:
            #         output = self.forward(output, layer)
            #     err += self.loss_mse(y, output)
            #     error = self.deriv_mse(y, output)
            #     for layer in reversed(self.layers[1:]):
            #         error = self.backward(error, lr, x, layer)
            # print('epoch %d/%d   error=%f' % (e + 1, epochs, err))

if __name__ == '__main__':
    x_train, y_true = NeuralSample.generate_lines()
    from sklearn.datasets import make_circles


    net = NeuralNetMinimal()
    net.add_layer(9, 0, "sig")
    net.add_layer(3, 1, "sig")
    net.add_layer(3, 2, "sig")
    net.add_layer(3, 3, "sig")
    net.add_layer(3, 3, "sig")
    net.train(x_train, y_true, 10, 0.0025)
    # plt.scatter(x, y_pred)
    # plt.show()

    # for i in range(100):
    #     print()