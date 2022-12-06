import numpy as np

def activation_binaryStep(x):
    return np.heaviside(x, 1)

def activation_linear(x):
    return x

def activation_sigmoid(x):
    return 1/(1+np.exp(-x))

def activation_tanh(x):
    return np.tanh(x)

def activation_RELU(x):
    x1=[]
    for i in x:
        if i<0:
            x1.append(0)
        else:
            x1.append(i)
    return x1

def activation_softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def loss_MSE(y_pred, y_true):
    return np.mean(np.power(y_true-y_pred, 2))

def deriv_tanh(x):
    return 1-np.tanh(x)**2

def forward_propagation(x, w, b):
    return np.dot(x, w) + b

def backward_propagation(loss, lr, x, w):
    return np.dot(loss, w.T), -lr * np.dot(x.T, loss), -lr * loss