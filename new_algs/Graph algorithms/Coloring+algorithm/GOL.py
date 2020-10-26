import matplotlib.pyplot as plt, matplotlib.animation as animation
import numpy as np, scipy.ndimage as ndi, time, resource, sys
from matplotlib.animation import FFMpegWriter


def render(matrices, speedOfLife, save, fileNameOut):
    f = plt.figure()
    reel = []
    for matrix in matrices:
        frame = plt.imshow(matrix,'gray')
        reel.append([frame])
    a = animation.ArtistAnimation(f, reel, interval=speedOfLife,blit=True,repeat_delay=1000)
    if save:
        frame_rate = speedOfLife
        writer = FFMpegWriter(fps=frame_rate, metadata=dict(artist='Me'), bitrate=1800)
        a.save(fileNameOut, writer=writer)
    plt.show()


def initialize_life():
    width = int(input('Enter width: '))
    height = int(input('Enter height: '))
    initial_state = np.random.randn(width * height).reshape((width, height)) > 0.5
    plt.imshow(initial_state, 'gray_r')
    plt.title('Initial State [GOL]')
    plt.show()

    initial = np.array(initial_state,dtype=int)
    return initial


def run(nGenerations, speed, seed, title):
    neighbors = [[1, 1, 1],
                 [1, 0, 1],
                 [1, 1, 1]]

    generations = []
    gen = 0
    start = time.time()
    while gen <= nGenerations:
        cells = ndi.convolve(seed, neighbors)
        nextState = seed.flatten()
        II = 0
        for cell in cells.flatten():
            # Check if its alive
            if nextState[II] == 1:
                if 2 <= cell < 4:
                    nextState[II] = 1
                else:
                    nextState[II] = 0
            elif cell == 3:
                nextState[II] = 1
            II += 1
        generations.append(nextState.reshape((seed.shape[0], seed.shape[1])))
        gen += 1
        seed = nextState.reshape((seed.shape[0], seed.shape[1]))
    # Animate the Game of Life Simulation!
    render(generations, speed, True, title)
    print "Finished Simulating" + str(nGenerations)+\
          " [" + str(time.time() - start) + "s Elapsed]"
    return generations


def check_mem_usage():
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return mem


def main():
    if len(sys.argv) <= 1 or '-classic' in sys.argv:
        print str(float(100 * check_mem_usage()) / 100000) + " Kb of initial RAM Overhead"
        # Create initial State
        initial_state = initialize_life()
        # Run the Simulation
        run(int(input('Enter Number of Generations to Simulate: ')),
            int(input('Enter Speed of Life [0-100]:\n') * 100 / 100), initial_state, "GOL.mp4")
        print str(float(100 * check_mem_usage()) / 100000) + " Kb of RAM Used"

    ''' Alternatively, you can run some interesting preconfigured initial states'''

    # Centered Box Starting State
    if '-box' in sys.argv:
        print str(float(100 * check_mem_usage()) / 100000) + " Kb of initial RAM Overhead"
        initial_state = np.zeros((150,150))
        # Create a simple box
        initial_state[50:100,50:100] = 1
        run(100,50,initial_state, 'box')
        print str(float(100 * check_mem_usage()) / 100000) + " Kb of RAM Used"

    # Checkerboard initial state
    if '-spots' in sys.argv:
        print str(float(100 * check_mem_usage()) / 100000) + " Kb of initial RAM Overhead"
        initial_state = np.zeros((150, 150))

        # putting a dissected box in top left corner
        initial_state[10:20,10:20] = 1
        initial_state[50:60,10:20] = 1
        initial_state[10:20,50:60] = 1
        initial_state[50:60,50:60] = 1
        initial_state[10:20,25:45] = 1
        initial_state[50:60,25:45] = 1
        initial_state[25:45,10:20] = 1
        initial_state[25:45,50:60] = 1

        # Putting random noise in lower right corner
        initial_state[80:150, 80:150] = np.random.randint(0, 2, 4900).reshape((70, 70))
        initial_state[10:20,90:100] = 1
        initial_state[50:60,130:140] = 1
        initial_state[60:70, 10:20] = 1
        initial_state[80:90, 10:20] = 1
        plt.imshow(initial_state, 'gray_r')
        plt.show()

        # Concatenate a rotation of bitplane to create a larger, and symmetric, world
        i2 = np.rot90(initial_state,1)
        initial_state = np.concatenate((initial_state,i2),1)
        plt.imshow(initial_state,'gray_r')
        plt.show()

        # Run the Simulation
        run(100,75, initial_state, 'spots')
        print str(float(100 * check_mem_usage()) / 100000) + " Kb of RAM Used"


if __name__ == '__main__':
    main()
