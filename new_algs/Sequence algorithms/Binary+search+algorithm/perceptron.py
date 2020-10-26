import numpy as np
np.random.seed(1)

def stepFunction(t):
    if t >= 0:
        return 1
    return 0

def prediction(X, W, b):
    return stepFunction((np.matmul(X,W)+b)[0])


# define the perceptron trick function:
def perceptronStep(X, y, W, b, learn_rate = 0.01):
    """ The function should receive as inputs the data X, the labels y,
        the weights W (as an array), and the bias b,
        update the weights and bias W, b, according to the perceptron algorithm,
        and return W and b."""
    for i in range(len(X)):
        y_hat = prediction(X[i], W[i], b)

        #预测为正，标签为负，则减去
        if y_hat - y == 1:
            W[0] -= X[i][0] * learn_rate
            W[1] -= X[i][1] * learn_rate
            b -= learn_rate
        #预测为负，标签为正，则加上
        elif y_hat - y = -1:
            W[0] += X[i][0] * learn_rate
            W[1] += X[i][1] * learn_rate
            b += learn_rate
    return W, b


def trainPerceptronAlgorithm(X, y, learn_rate = 0.01, num_epochs = 25):
    """ This function runs the perceptron algorithm repeatedly on the dataset,
        and returns a few of the boundary lines obtained in the iterations,
        for plotting purposes."""

    x_min, x_max = min(X.T[0]), max(X.T[0])
    y_min, y_max = min(X.T[1]), max(X.T[1])
    W = np.array(np.random.rand(2,1))
    b = np.random.rand(1)[0] + x_max
    # These are the solution lines that get plotted below.
    boundary_lines = []
    for i in range(num_epochs):
        # In each epoch, we apply the perceptron step.
        W, b = perceptronStep(X, y, W, b, learn_rate )
        boundary_lines.append((-W[0]/W[1], -b/W[1]))
    return boundary_lines
