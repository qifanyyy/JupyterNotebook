import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.linear_model import LogisticRegression
import json
import time
import datetime
import torch as th
from torch.nn import functional as F

import random


def parse_labels(tool1, tool2, labels, major=None):
    o = []

    pos = 0
    neg = 0

    for L in labels:
        l1 = 100
        l2 = 100

        for i, label in enumerate(L):
            if label == tool1:
                l1 = i
            elif label == tool2:
                l2 = i
            elif isinstance(label, list):
                if tool1 in label:
                    l1 = i
                if tool2 in label:
                    l2 = i

        assert(l1 < 100 and l2 < 100)

        if l1 < l2:
            pos += 1
            o.append(1)
        elif l2 < l1:
            neg += 1
            o.append(0)
        else:
            o.append(-1)

    o = np.array(o)
    if major is None:
        major = pos > neg

    o[np.where(o == -1)] = 1 if major else 0

    return o, major


def load_binary_data(tool1, tool2):
    start = time.time()

    train = np.genfromtxt("train.csv", delimiter="\t")
    test = np.genfromtxt("test.csv", delimiter="\t")

    with open("train_labels.json", "r") as inp:
        train_labels, major = parse_labels(
            tool1, tool2, json.load(inp)
        )

    with open("test_labels.json", "r") as inp:
        test_labels, _ = parse_labels(
            tool1, tool2, json.load(inp), major
        )

    scaler = MinMaxScaler()
    train = scaler.fit_transform(train)
    test = scaler.transform(test)

    acc = (test_labels == (1 if major else 0)).sum() / float(test_labels.shape[0])

    print("Load dataset for %s and %s in %f seconds (Default accuracy: %f)"\
          % (tool1, tool2, (time.time() - start), acc))

    # Sanity check
    clf = LogisticRegression()
    clf.fit(train, train_labels)

    train_score = clf.score(train, train_labels)
    test_score = clf.score(test, test_labels)

    test_1 = test_labels.mean()
    test_0 = (1 - test_labels).mean()
    bias = max(test_0, test_1)
    print("Test bias: %f" % bias)

    print("Logistic Regression Sanity check: Train %f Test %f" % (train_score, test_score))

    return train, train_labels, test, test_labels


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class Rank_BCE(th.nn.Module):

    def __init__(self):
        super().__init__()

    def forward(self, x, y):

        filt = th.abs(2 * y - 1)
        x = filt * x
        y = filt * y

        return F.binary_cross_entropy_with_logits(x, y)


class MLP(th.nn.Module):

    def __init__(self, sizes):
        super().__init__()

        for i in range(len(sizes) - 1):
            in_ch = sizes[i]
            out_ch = sizes[i + 1]
            self.add_module("lin_%d" % i, th.nn.Linear(in_ch, out_ch))

    def forward(self, x):
        train = self.training

        out = x
        for i, child in enumerate(self.children()):
            if i > 0:
                out = F.dropout(out, training=train)
            out = child(out)

        return out


def precision(pred, target):
    tp = (pred == 1 and target == 1).sum().item()
    fp = (pred == 1 and target == 0).sum().item()
    return tp / (tp + fp)


def recall(pred, target):
    tp = (pred == 1 and target == 1).sum().item()
    fn = (pred == 0 and target == 1).sum().item()

    return tp / (tp + fn)


def f1_score(pred, target):
    p = precision(pred, target)
    r = recall(pred, target)
    f = 2*(p * r)/(p + r)
    return f, p, r


if __name__ == '__main__':

    learning_rate = 0.001
    batch_size = 32
    epoch = 10000
    C = 0.00001

    X, y, Xt, yt = load_binary_data("Klee", "ESBMC-incr")

    X = th.tensor(X, dtype=th.float)
    y = th.tensor(y, dtype=th.float)
    Xt = th.tensor(Xt, dtype=th.float)
    yt = th.tensor(yt, dtype=th.float)

    model = MLP([X.shape[1], 1])

    device = th.device('cpu')
    model = model.to(device)
    bce = Rank_BCE().to(device)
    optimizer = th.optim.Adam(model.parameters(), lr=0.1, weight_decay=C)

    index = list(range(X.shape[0]))

    for ep in range(epoch):
        model.train()
        random.shuffle(index)
        for i, batch in enumerate(chunks(index, batch_size)):
            Xb = X[batch, :].to(device)
            yb = y[batch].to(device)
            yb = th.reshape(yb, [yb.shape[0], 1])
            optimizer.zero_grad()
            out = model(Xb)
            loss = bce(out, yb)
            loss.backward()
            # print("It %d Loss %f" % (i, loss.item()))
            optimizer.step()
        if ep % 10 == 0:
            model.eval()
            testo = model(Xt)
            testo = th.sigmoid(testo)
            testo = th.round(testo)
            ya = th.reshape(yt, testo.shape)
            test_acc = (testo == ya).float().mean().item()
            traino = th.round(th.sigmoid(model(X)))
            ya = th.reshape(y, traino.shape)
            train_acc = (traino == ya).float().mean().item()
            print("Epoch %d Train Accuracy %f Test Accuracy %f" % (ep, train_acc, test_acc))
