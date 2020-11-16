import numpy as np
from scipy.stats import gamma
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# ------------------------------------------ Problem 1 ------------------------------------------
'''
Calculate the mean of a Gamma(4.3, 6.2) random variable using:
a) Accept-reject with Gamma(4, 7) candidate
b) Metropolis-Hastings with Gamma(4, 7) candidate
c) Metropolis-Hastings with Gamma(5, 6) candidate
In each case monitor the convergence.
'''
f_sh = 4.3
f_sc = 6.2
np.random.seed(42)

# a) Accept-reject with Gamma(4, 7) candidate
g_sh = 4
g_sc = 7
x = np.linspace(start=0, stop=100, num=100)

# plot f and g before scaling g
def plot_f_g(f_name, M=1):
    fig = plt.figure()
    plt.plot(x, gamma.pdf(x, a=f_sh, scale=f_sc)) # f
    plt.plot(x, M * gamma.pdf(x, a=g_sh, scale=g_sc), linestyle=':') # g
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('gamma.pdf(x, shape, scale)')
    if M is not 1:
        l, l2 = 'after', 'M*'
    else:
        l, l2 = 'before', ''
    plt.title('PDFs of f(x) and g(x) {} scaling'.format(l))
    plt.legend(['f(x) = gamma.pdf(x, 4.3, 6.2)', '{}g(x) = {}gamma.pdf(x, 4, 7)'.format(l2, l2)])
    fig.savefig(f_name, dpi=300)
    plt.show()
# plot_f_g('f_g_before_scaling.png')

# plot f and g after scaling g
def find_max():
    f = lambda x: gamma.pdf(x, a=f_sh, scale=f_sc) / gamma.pdf(x, a=g_sh, scale=g_sc)
    res = minimize(lambda x: -f(x), 20)
    print('Max {} achieved at {}'.format(-res.fun, res.x))
    return -res.fun
M = find_max()
# plot_f_g('f_g_after_scaling.png', M)

# accept-reject algorithm
def accept_reject(g_sh, g_sc, n_sim=10000):
    X = np.array([])
    while len(X) < n_sim:
        size = int(M * n_sim)
        Y = np.random.gamma(shape=g_sh, scale=g_sc, size=size)
        f_gamma = gamma.pdf(Y, a=f_sh, scale=f_sc)
        g_gamma = gamma.pdf(Y, a=g_sh, scale=g_sc)
        idcs = M*np.random.uniform(size=size) < f_gamma/g_gamma
        X = np.append(X, Y[idcs])
    return X

X = accept_reject(g_sh, g_sc)
print('X:', len(X), X[-5:])



# b) Metropolis-Hastings with Gamma(4, 7) candidate
'''
def metropolis_hastings_old(g_sh, g_sc, n_sim=10000):
    X = [1]
    for i in range(n_sim):
        Y_prop_val = np.random.gamma(shape=g_sh, scale=g_sc)
        tgt_val = np.random.gamma(shape=f_sh, scale=f_sc)

        prop_dist = gamma.pdf(Y_prop_val, a=g_sh, scale=g_sc)
        tgt_dist = gamma.pdf(tgt_val, a=f_sh, scale=f_sc)

        accept_p = min(1, prop_dist/tgt_dist * tgt_val/Y_prop_val)
        move = Y_prop_val if np.random.random() < accept_p else X[-1]
        X.append(move)
    return X
'''

def metropolis_hastings(g_sh, g_sc, n_sim=10000):
    X = []
    x = 1
    for i in range(n_sim):
        Y_prop_val = np.random.gamma(shape=g_sh, scale=g_sc)

        q_x = gamma.pdf(x, a=g_sh, scale=g_sc) # tgt_val num. needed to be dist using x, use g
        q_y = gamma.pdf(Y_prop_val, a=g_sh, scale=g_sc) # den. needed to be dist using Y_prop_val

        prop_dist = gamma.pdf(Y_prop_val, a=f_sh, scale=f_sc) # had g
        tgt_dist = gamma.pdf(x, a=f_sh, scale=f_sc) # had tgt_val, now x

        A = prop_dist/tgt_dist
        B = q_x/q_y
        accept_p = min(1, A*B)
        if np.random.random() < accept_p:
            x = Y_prop_val
        X.append(x)
    return X

X1 = metropolis_hastings(g_sh, g_sc)
print('X1:', len(X1), X1[-5:])

# c) Metropolis-Hastings with Gamma(5, 6) candidate
g_sh = 5
g_sc = 6

X2 = metropolis_hastings(g_sh, g_sc)
print('X2:', len(X2), X2[-5:])



# plot convergence of 3 estimators to 26.66, true est. value of a Gamma(4.3, 6.2) random variable
f_mean = f_sh * f_sc # mean = shape * scale
def running_mean(x):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return [cumsum[i]/i for i, sum in enumerate(cumsum)][1:]

fig = plt.figure()
X_running_mean = running_mean(X)
X1_running_mean = running_mean(X1)
X2_running_mean = running_mean(X2)
print('X final value:', X_running_mean[-1])
print('X1 final value:', X1_running_mean[-1])
print('X2 final value:', X2_running_mean[-1])
plt.plot(range(len(X)), X_running_mean, linewidth=1)
plt.plot(range(len(X1)), X1_running_mean, linewidth=1, color='red')
plt.plot(range(len(X2)), X2_running_mean, linewidth=1, color='green')
plt.grid()
plt.xlabel('Iterations')
plt.ylabel('E[X]')
plt.title('Convergence to Gamma(4.3, 6.2) Mean')
plt.legend(['Accept-Reject with Gamma(4, 7)',
            'Metropolis-Hastings with Gamma(4, 7)',
            'Metropolis-Hastings with Gamma(5, 6)'])
fig.savefig('convergence.png', dpi=300)
plt.show()
