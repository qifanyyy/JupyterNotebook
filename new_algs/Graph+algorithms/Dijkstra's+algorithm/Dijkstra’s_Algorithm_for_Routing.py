import numpy as np
from numpy import Infinity, sqrt, argmin
from numpy.random import randint
from matplotlib.pyplot import figure, plot, text


# Dijkstra's Finding nearest node algorithm
def dijkstra_routing(N, hop):
    w = [Infinity] * N
    w[0] = 0
    path = [-1] * N
    path[0] = 0

    source = [0]
    dest = [N for N in range(1, N)]
    loop = 0
    while True:
        for i in range(len(dest)):
            j = dest[i]
            dists = []
            for k in range(len(source)):
                l = source[k]
                dist = sqrt((x[j] - x[l]) ** 2 + (y[j] - y[l]) ** 2)  # Euclidian distance
                if dist > hop:
                    dist = Infinity
                dists.append(dist + w[l])
                # print(d)

            w[j], ind1 = np.min(dists), argmin(dists)
            # print(w, ind1)
            if w[j] != Infinity:
                path[j] = source[ind1]

        wdest = [w[i] for i in dest]
        dmin, ind2 = np.min(wdest), argmin(wdest)
        q = dest[ind2]
        plot(x[q], y[q], 'ro', ms=16)
        source.append(q)
        dest = np.delete(dest, ind2)

        print('--------------------- Iteration', loop, '---------------------')
        loop += 1
        if loop >= N - 1:
            break

    trace = [N - 1]
    i = -1
    while True:
        preN = path[i]
        i = preN
        if preN != 0:
            trace.append(preN)
        else:
            trace.append(0)
            break

    print(len(trace))
    for i in range(len(trace) - 1):
        p = trace[i]
        q = trace[i + 1]
        plot([x[p], x[q]], [y[p], y[q]], 'b')


if __name__ == '__main__':
    # Data Preparing & Plotting
    N = 100
    x1 = randint(10, 90, size=N)
    y1 = randint(10, 90, size=N)
    ind = [i for i, v in enumerate(x1) if v < 40 or v > 60]
    # let x, y br lists with elements whose values are under 40 or over 60
    x, y = x1[ind], y1[ind]
    N = len(x)

    # set first and last elements of x and y as 0 and 100
    x[0], x[-1] = 0, 100
    y[0], y[-1] = 0, 100

    fig = figure(1, figsize=(20, 20))
    plot(x, y, 'ko', ms=10)
    plot(x[0], y[0], 'bs', ms=15)
    plot(x[-1], y[-1], 'bs', ms=15)

    # This is to show the source node and last node of the program
    for i in range(N):
        if i == 0:
            text(x[i], y[i] + 2, 'S', fontsize=16)
        elif i == N - 1:
            text(x[i], y[i] + 2, 'D', fontsize=16)
        else:
            text(x[i], y[i] + 2, str(i), fontsize=16)

    hop = 80
    dijkstra_routing(N, hop)
    fig.savefig('hop = {}'.format(hop), dpi=300)