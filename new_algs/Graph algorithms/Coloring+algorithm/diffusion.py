import sys, time, numpy as np, scipy.ndimage as ndi
import matplotlib.pyplot as plt, matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter


def render(matrices, isColor, speed, save, nameOut):
    reel = []
    f = plt.figure()
    for frames in matrices:
        if isColor:
            reel.append([plt.imshow(frames)])
        else:
            reel.append([plt.imshow(frames, 'gray_r')])
    a = animation.ArtistAnimation(f, reel, interval=speed, blit=True, repeat_delay=500)
    if save:
        print "Saving Animation as "+nameOut
        writer = FFMpegWriter(fps=35, metadata=dict(artist='Me'), bitrate=1800)
        a.save(nameOut, writer=writer)
    plt.show()


def evaporate(ngen,state):
    gen = 0
    generations = []

    ev = [[1,1,1,1,1],  # [1]: 16 occurrences (16)
         [1,2,2,2,1],  # [2]: 8 occurrences (16)
         [1,2,3,2,1],  # [3]: 1 occurrance (3)
         [1,2,2,2,1],  # SUM 35 = Maxed out
         [1,1,1,1,1]]

    while gen < ngen:
        world = ndi.convolve(np.array(state),np.array(ev))
        dims = state.shape
        ii = 0
        state = state.flatten()
        for cell in world.flatten():
            if state[ii]==1 and cell <= 20:
                state[ii] = 0
            if state[ii]==0 and cell >= 20:
                state[ii] = 1
            ii += 1
        state = state.reshape(dims[0],dims[1])
        generations.append(state)
        gen += 1
    return generations


def parity_diffuse(ngen, state):
    gen = 0
    generations = []
    dfu = [[1, 1, 1, 1, 1],  # [1]: 16 occurrences (16)
           [1, 2, 2, 2, 1],  # [2]: 8 occurrences (16)
           [1, 2, 3, 2, 1],  # [3]: 1 occurrance (3)
           [1, 2, 2, 2, 1],  # SUM 35 = Maxed out
           [1, 1, 1, 1, 1]]

    while gen < ngen:
        world = ndi.convolve(np.array(state), np.array(dfu))
        dims = state.shape
        ii = 0
        state = state.flatten()
        for cell in world.flatten():
            if state[ii] == 0 and 30 > cell > 20:
                state[ii] = 1
            if state[ii] == 1 and 30 > cell > 20:
                state[ii] = 0
            if 5 <= cell < 20:
                state[ii] = 1
            ii += 1
        state = state.reshape(dims[0], dims[1])
        generations.append(state)
        gen += 1
    return generations


def diffuse(ngen,state):
    gen = 0
    generations = []
    dfu = [[1,1,1,1,1],  # [1]: 16 occurrences (16)
           [1,2,2,2,1],  # [2]: 8 occurrences (16)
           [1,2,1,2,1],  # [3]: 1 occurrance (3)
           [1,2,2,2,1],  # SUM 35 = Maxed out
           [1,1,1,1,1]]
    flipped = np.zeros((state.shape)).flatten()
    while gen < ngen:
        world = ndi.convolve(np.array(state), np.array(dfu))
        dims = state.shape
        ii = 0
        state = state.flatten()
        for cell in world.flatten():
            if state[ii] == 0 and 5 <= cell < 20:
                flipped[ii] += 1    # Adding time-evolving decay
                state[ii] = 1
            if cell >= 20:
                flipped[ii] += 1      # Adding time-evolving decay
                state[ii] = 0
            if flipped[ii] > 5:
                state[ii] = 0
            ii += 1
        state = state.reshape(dims[0],dims[1])
        generations.append(state)
        gen += 1
    return generations


def main():
    Debug = False
    ''' Create Geometric solid to be diffused '''
    seed = np.zeros((250, 250), dtype=int)
    seed[100:150, 100:150] = 1
    """ If No args, show all experiments """
    if len(sys.argv) <= 1:
        if Debug:
            plt.imshow(seed, 'gray_r')
            plt.show()

        ''' Do the simulation(s) '''
        print "Displaying Diffusion Experiment #1 [150 Generations]"
        s0t0 = time.time()
        simulation = diffuse(150, seed)
        s0t1 = time.time()
        ''' Show the results '''
        render(simulation, False, 100,False,'')
        print "Simulation Time: " + str(s0t1 - s0t0) + " seconds "

        print "Displaying Diffusion Experiment #2 [100 Generations]"
        s1t0 = time.time()
        simulation2 = parity_diffuse(100, seed)
        s1t1 = time.time()
        render(simulation2, False, 125,False, '')
        print "Simulation Time: " + str(s1t1 - s1t0) + " seconds "

        print "Displaying Diffusion Experiment #3 [150 Generations]"
        s2t0 = time.time()
        simulation3 = evaporate(150, seed)
        s2t1 = time.time()
        render(simulation3, False, 100,False,'')
        print "Simulation Time: " + str(s2t1 - s2t0) + " seconds "

    ''' If user provides args, run the experiment designated '''

    if '-evaporate' in sys.argv:
        print "Displaying Diffusion Experiment #3 [150 Generations]"
        s2t0 = time.time()
        simulation3 = evaporate(150, seed)
        s2t1 = time.time()
        render(simulation3, False, 100,False,'')
        print "Simulation Time: " + str(s2t1 - s2t0) + " seconds "

    if '-explode' in sys.argv:
        ''' Do the simulation(s) '''
        print "Displaying Diffusion Experiment #1 [150 Generations]"
        s0t0 = time.time()
        simulation = diffuse(150, seed)
        s0t1 = time.time()
        ''' Show the results '''
        render(simulation, False, 100,False,'')
        print "Simulation Time: " + str(s0t1 - s0t0) + " seconds "

    if '-mosaic' in sys.argv:
        print "Displaying Diffusion Experiment #2 [100 Generations]"
        s1t0 = time.time()
        simulation2 = parity_diffuse(100, seed)
        s1t1 = time.time()
        render(simulation2, False, 125,True,'mosaic.mp4')
        print "Simulation Time: " + str(s1t1 - s1t0) + " seconds "


if __name__ == '__main__':
    main()
