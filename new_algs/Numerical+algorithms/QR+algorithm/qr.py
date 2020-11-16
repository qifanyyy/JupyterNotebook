import numpy as np

def power_iteration(A, v=None):
    if v is None:
        v = np.random.normal(size=A.shape[1])
    v = v / np.linalg.norm(v)
    memo = []; memo.append(v)
    previous = np.empty(shape=A.shape[1])
    while True:
        previous[:] = v
        v = A @ v
        v = v / np.linalg.norm(v)
        memo.append(v)
        if np.all(np.abs(v - previous) < 0.00001):
            break
    return v, memo

def power_iteration_matrix(A):
    X = np.random.normal(size=A.shape)
    X, R = np.linalg.qr(X)
    memo = []; memo.append(X)
    previous = np.empty(shape=X.shape)
    for i in range(100):
        previous[:] = X
        Xp = A @ X
        X = Xp / np.linalg.norm(Xp, axis=0)
        memo.append(X)
        #X, R = np.linalg.qr(X)
        if np.all(np.abs(X - previous) < 0.00001):
            break
    return X, memo

def simultaneous_orthogonalization(A):
    X = np.eye(A.shape[0])
    Q, R = np.linalg.qr(X) 
    memo = []; memo.append(Q)
    previous = np.empty(shape=Q.shape)
    for i in range(100):
        previous[:] = Q
        X = A @ Q
        Q, R = np.linalg.qr(X)
        memo.append(Q)
        if np.all(np.abs(Q - previous) < 0.001):
            break
    return Q, memo

def qr_algorithm(A):
    X = np.random.normal(size=A.shape)
    Q, R = np.linalg.qr(A)
    memo_q = []; memo_q.append(Q)
    memo_r = []; memo_r.append(R)
    previous = np.empty(shape=Q.shape)
    for i in range(500):
        previous[:] = Q
        X = R @ Q
        Q, R = np.linalg.qr(X)
        memo_q.append(Q); memo_r.append(R)
        if np.allclose(X, np.triu(X), atol=10**-8): 
            break
    return Q, memo_q, memo_r


def plot_vector(ax, v, final_v=None):
    ax.auto_scale_xyz([-1, 1], [-1, 1], [-1, 1])
    if final_v is not None:
        ax.quiver(0, 0, 0, final_v[0], final_v[1], final_v[2], 
                  pivot='tail', color='black', alpha=0.5)
        t = np.linspace(-5, 5, num=250)
        ax.plot(t*final_v[0], t*final_v[1], t*final_v[2], color="black", alpha=0.2)
    for i in range(v.shape[0]):
        ax.quiver(0, 0, 0, v[0], v[1], v[2], 
                  pivot='tail', color='black')
    _setup_axies(ax)

def plot_basis(ax, Q, final_Q=None):
    ax.auto_scale_xyz([-1, 1], [-1, 1], [-1, 1])
    if final_Q is not None:
        for i in range(final_Q.shape[1]):
            ax.quiver(0, 0, 0, 
                      final_Q[0, i], final_Q[1, i], final_Q[2, i], 
                      pivot='tail', color='black', alpha=0.2,
                      zorder=0)
            t = np.linspace(-5, 5, num=250)
            ax.plot(t*final_Q[0, i], t*final_Q[1, i], t*final_Q[2, i], 
                    color="black", alpha=0.2)
    for i in range(Q.shape[1]):
        ax.quiver(0, 0, 0, Q[0, i], Q[1, i], Q[2, i], 
                  pivot='tail', color='black', zorder=10)
    _setup_axies(ax)

def _setup_axies(ax):
    ax.scatter([0], [0], [0], color='black', s=50)
    ax.set_xlim([-1, 1])
    ax.set_xlabel("$x$")
    ax.set_xticks([-1.0, 0.0, 1.0])
    ax.set_ylim([-1, 1])
    ax.set_ylabel("$y$")
    ax.set_yticks([-1.0, 0.0, 1.0])
    ax.set_zlim([-1, 1])
    ax.set_zlabel("$z$")
    ax.set_zticks([-1.0, 0.0, 1.0])
