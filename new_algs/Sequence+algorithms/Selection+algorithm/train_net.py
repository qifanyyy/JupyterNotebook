import torch
import numpy as np


def train_model(model, loss_fn, optimiser, num_epoch, X, Y):
    losses = []  # store losses for visualisation

    # train neural network
    for epoch in range(num_epoch):
        # perform forward pass: compute predicted y by passing x to the model
        output = model(X).squeeze()

        # compute loss
        loss = loss_fn(output, Y)
        losses.append(loss.data)

        # print training progress
        ##        if epoch % 50 == 0:
        ##            predicted = torch.squeeze(torch.round(output), 1)
        ##            # calculate and print accuracy
        ##            total = predicted.size(0)
        ##            correct =  predicted.data.numpy() == Y.data.numpy()
        ##            print('Epoch [%d/%d] Loss: %.4f  Accuracy: %.2f %%'
        ##                % (epoch + 1, num_epoch, loss.data[0], 100 * sum(correct)/total))

        # clear the gradients before running the backward pass.
        optimiser.zero_grad()

        # perform backward pass
        loss.backward()

        # apply gradients
        optimiser.step()

    return model, loss


def abs_mse_loss(input, target, size_average=True, reduce=True):
    """
    Adapted per: http://pytorch.org/docs/master/_modules/torch/nn/functional.html
    mse_loss(input, target, size_average=True, reduce=True) -> Ten sor
    Measures the element-wise mean squared error.
    See :class:`~torch.nn.MSELoss` for details.
    """
    return _pointwise_loss(lambda a, b: abs(a - b), torch._C._nn.mse_loss,
                           input, target, size_average, reduce)


def _pointwise_loss(lambd, lambd_optimized, input, target, size_average=True, reduce=True):
    """
    Per: http://pytorch.org/docs/master/_modules/torch/nn/functional.html
    """
    if target.requires_grad:
        d = lambd(input, target)
        if not reduce:
            return d
        return torch.mean(d) if size_average else torch.sum(d)
    else:
        return lambd_optimized(input, target, size_average, reduce)


def get_min_phat(model, X, Y, optimiser):
    '''
    Takes a model. Compute p-hat for each unit.
    The input with the lowest p-hat value.
    '''
    # the derivative finding p-hat for each input node is calculated using error propagation
    # where the loss function is linear
    output = model(X).squeeze()
    loss = abs_mse_loss(output, Y)
    optimiser.zero_grad()
    loss.backward()
    optimiser.step()

    # calculate p_hat for each input node
    p_hat = torch.mul(X.grad[X.size()[0] - 1], -1)
    # p_hat = X.grad[X.size()[0]-1]
    p_hat_np = p_hat.data.numpy()

    if np.any(p_hat_np):
        # index of input to remove from df.
        min_index = np.where(p_hat_np == np.min(p_hat_np[np.nonzero(p_hat_np)]))
        return min_index[0]
    else:
        return None


def remove_input(df, irrelevant_input):
    inp_idx = irrelevant_input + 1  # add one to account for output column at 0
    return df.drop(df.columns[inp_idx], axis=1)
