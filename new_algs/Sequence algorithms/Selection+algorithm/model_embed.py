from tasks.torch_test import TestModel
import torch as th
import numpy as np


model = TestModel(148, 91, size=32)
model.load_state_dict(th.load('/Users/cedricrichter/Documents/Arbeit/Ranking/NeuralAlgorithmSelection/resources/simple_linear.th'))
model.eval()


vec = th.zeros((148, 148), dtype=th.float)
for i in range(148):
    vec[i, i] = i
vec = model.embed(vec)
vec = vec.detach().numpy()
np.savetxt('model.csv', vec)
