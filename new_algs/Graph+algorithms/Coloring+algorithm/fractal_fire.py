import sys, time, numpy as np, scipy.ndimage as ndi
import matplotlib.pyplot as plt, matplotlib.animation as animation
import utility

def render(matrices, isColor, speed):
    reel = []
    f = plt.figure()
    for frames in matrices:
        if isColor:
            reel.append([plt.imshow(frames)])
        else:
            reel.append([plt.imshow(frames, 'gray_r')])
    a = animation.ArtistAnimation(f, reel, interval=speed, blit=True, repeat_delay=500)
    plt.show()


def burn(initial_state, ngen, filta):
    gen = 0
    generations = []
    while gen < ngen:
        generations.append(initial_state)
        world = ndi.convolve(initial_state, filta)
        initial_state = fractal_flames(initial_state.flatten(), world).reshape(initial_state.shape)
        gen += 1
    return generations


def fractal_flames(nextstate, world):
    ii = 0

    for cell in world.flatten():
        if 6 == cell or cell == 8 or cell == 17:
            nextstate[ii] += 1
        if cell == 9 or cell == 3 or cell == 12:
            nextstate[ii] = 1
        if cell == 3 or cell == 5 or cell == 7:
            nextstate[ii] = 0
        ii += 1
    return nextstate


def build_log(dims, isShown):
    width = dims[0]
    height = dims[1]
    canvas = np.zeros((width, height))
    canvas[width-10:width,:] = 1
    ii = 0
    for x in np.arange(width-10, width, 1):
        for y in np.arange(0, height, 1):
            if ii % 3 ==0:
                canvas[x,y] = 0
            ii += 1
    if isShown:
        plt.imshow(canvas,'gray_r')
        plt.title('LOG [Seed Image]')
        plt.show()

    return canvas.reshape(dims)


def main():
    spark = [[2, 2, 2], [2, 1, 2], [2, 2, 2]]
    nFrames = 220
    gas = build_log([100, 100], False)

    if '-coal' in sys.argv:
        coal = np.zeros((200, 200))
        coal[50:150, 50:150] = 1
        small_fire = burn(coal, nFrames, spark)
        if '-save' in sys.argv:
            utility.bw_render(small_fire,70, True,'large_coal.mp4')
        else:
            render(small_fire, False, 70)

        coal = np.zeros((200, 200))
        coal[75:100, 75:100] = 1
        fire = burn(coal, nFrames, spark)
        if '-save' in sys.argv:
            utility.bw_render(fire,70, True,'small_coal.mp4')
        else:
            render(fire, False, 70)

    if '-log' in sys.argv:
        s0 = time.time()
        flames = burn(gas, nFrames, spark)
        print (str(nFrames) + " Frame Simulation finished [" + str(time.time() - s0) + "s]")
        if '-save' in sys.argv:
            utility.bw_render(flames,70,True,'fractalFireLog.mp4')
        else:
            render(flames, False, 70)


if __name__ == '__main__':
    main()
