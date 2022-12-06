import numpy as np
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler


def generate_test():
    X = np.random.uniform(low=-5, high=5, size=(100,1))
    # Y = X + 1
    Y = np.sin(X)
    return X, Y

def generate_digits():
    digits = load_digits()
    x = digits.images[0:10]
    # x = StandardScaler().fit_transform(digits.data)
    y = []
    for i in range(10):
        t_a = [0.0] * 10
        t_a[i] = 1.0
        y.append(t_a)
    return x, y

def generate_lines():
    x = [
        [1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 1],
        ]
    y = [
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ]
    return x, y