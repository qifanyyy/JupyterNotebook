import math
import torch
import torch.nn.functional as f

import train_net as trn

EPOCH = 10000
LEARNING_RATE = 0.05
MOMENTUM_RATE = 0.01


def construct_model(x, y):
    """
    Define and train a neural network

    The network will be trained with Stochastic Gradient Descent (SGD) as an
    optimiser, that will hold the current state and will update the parameters
    based on the computed gradients. The loss function we use is MSE.
    """

    # Construct model
    n_input = len(x[0])
    n_output = 1
    n1_hidden = round(math.sqrt(n_input * n_output) * 2)
    model = TwoLayerNet(n_input, n1_hidden, n_output)

    # define loss function
    loss_fn = torch.nn.MSELoss()
    # define optimiser
    optimiser = torch.optim.SGD(model.parameters(), lr=LEARNING_RATE, momentum=MOMENTUM_RATE)

    # train nn using functions defined above, returns a tuple (model, se_model)
    trained_model, model_se = trn.train_model(model, loss_fn, optimiser, EPOCH, x, y)

    return model, optimiser, trained_model, model_se


class TwoLayerNet(torch.nn.Module):
    """
    A fully-connected sigmoid network with two hidden layers, trained to predict y from x by minimizing sum squared errors.
    This implementation defines the model as a custom Module subclass.
    """
    def __init__(self, n_input, n_hidden, n_output):
        super(TwoLayerNet, self).__init__()
        # define linear hidden layer output
        self.hidden = torch.nn.Linear(n_input, n_hidden)
        # define linear output layer output
        self.out = torch.nn.Linear(n_hidden, n_output)

    def forward(self, x):
        """
        Takes variable of input data and returns variable of output data.
        """

        # get hidden layer input
        h_input = self.hidden(x)
        # define activation function for hidden layer
        h_output = f.sigmoid(h_input)
        # get output layer output
        y_pred = self.out(h_output)

        return f.sigmoid(y_pred)
