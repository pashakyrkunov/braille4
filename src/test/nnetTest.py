import numpy as np
from classify import nnet as nn


def predict_test1():
    layers = [np.array([[30, -20, -20]])]  # 1 layer, 1 neuron (NAND switch)
    for x, y in zip((0, 0, 1, 1), (0, 1, 0, 1)):
        hypothesis = nn.predict(layers, np.array([x, y]))[0]
        assert abs(hypothesis - float(not (x and y))) < 1e-3


def predict_test2():
    layer1 = np.array([[30, -20, -20], [-30, 20, 20]])
    layers = [layer1]  # 1 layer, 2 neurons (NAND, AND)
    for x, y in zip((0, 0, 1, 1), (0, 1, 0, 1)):
        hypothesis = nn.predict(layers, np.array([x, y]))
        assert(abs(hypothesis[0] - float(not(x and y)))) < 1e-3
        assert(abs(hypothesis[1] - float(x and y))) < 1e-3


def init_xor_switch():
    """
    XOR logic switch based on neural network
    x XOR y = (x NAND y) AND (x OR y) -> need two layers
    """
    layer1 = np.array([[-10, 20, 20], [30, -20, -20]])  # OR, NAND
    layer2 = np.array([[-30, 20, 20]])  # AND
    layers = [layer1, layer2]
    x_mtx = np.array(((0, 0), (0, 1), (1, 0), (1, 1)))
    return layers, x_mtx


def predict_test3():
    layers, x_mtx = init_xor_switch()
    hypothesis_mtx = nn.predict_many(layers, x_mtx)
    for ivec in range(len(x_mtx)):
        x_vec = x_mtx[ivec]
        x = x_vec[0]
        y = x_vec[1]
        assert abs(nn.predict(layers, x_vec) - float(x != y)) < 1e-3
        assert abs(nn.predict(layers, x_vec) - hypothesis_mtx[ivec]) < 1e-5


def cost_test():
    layers, x_mtx = init_xor_switch()
    y_right = np.array([[0, 1, 1, 0]]).T
    cost_right = nn.cost_crossentropy(x_mtx, y_right, layers)
    assert 0 <= cost_right <= 10e-3
    y_wrong = np.array([[0, 1, 0, 0]]).T
    cost_wrong = nn.cost_crossentropy(x_mtx, y_wrong, layers)
    assert 0.5 <= cost_wrong


def grad_test1():
    layers = [np.array([[-30, 20, 20]])]  # 1 layer, 1 neuron (AND switch)
    x_mtx = np.array(((0, 0), (0, 1), (1, 0), (1, 1)))
    y_mtx = np.array([[0], [0], [0], [1]])
    grad = nn.gradients(x_mtx, y_mtx, layers)  # compute gradients in optimal point
    assert len(grad) == 1
    grad = grad[0]  # only one 2-dimensional matrix, so we may reduce dimensions
    assert grad.shape == layers[0].shape
    assert np.max(np.abs(grad)) < 1e-4
    y_mtx[0][0] = 1
    grad = nn.gradients(x_mtx, y_mtx, layers)[0]  # not optimal point
    assert np.max(np.abs(grad)) > 0.2


def grad_test2():
    layers, x_mtx = init_xor_switch()
    y_right = np.array([[0, 1, 1, 0]]).T
    grad_right = nn.gradients(x_mtx, y_right, layers)
    assert len(grad_right) == 2  # one grad matrix for one layer
    assert grad_right[0].shape == layers[0].shape  # one grad matrix for one layer
    assert grad_right[1].shape == layers[1].shape  # one grad matrix for one layer
    assert np.max(np.abs(grad_right[0])) < 1e-3
    assert np.max(np.abs(grad_right[1])) < 1e-3


if __name__ == '__main__':
    predict_test1()
    predict_test2()
    predict_test3()
    cost_test()
    grad_test1()
    grad_test2()
