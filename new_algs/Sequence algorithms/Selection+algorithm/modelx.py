import torch as th
from torch_geometric.utils import softmax, scatter_
from torch_geometric.nn import MessagePassing
from torch.nn import functional as F


class Entry(th.nn.Module):

    def __init__(self, in_channels, out_channels):

        super().__init__()

        self.nn = th.nn.Sequential(
            th.nn.BatchNorm1d(in_channels),
            th.nn.Linear(in_channels, out_channels),
            th.nn.BatchNorm1d(out_channels),
            th.nn.ReLU()
        )

    def forward(self, x):
        return self.nn(x)


class ConGIN(MessagePassing):

    def __init__(self, in_channels, out_channels, edge_channels, hidden):
        super().__init__()

        self.nn = th.nn.Sequential(
            th.nn.BatchNorm1d(2*in_channels),
            th.nn.Linear(2*in_channels, hidden),
            th.nn.BatchNorm1d(hidden),
            th.nn.ReLU(),
            th.nn.Linear(hidden, out_channels),
            th.nn.BatchNorm1d(out_channels),
            th.nn.ReLU()
        )

    def forward(self, x, edge_index, edge_attr):
        x = x.unsqueeze(-1) if x.dim() == 1 else x

        edge_sum = self.propagate(edge_index, x=x)

        out = th.cat([x, edge_sum], dim=1)

        return self.nn(out)

    def message(self, x_j):
        return x_j


class DenseGIN(MessagePassing):

    def __init__(self, in_channels, out_channels, edge_channels, hidden):
        super().__init__()

        self.nn = th.nn.Sequential(
            th.nn.Linear(in_channels, hidden),
            th.nn.BatchNorm1d(hidden),
            th.nn.ReLU(),
            th.nn.Linear(hidden, out_channels),
            th.nn.BatchNorm1d(out_channels),
            th.nn.ReLU()
        )

        self.sum_norm = th.nn.BatchNorm1d(out_channels)

    def forward(self, x, edge_index, edge_attr):
        x = x.unsqueeze(-1) if x.dim() == 1 else x

        x_i = self.nn(x)

        edge_sum = self.propagate(edge_index, x=x_i)

        edge_sum = self.sum_norm(edge_sum)

        out = th.cat([x, edge_sum], dim=1)

        return out

    def message(self, x_j):
        return x_j


class DenseEGIN(MessagePassing):

    def __init__(self, in_channels, out_channels, edge_channels, hidden):
        super().__init__()

        self.in_nn = th.nn.Sequential(
            th.nn.Linear(in_channels, hidden),
            th.nn.BatchNorm1d(hidden),
            th.nn.ReLU()
        )

        self.nn = th.nn.Sequential(
            th.nn.Linear(2*hidden + edge_channels, out_channels),
            th.nn.BatchNorm1d(out_channels),
            th.nn.ReLU()
        )

        self.sum_norm = th.nn.BatchNorm1d(out_channels)

    def forward(self, x, edge_index, edge_attr):
        x = x.unsqueeze(-1) if x.dim() == 1 else x

        x_i = self.in_nn(x)

        edge_sum = self.propagate(edge_index, x=x_i,
                                  edge_attr=edge_attr)

        edge_sum = self.sum_norm(edge_sum)

        out = th.cat([x, edge_sum], dim=1)

        return out

    def message(self, x_i, x_j, edge_index_j, edge_attr):
        attr = edge_attr[edge_index_j]
        inter = th.cat([x_i, x_j, attr.float()], dim=1)
        return self.nn(inter)


class DenseEdgeLayer(MessagePassing):

    def __init__(self, in_channels, edge_channels, out_channels, m=4):
        super().__init__(aggr='add')
        growth = out_channels - in_channels
        in_size = in_channels + edge_channels

        self.nn = th.nn.Sequential(
            th.nn.BatchNorm1d(in_size),
            th.nn.ReLU(),
            th.nn.Linear(in_size, m*growth),
            th.nn.BatchNorm1d(m*growth),
            th.nn.ReLU(),
            th.nn.Linear(m*growth, growth),
            th.nn.BatchNorm1d(growth),
            th.nn.ReLU()
        )

    def forward(self, x, edge_index, edge_attr):
        x = x.unsqueeze(-1) if x.dim() == 1 else x

        edges = self.propagate(edge_index, x=x,
                               edge_attr=edge_attr)

        return th.cat([x, edges], dim=1)

    def message(self, x_j, edge_index_j, edge_attr):
        attr = edge_attr[edge_index_j]
        inter = th.cat([x_j, attr.float()], dim=1)
        return self.nn(inter)


class DenseNodeLayer(MessagePassing):

    def __init__(self, in_channels, out_channels, m=4):
        super().__init__(aggr='add')
        growth = out_channels - in_channels
        in_size = in_channels

        self.nn = th.nn.Sequential(
            th.nn.BatchNorm1d(in_size),
            th.nn.ReLU(),
            th.nn.Linear(in_size, m*growth),
            th.nn.BatchNorm1d(m*growth),
            th.nn.ReLU(),
            th.nn.Linear(m*growth, growth),
            th.nn.ReLU()
        )

    def forward(self, x, edge_index, edge_attr):
        x = x.unsqueeze(-1) if x.dim() == 1 else x

        x_in = self.nn(x)

        edges = self.propagate(edge_index, x=x_in)

        return th.cat([x, edges], dim=1)

    def message(self, x_j):
        return x_j


class DenseEdgeGIN(th.nn.Module):

    def __init__(self, in_channels, edge_channels, out_channels,
                 embed_size, growth, layers=2, edge=True, bm=4):
        super().__init__()
        mid = int((in_channels + embed_size)/2)
        self.in_gate = th.nn.Sequential(
            th.nn.BatchNorm1d(in_channels),
            th.nn.ReLU(),
            th.nn.Linear(in_channels, mid),
            th.nn.BatchNorm1d(mid),
            th.nn.ReLU(),
            th.nn.Linear(mid, embed_size)
        )

        size = embed_size

        layer = []

        for i in range(layers):
            layer.append(
                DenseEdgeLayer(
                    size, edge_channels, size + growth, m=bm
                ) if edge else
                DenseNodeLayer(
                    size, size + growth, m=bm
                )
            )
            size += growth

        self.dense = th.nn.ModuleList(layer)

        mid = int((size + out_channels)/2)

        self.out_gate = th.nn.Sequential(
            th.nn.BatchNorm1d(size),
            th.nn.ReLU(),
            th.nn.Linear(size, mid),
            th.nn.BatchNorm1d(mid),
            th.nn.ReLU(),
            th.nn.Linear(mid, out_channels),
            th.nn.BatchNorm1d(out_channels),
            th.nn.ReLU()
        )

    def forward(self, x, edge_index, edge_attr):
        x = x.unsqueeze(-1) if x.dim() == 1 else x

        x_in = self.in_gate(x)

        for module in self.dense:
            x_in = module(x_in, edge_index, edge_attr)

        return self.out_gate(x_in)
