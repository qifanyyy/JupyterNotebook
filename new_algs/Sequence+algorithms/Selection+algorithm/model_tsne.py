import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

X = np.loadtxt('model.csv')
tsne = TSNE(perplexity=50)
X = tsne.fit_transform(X)
np.savetxt('tsne.csv', X)

vec = np.zeros((148, 148))
for i in range(148):
    vec[i, i] = i
tsne = TSNE(perplexity=50)
X = tsne.fit_transform(vec)
np.savetxt('tsne_uniform.csv', X)
