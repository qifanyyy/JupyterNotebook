import sys, time, numpy as np, scipy.ndimage as ndi
import matplotlib.pyplot as plt, matplotlib.animation as animation


def render(matrices, isColor, speed):
    f = plt.figure()
    reel = []
    for frame in matrices:
        reel.append([plt.imshow(frame, 'gray_r')])
    a = animation.ArtistAnimation(f, reel, interval=speed, blit=True, repeat_delay=500)
    plt.show()


def simulate(ngeneration,initial_state,filter):
    gen = 0
    generations = []
    while ngeneration < gen:
        generations.append(initial_state)
        world = ndi.convolve(initial_state,filter)
        generations.append(world)
        gen += 1
    return generations


def create_seed_image():
    width = int(input('Enter a Width [int]:'))
    height = int(input('Enter a Height [int]:'))
    return np.random.randint(0, 2, width*height).reshape((width, height))


def main():
    height = 250
    width = 250
    DEBUG = True

    # ########### DEFINE IMAGE KERNEL FILTERS ########### #
    b0 = [[1,1,1],      # Key Nums:
          [1,1,1],      # [1, 3, 9]
          [1,1,1]]
    ''' <> '''
    c0 = [[1,1,0,1,1],  # Key Nums:
          [1,0,0,0,1],  # [1,3,6,9,10]
          [0,0,1,0,0],
          [1,0,0,0,1],
          [1,1,0,1,1]]

    ''' <Neural Kernels> '''
    f2 = [[1,0,1,1,0,1],  # Key Nums:
          [0,1,0,0,1,0],  # [4, 8, 10]
          [1,0,1,1,0,1],
          [1,0,1,1,0,1],
          [0,1,0,0,1,0],
          [1,0,1,1,0,1]]

    f3 = [[1,0,1,0,1],    # Key Nums:
          [0,1,1,1,0],    # []
          [1,1,1,1,1],
          [0,1,1,1,0],
          [1,0,1,0,1]]
    # ############ End of Kernel Definitions ############ #
    if '-manual' in sys.argv:
        seed = create_seed_image()
    else:
        seed = np.random.randint(0,2,width*height).reshape((width, height))

    if '-fine' in sys.argv:
        density = int(input('Enter density to use [1-255]:'))
        seed = np.random.randint(0, 255, width * height).reshape((width, height)) > density

    if DEBUG:
        f, ax = plt.subplots(1,2,sharex=True,sharey=True,figsize=(8,4))
        ax[0].imshow(seed, 'gray_r')
        ax[1].imshow(ndi.convolve(seed,c0,origin=0))
        plt.show()
    # Run the simulation
    sim = simulate(100, seed, b0)
    render(sim, False, 75)


if __name__ == '__main__':
    main()
