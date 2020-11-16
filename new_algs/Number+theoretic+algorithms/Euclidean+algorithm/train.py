import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import json
import os
import numpy as np
import random
from tensorboardX import SummaryWriter
import tqdm

from data_loader import *
from models import model_dict
from util import get_parser

parser = get_parser()
parser = parser.parse_args()

use_cuda = torch.cuda.is_available()
if use_cuda:
    if parser.manual_seed >= 0:
    	torch.cuda.manual_seed(parser.manual_seed)
device = torch.device("cuda" if use_cuda else "cpu")

def _generate_shuffled_incides(shuffled_indices, n_servers, n_dim):
    return idxs

shuffled_indices = list(range(parser.n_servers))

def train(epoch, model, training_set, optimizer, writer, verbose=True):
    total_optimal_cost = 0
    total_model_cost = 0
    total_model_loss = 0
    model.train()
    datasets = training_set.dataset.datasets
    # Add shuffling, one fixed shuffle per epoch
    global shuffled_indices
    # i, j = random.randrange(0, parser.n_servers), random.randrange(0, parser.n_servers)
    # shuffled_indices[i], shuffled_indices[j] = shuffled_indices[j], shuffled_indices[i]
    # random.shuffle(shuffled_indices)
    # shuffled_x_indices = shuffled_indices + [parser.n_servers]
    global permutations
    num_batches =  len(training_set)
    permutations = [[i for i in range(parser.n_servers)] for i in range(num_batches)]
    
    shuffle, no_shuffle = 0, 0
    for i, (X_batch, y_batch) in enumerate(tqdm.tqdm(training_set)):
        # first, get the list of servers
        servers = datasets[i].servers
        total_optimal_cost += datasets[i].cost
        model_cost = 0
        locations = servers.clone().to(device)
        total_loss = 0
        optimizer.zero_grad()
        if batch_style == 'predicted':
            for X, y in zip(X_batch, y_batch):
                X, y = X.to(device), y.to(device)
                # go through each example, get the starting points, etc.
                X_all = torch.cat((locations, X.reshape(-1, parser.dims)))
                # log_probs is the log probability of the elements
                log_probs = model(X_all)
                model_loss = F.nll_loss(log_probs, y)
                total_loss += model_loss
                # Gives the index of the server to move
                # TODO: See if we should change it to a probabilistic model
                model_pred = log_probs.argmax()
                model_cost += distance_function(locations[model_pred], X.reshape(-1, parser.dims)).item()
                # locations[model_pred] = X.reshape(-1, parser.dims)
                locations[y] = X.reshape(-1, parser.dims)
        else:
            if random.randrange(0, 10) <= 0:
                # Add random shuffling.
                shuffle += 1
                random.shuffle(permutations[i])
            else:
                no_shuffle += 1
            
            shuffled_x_indices = permutations[i] + [parser.n_servers]
            X_batch_shuffled = X_batch[:, shuffled_x_indices, :]
            y_batch_shuffled = torch.Tensor([permutations[i][j] for j in y_batch.type(torch.LongTensor).squeeze_()])
            y_batch_shuffled = y_batch_shuffled.reshape(y_batch.shape).type(torch.LongTensor)

            X_batch_shuffled, y_batch_shuffled = X_batch_shuffled.to(device), y_batch_shuffled.to(device)
            # log_probs is the log probability of the elements
            log_probs = model(X_batch_shuffled)
            model_loss = F.nll_loss(log_probs, y_batch_shuffled.squeeze_())
            total_loss += model_loss
        total_model_loss += (model_loss.item())
        total_model_cost += model_cost
        model_loss.backward()
        optimizer.step()
    if verbose:
        print('Epoch {}: \t\tLoss: {}, rand ratio {}'.format(
            epoch, total_model_loss/len(training_set), shuffle / (shuffle + no_shuffle)))
    
    writer.add_scalar('train_loss', total_loss, epoch)

