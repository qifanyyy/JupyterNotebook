import numpy as np
import matplotlib.pyplot as plt

def default_cmap(x):
    if x == 1:
        return [0, 255, 0]
    else:
        return [255, 0, 0]
    
def colored(A, cmap):
    im = np.zeros((A.shape[0], A.shape[1], 3), dtype=np.int)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            im[i, j] = cmap(A[i, j])
    return im

def visualize_adjacency(title, A):
    """Visualize an adjacency matrix using matplotlib.

    Args:
        title (str): Name of image we're visualizing.
        A (np.ndarray): Adjacency matrix we're visualizing.
    """
    assert type(title) == str, "Title not a string!"
    assert len(A.shape) == 2, "Image array not 2D!"
    
    plt.figure(figsize=(7, 7))

    # Visualize adjacency matrix
    # We manually set the black value with `vmin`, and the white value with `vmax`
    plt.imshow(A, vmin=0.0, vmax=1.0, cmap="gray")

    # Give our plot a title -- this is purely cosmetic!
    plt.title(f"{title}, shape={A.shape}")

    # Show image
    plt.show()

def visualize_map(title, M, A=None, start=None, end=None, path=None, cmap=default_cmap):
    """Visualize a 2D array using matplotlib.

    Args:
        title (str): Name of map we're visualizing.
        M (np.ndarray): Map we're visualizing. Shape should be `(rows, cols)`.
        A (np.ndarray): Adjacency matrix of graph.
    """
    assert type(title) == str, "Title not a string!"
    assert len(M.shape) == 2, "Map array not 2D!"
    
    plt.imshow(colored(M, cmap))
    if start is not None:
        plt.scatter(start[1], start[0], color="blue", label="start")
    if end is not None:
        plt.scatter(end[1], end[0], color="yellow", label="end")
        
    m, n = M.shape

    def ids(l):
        p = [l // n, l % n]
        return p

    def flip(t):
        return [t[1], t[0]]
        
    if A is not None:

        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                if A[i, j]:
                    # print(f"({i}, {j}) {ids(i)} -> {ids(j)}")
                    icoords = flip(ids(i))
                    jcoords = flip(ids(j))
                    x = [icoords[0], jcoords[0]]
                    y = [icoords[1], jcoords[1]]
                    plt.scatter(ids(i)[1], ids(i)[0], color="black")#, label=f"{i}")
                    plt.plot(x, y, color="black", alpha=0.5)#, label=f"{i} -> {j}")
                   
    if path is not None:
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]

            ucoords = flip(ids(u))
            vcoords = flip(ids(v))
            x = [ucoords[0], vcoords[0]]
            y = [ucoords[1], vcoords[1]]
            plt.plot(x, y, color="black", alpha=0.5)#, label=f"{i} -> {j}")
                    
    if start or end:
        plt.legend()
        
    plt.title(title)
    plt.show()

def visualize_costs(title, M, costs, start=None, end=None):
    m, n = M.shape
    C = np.zeros(M.shape)
    for i in range(m):
        for j in range(n):
            C[i, j] = costs[i * n + j]
    
    if start is not None:
        plt.scatter(start[1], start[0], color="blue", label="start")
    if end is not None:
        plt.scatter(end[1], end[0], color="yellow", label="end")
    #np.max([x for x in costs if x != np.inf])
    plt.imshow(C)
    plt.colorbar()
    if start or end:
        plt.legend()
    plt.title(title)
    plt.show()
    
def plot_path(M, path):
    m, n = B.shape
    plt.imshow(colored(B, default_cmap))
    
    def ids(l):
        p = [l // m, l % m]
        return p
    
    def flip(t):
        return [t[1], t[0]]
    
    for i in range(len(p)-1):
        u, v = p[i], p[i+1]
        
        ucoords = flip(ids(u))
        vcoords = flip(ids(v))
        x = [ucoords[0], vcoords[0]]
        y = [ucoords[1], vcoords[1]]
        plt.plot(x, y, color="black", alpha=0.5)#, label=f"{i} -> {j}")
        
        
def visualize_path(M, p):
    # p is the path
    
    from IPython.display import HTML
    from matplotlib.animation import FuncAnimation
    from matplotlib.patches import Rectangle
    import matplotlib.pyplot as plt
    import numpy as np

    n = 2
    T = 5
    D = 0.4

    def interpolate(init, final):
        return np.tile(init, (1, T)) + (final - init) * np.linspace(0, 1, T)

    m, n = M.shape

    def ids(l):
        return [l // n, l % n]

    def flip(t):
        return [t[1], t[0]]

    ps = np.zeros((2, T * (len(p)-1)))
    for i in range(len(p)-1):
        u, v = p[i], p[i+1]
        ucoords = np.array(flip(ids(u))).reshape((2, 1))
        vcoords = np.array(flip(ids(v))).reshape((2, 1))
        ps[:, i*T:T*(i+1)] = interpolate(ucoords, vcoords)


    # from http://python4econ.blogspot.com/2013/03/matlabs-cylinder-command-in-python.html
    def cylinder(r, n):
        """
        Returns the unit cylinder that corresponds to the curve r.
        INPUTS:  r - a vector of radii
                 n - number of coordinates to return for each element in r

        OUTPUTS: x,y,z - coordinates of points
        """

        # ensure that r is a column vector
        r = np.atleast_2d(r)
        r_rows, r_cols = r.shape

        if r_cols > r_rows:
            r = r.T
        # find points along x and y axes
        points = np.linspace(0, 2 * np.pi, n + 1)
        x = np.cos(points) * r
        y = np.sin(points) * r

        # find points along z axis
        rpoints = np.atleast_2d(np.linspace(0, 1, len(r)))
        z = np.ones((1, n + 1)) * rpoints.T

        return x, y, z


    x, y, z = cylinder(D / 2, 100)
    x = x.squeeze()
    y = y.squeeze()
    z = z.squeeze()

    fig, ax = plt.subplots(figsize=(10, 10))
    plt.close(fig)

    ax.axis("equal")
    #ax.axis([-1.5, 1.5, -1.5, 1.5])
    p_data = ax.plot(ps[0, :], ps[1, :], color="C0")[0]
    ax.scatter(ps[0, :], ps[1, :], color="C0", marker=".")

    ax.imshow(colored(M, default_cmap))
    def update(i):
        p_data.set_data(ps[0, i] + x, ps[1, i] + y)
        ax.set_title(f"i = {i}")


    ani = FuncAnimation(fig, update, interval=100, frames=T*(len(p) - 1))
    return HTML(ani.to_html5_video())