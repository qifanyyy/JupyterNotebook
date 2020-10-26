import numpy as np
import torch
from torch.utils.data import Dataset, ConcatDataset, DataLoader
import tqdm

# # For creating multiple CUDA tensors in a dataloader
# import torch
# torch.multiprocessing.set_start_method("spawn")

from optimal_offline import KServer


class AbstractDistribution(object):
    """
    Abstract class for all distrubitons.
    """
    def __init__(self):
        raise NotImplementedError

    def sample(self, n):
        raise NotImplementedError


class NumpyDistribution(AbstractDistribution):
    """
    Reference wrapper around numpy distributions.
    """
    def __init__(self, distribution_name='normal', shift= np.array([0]), args=(1.,), seed=0):
        self.distribution = getattr(np.random, distribution_name)
        self.args = args
        self.shift = shift
        np.random.seed(seed)

    def sample(self, n):
        sz = (n,) + np.array(self.shift).shape
        return self.shift + self.distribution(*self.args, size=sz)


class MixedDistribution(AbstractDistribution):
    """
    Reference implementation of mixture models. Takes a list of distributions and 
    their associated, and then allows you to sample from the mixed models.
    """
    def __init__(self, distributions, weights, seed=0):
        assert len(distributions) == len(weights)
        self.distributions = distributions
        self.weights = np.array(weights, dtype='f')
        self.weights /= self.weights.sum()
        np.random.seed(seed)

    def sample(self, n):
        components = np.random.choice(len(self.distributions), n, p = self.weights)
        samples = np.array([self.distributions[i].sample(1) for i in components]).reshape(n, -1)
        return samples

        # num_samples = np.rint([n * p for p in self.weights]).astype(int)
        # samples = [self.distributions[i].sample(num_sample) for i, num_sample in enumerate(num_samples)]
        # if np.sum(num_samples) < n:
        #     choices = np.random.choice(len(self.distributions), (n - np.sum(num_samples)), p=self.weights)
        #     for c in choices:
        #         samples.append(self.distributions[c].sample(1))
        # samples = np.concatenate(samples)
        # np.random.shuffle(samples)
        # return samples

class KServerDataset(Dataset):
    """
    A generator for k-server datasets.
    """
    def __init__(self, num_servers, 
                 num_requests, server_distribution, request_distribution, 
                 dimensions=2, distance_metric=2, seed=0, device='cpu', style='optimal', algorithm='optimal'):
        np.random.seed(seed)
        self.servers = server_distribution.sample(num_servers)
        self.requests = request_distribution.sample(num_requests)
        self.instance = KServer(servers = self.servers, requests= self.requests, order=distance_metric)
        self.cost = self.instance.optimal_cost()
        self.optimal_movement = self.instance.get_serves()

        if type(device) == str:
            device = torch.device(device)
        self.servers = torch.Tensor(self.servers)
        self.requests = torch.Tensor(self.requests)
        self.optimal_movement = torch.Tensor(self.optimal_movement).type(torch.LongTensor)
        self.optimal_movement.unsqueeze_(-1)
        self.move_closest_cost = 0

        all_inputs = []
        locations = self.servers.clone()
        move_closest_locations = self.servers.clone()
        move_closest_labels = []
        X_all_move_closest = []
        for X, y in zip(self.requests, self.optimal_movement):
            # go through each example, get the starting points, etc.
            X_all = torch.cat((locations, X.reshape(-1, dimensions)))
            all_inputs.append(X_all.clone())
            locations[y] = X.reshape(-1, dimensions)
            
            X_all_move_closest.append( torch.cat((move_closest_locations, X.reshape(-1, dimensions))) )
            dist_matrix = -torch.norm(move_closest_locations - X.reshape(-1, dimensions), 
                                     p=distance_metric, dim=1, keepdim=True)
            # put in the minimum distance
            move_closest_labels.append(dist_matrix.argmax().item())
            self.move_closest_cost -= dist_matrix.max().item()
            move_closest_locations[move_closest_labels[-1]] = X.reshape(-1, dimensions)
        self.move_closest_labels = torch.Tensor(move_closest_labels).type(torch.LongTensor).reshape(self.optimal_movement.shape)
        self.move_closest_batch = torch.stack(X_all_move_closest)

        # print(self.move_closest_labels.shape, self.move_closest_batch.shape)
        self.batch = torch.stack(all_inputs)
        assert style in ['predicted', 'optimal']
        self.style = style
        self.algorithm = algorithm

    def __len__(self):
        return len(self.optimal_movement)
    
    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def __getitem__(self, idx):
        if self.algorithm == 'move_closest':
            if self.style == 'predicted':
                return (self.requests[idx], self.move_closest_labels[idx])
            elif self.style == 'optimal':
                return (self.move_closest_batch[idx], self.move_closest_labels[idx])
        elif self.algorithm == 'optimal':
            if self.style == 'predicted':
                return (self.requests[idx], self.optimal_movement[idx])
            elif self.style == 'optimal':
                return (self.batch[idx], self.optimal_movement[idx])
        else:
            raise ValueError('Algorithm undefined')