def test(epoch, model, test_set, writer, verbose=True):
    total_optimal_cost = 0
    total_model_cost = 0
    total_model_loss = 0
    total_move_closest_cost = 0
    model.eval()
    datasets = test_set.dataset.datasets
    for i, (X_batch, y_batch) in enumerate(tqdm.tqdm(test_set)):
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        # first, get the list of servers
        servers = datasets[i].servers
        total_optimal_cost += datasets[i].cost
        total_move_closest_cost += datasets[i].move_closest_cost
        model_cost = 0
        locations = servers.clone().to(device)
        total_loss = 0
        for X, y in zip(X_batch, y_batch):
            X, y = X.to(device), y.to(device)
            # go through each example, get the starting points, etc.
            X_all = torch.cat((locations, X.reshape(-1, parser.dims)))
            # log_probs is the log probability of the elements
            log_probs = model(X_all)
            model_loss = F.nll_loss(log_probs, y)
            total_loss += model_loss
            # Gives the index of the server to move
            model_pred = log_probs.argmax()
            model_cost += distance_function(locations[model_pred], X.reshape(-1, parser.dims)).item()
            # Here, we go sequentially and solve the problem with our neural net
            locations[model_pred] = X.reshape(-1, parser.dims)
        total_model_cost += model_cost
        total_model_loss += (model_loss.item())
    if verbose:
        print('Testing:')
        print('Epoch {}: \t\tModel cost/Optimal Cost: {}/{}\n\t\t\tRatio: {} MC Ratio: {} Loss: {}'.format(
            epoch, total_model_cost, total_optimal_cost, 
            total_model_cost/total_optimal_cost, total_move_closest_cost/total_optimal_cost, 
            total_model_loss/len(test_set)))
    writer.add_scalar('test_ratio', total_model_cost/total_optimal_cost, epoch)
    writer.add_scalar('move_closest_ratio', total_move_closest_cost/total_optimal_cost, epoch)
    writer.add_scalar('model_cost', total_model_cost, epoch)
    writer.add_scalar('optimal_cost', total_optimal_cost, epoch)
    
    global best_ratio
    if best_ratio > total_model_cost/total_optimal_cost:
        best_ratio = total_model_cost/total_optimal_cost
        save_model(epoch, {
                'epoch': epoch + 1,
                'state_dict': model.state_dict(),
                'optimizer' : optimizer.state_dict(),
            })

# Summary writer and model directory
model_dir = parser.model_dir
# Initialize tensorboard writer
writer = SummaryWriter(model_dir)

def save_model(epoch, model_dict):
    filename = os.path.join(model_dir, 'checkpoint_{}'.format(epoch))
    torch.save(model_dict, filename)

# Training/test set details
num_servers = parser.n_servers
num_requests = parser.n_requests_batch
training_set_size = parser.n_requests_train
batch_size = parser.batch_size
test_set_size = parser.n_requests_test
dims = parser.dims
metric = parser.dist_metric
batch_style = parser.batch_style

def distance_function(x, y, metric=metric):
    return torch.norm(x-y, p=metric)

# Model params
architecture = parser.model
hidden_layers = parser.hidden_layers
hidden_units = parser.hidden_units

# Training params
learning_rate = parser.learning_rate
epochs = parser.epochs
optimizer = optim.SGD if parser.optim == 'sgd' else optim.Adam

# Create model
model = model_dict.get(architecture)
if model == None:
    model = model_dict['fc']

model = model(dims, num_servers, hidden_units, hidden_layers)
model = model.to(device)
optimizer = optimizer(model.parameters(), lr=learning_rate, weight_decay=0.0002)

if parser.verbose:
    print ("Set up model")

# Load dataset
# TODO (Mahi): Get a better way of inputting the distributions
server_distribution = distribution_from_centers([np.array([0., 0.])], [np.array([2.])])
request_distribution = distribution_from_centers(np.array([[ 1, 1],
                                                            [-1, 1],
                                                            [-1,-1],
                                                            [ 1,-1],
                                                            [ 1, 0],
                                                            [ 0, 1],
                                                            [-1, 0],
                                                            [ 0,-1],
                                                            [ 0, 0]], dtype='f'), np.array([0.5] * 9))

training_batch_size = 50 * batch_size
test_batch_size = batch_size

training_set, test_set = kserver_test_and_train(training_set_size, test_set_size, 
                                                num_servers, num_requests, 
                                                training_batch_size, test_batch_size,
                                                # TODO: Change this back
                                                request_distribution, request_distribution, 
                                                dimensions=dims, distance_metric=metric, 
                                                device=device, style=batch_style)

if parser.verbose:
    print ("Set up training data")

if __name__ == '__main__':
    for e in range(epochs):
        train(e, model, training_set, optimizer, writer)
        test(e, model, test_set, writer)