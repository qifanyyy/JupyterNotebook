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
best_ratio = 100.

def train(epoch, num_batches, model, optimizer, writer, verbose=True):
    model.train()
    total_loss = 0.
    for i in tqdm.trange(num_batches):
        optimizer.zero_grad()

        train_batch = torch.tensor(request_distribution.sample(batch_size * (num_servers + 1)), device=device, dtype=torch.float)
        train_batch = train_batch.reshape(batch_size, (num_servers + 1), -1)

        q_value_old = model(train_batch)

        best_indices = q_value_old.argmax(dim=1)
        rand_indices = torch.randint_like(best_indices, low=0, high=num_servers)
        index_picking = torch.bernoulli( eps_greedy * torch.ones_like(best_indices).double() ).long()
        indices = (index_picking * rand_indices) + ((1. - index_picking) * best_indices)

        new_locations = train_batch.clone().detach()
        location_to_move_to = new_locations[:, -1, :]
        old_server_loc = new_locations[range(batch_size), indices, :]
        batch_distance = compute_distance(old_server_loc, location_to_move_to)
        new_locations[range(batch_size), indices, :] = location_to_move_to

        new_req = torch.tensor(request_distribution.sample(avg_over), device=device, dtype=torch.float)
        locations_to_avg_over = new_locations[ [i for i in range(batch_size) for j in range(avg_over)], :, :]
        new_req_multiplied = new_req[[i for i in range(batch_size) for j in range(avg_over)], :]
        locations_to_avg_over[:, -1, :] = new_req_multiplied

        with torch.no_grad():
            q_values_to_avg = model(locations_to_avg_over)
            max_q_value_to_avg = q_values_to_avg.max(dim=1)[0]
            max_q_values = max_q_value_to_avg.reshape(batch_size, avg_over).mean(dim=1)

        update_values = alpha * ( -batch_distance + gamma * max_q_values)
        q_value_new = q_value_old.clone().detach()
        q_value_new[range(batch_size), indices] = (1 - alpha) * q_value_new[range(batch_size), indices] + update_values

        loss = ((q_value_old - q_value_new) ** 2).sum()
        total_loss += loss.item()
        loss.backward()
        optimizer.step()
    print(f'Loss: {total_loss}')
    writer.add_scalar('train_loss', total_loss, epoch)


def test(epoch, model, test_set, writer, verbose=True):
    total_optimal_cost = 0
    total_model_cost = 0
    total_model_loss = 0
    total_move_closest_cost = 0
    model.eval()
    datasets = test_set.dataset.datasets
    assert len(datasets) == len(test_set), "Test batches bigger than single datasets"
    for i, (X_batch, y_batch) in enumerate(tqdm.tqdm(test_set)):
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        # first, get the list of servers
        servers = datasets[i].servers
        total_optimal_cost += datasets[i].cost
        total_move_closest_cost += datasets[i].move_closest_cost
        model_cost = 0
        locations = servers.clone().detach().to(device)
        total_loss = 0
        for X, y in zip(X_batch, y_batch):
            X, y = X.to(device), y.to(device)
            # go through each example, get the starting points, etc.
            X_all = torch.cat((locations, X.reshape(-1, parser.dims)))
            # log_probs is the log probability of the elements
            logits = model(X_all)
            log_probs = F.log_softmax(logits, dim=1)
            model_loss = F.nll_loss(log_probs, y)
            total_loss += model_loss
            # Gives the index of the server to move
            model_pred = log_probs.argmax()
            # model_pred = torch.randint_like(log_probs.argmax(), 0, num_servers)
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

# RL parameters
alpha = parser.alpha
gamma = parser.gamma
eps_greedy = parser.eps_greedy
avg_over = parser.avg_over

def distance_function(x, y, metric=metric):
    return torch.norm(x-y, p=metric)

def compute_distance(x, y, metric=metric):
    return torch.norm(x-y, p=metric, dim=-1)

# Model params
architecture = parser.model
hidden_layers = parser.hidden_layers
hidden_units = parser.hidden_units

# Training params
learning_rate = parser.learning_rate
epochs = parser.epochs
optimizer = optim.SGD if parser.optim == 'sgd' else optim.Adam

# Create model
# model = model_dict.get(architecture)
# if model == None:
model = model_dict['fcq']

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
                                                            [ 0, 0]], dtype='f'), np.array(([0.5] * 8 + [5])))


training_batch_size = batch_size // 10
test_batch_size = num_requests
num_batches = 1000

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
        train(e, num_batches, model, optimizer, writer)
        test(e, model, test_set, writer)