class ConstantDistribution(AbstractDistribution):
    def __init__(self, points):
        self.points = points
    
    def sample(self, n):
        assert len(self.points) == n
        return self.points


def _kserver_training_set(len_data, num_servers, 
            num_requests, server_distribution, request_distribution, 
            dimensions=2, distance_metric=2, seed=0, device='cpu', style='optimal'):
    np.random.seed(seed)
    batch_size = num_requests
    single_datasets = []
    for i in tqdm.trange(len_data // num_requests):
        single_datasets.append(KServerDataset(num_servers, 
                                num_requests, server_distribution, 
                                request_distribution, dimensions, 
                                distance_metric, seed = np.random.randint(0, len_data), 
                                device=device, style=style))
        # set them to move closest
        # TODO: Make this better
        # single_datasets[-1].set_algorithm('move_closest')
    return ConcatDataset(single_datasets)


def _kserver_loader(len_data, num_servers, 
            num_requests, batch_size, server_distribution, request_distribution, 
            dimensions=2, distance_metric=2, seed=0, device='cpu', style='optimal'):
    dataset = _kserver_training_set(len_data, num_servers, 
                                   num_requests, server_distribution, 
                                   request_distribution, dimensions, 
                                   distance_metric, seed, device=device, style=style)
    return DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=2)


def kserver_test_and_train(len_train, len_test, num_servers, num_requests, training_batch_size, test_batch_size,
                           server_distribution, request_distribution, 
                           dimensions=2, distance_metric=2, seed=0, device='cpu', style='optimal'):
    train_loader = _kserver_loader(len_train, num_servers, num_requests, training_batch_size, server_distribution, 
                                   request_distribution, dimensions, distance_metric, seed, device=device, style=style)
    # Testing is always done with predicted stuff, so we used the predicted data loader mode
    assert num_requests == test_batch_size
    test_loader = _kserver_loader(len_test, num_servers, num_requests, num_requests, server_distribution, 
                                  request_distribution, dimensions, distance_metric, seed, device=device, style='predicted')
    return train_loader, test_loader


def distribution_from_centers(mus, sigmas, weights=None, seed=0):
    dist = []
    if weights is None:
        weights = [1.] * len(mus)
    for mu, sigma in zip(mus, sigmas):
        dist.append(NumpyDistribution(distribution_name='normal', shift = mu, args=(sigma,), seed=seed))
    return MixedDistribution(dist, weights)


"""
Testing the code.

d = distribution_from_centers(np.array([[1,1],
                                        [-1,1],
                                        [-1,-1],
                                        [1,-1],
                                        [1,0],
                                        [0,1],
                                        [-1,0],
                                        [0,-1],
                                        [0,0]
                                        ], dtype='f'), np.array([0.5] * 9))

print(d.sample(100))
"""