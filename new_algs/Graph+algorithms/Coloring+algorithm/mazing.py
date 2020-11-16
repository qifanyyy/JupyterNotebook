import matplotlib.pyplot as plt, matplotlib.animation as ani
from matplotlib.animation import FFMpegWriter
import sys, os, resource, numpy as np, scipy.ndimage as ndi


def check_mem_usage():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def render(matrices, speedOfLife, save, fileNameOut):
    f = plt.figure()
    reel = []
    for matrix in matrices:
        frame = plt.imshow(matrix,'gray_r')
        reel.append([frame])
    a = ani.ArtistAnimation(f, reel, interval=speedOfLife,blit=True,repeat_delay=1000)
    ''' TODO: Add save2gif ability '''
    frame_rate = speedOfLife
    if save:
        writer = FFMpegWriter(fps=frame_rate, metadata=dict(artist='Me'), bitrate=1800)
        a.save(fileNameOut, writer=writer)
    plt.show()

def simulate(ngen, filter, seed):
    gen = 0
    generations = []

    while gen <= ngen:
        ii = 0
        world = ndi.convolve(seed,filter,origin=0)
        nextstate = seed.flatten()
        for cell in world.flatten():
            if cell == 42 or cell > 45:
                nextstate[ii] = 1
            if cell >= 32 and nextstate[ii] == 1:
                nextstate[ii] = 0
            if nextstate[ii] ==0 and cell == 22:
                nextstate[ii] = 1
            if nextstate[ii] == 1 and cell == 26:
                nextstate[ii]== 0
            if nextstate[ii] == 0 and cell == 1:
                nextstate[ii] = 1
            ii += 1

        seed = nextstate.reshape(seed.shape)
        generations.append(seed)
        gen += 1
    return generations


def crawler(density,ngenerations):
    # Create a random bit plane seed that is 100x100
    seed = np.array((np.random.randint(0, 128, 10000).reshape((100, 100)) > density), dtype=int)
    # Using a quirky little 7x7 kernel that tends to favor dense
    # edges or corners
    filter1 = [[2, 2, 2, 1, 2, 2, 2],
               [2, 1, 1, 1, 1, 1, 2],
               [2, 1, 0, 0, 0, 1, 1],
               [1, 1, 0, 1, 0, 1, 1],
               [2, 1, 0, 0, 0, 1, 1],
               [2, 1, 1, 1, 1, 1, 2],
               [2, 2, 2, 1, 2, 2, 2]]

    # Run the simulation using the seed and filter created above
    sim = simulate(ngenerations, filter1, seed)
    # render(sim, 100)
    f,ax = plt.subplots(1,2)
    ax[0].imshow(seed, 'gray_r')
    ax[0].set_title('Initial State')
    ax[1].imshow(sim.pop(), 'gray')
    ax[1].set_title('Final State')
    plt.show()
    return sim

def main():
    crawler(75, 95)
    crawler(82, 75)
    crawler(85, 150)
    crawler(95, 150)
    sim = crawler(100, 150)
    render(sim,50,True,'mazy.mp4')


if __name__ == '__main__':
    main()
