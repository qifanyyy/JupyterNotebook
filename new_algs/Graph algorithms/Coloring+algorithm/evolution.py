import numpy as np, scipy.ndimage as ndi
import utility, time, sys


class Evolve:
    lifetime = 0
    state = [[]]
    kernel = [[]]
    k_threshold = 0
    score = 0

    def __init__(self, n_generation, seed, filter):
        self.lifetime = n_generation
        self.state = seed
        self.kernel = filter

    def set_target(self, manual, val):
        if manual:
            self.k_threshold = int(input('Enter the threshold to use:'))
            print np.array(self.kernel)
        else:
            self.k_threshold = val

    def evolve(self, agent, usingAI):
        history = []
        for i in range(self.lifetime):
            history.append(np.array(self.state))
            # Update organism
            agent.state = self.state
            if usingAI:
                self.state = agent.antibacterial(self.k_threshold)
                history.append(np.array(self.state))
            # Update State
            self.run()
        return history

    def run(self):
        world = ndi.convolve(self.state, self.kernel)
        nextstate = self.state.flatten()
        ii = 0
        for cell in world.flatten():
            if cell >= self.k_threshold and nextstate[ii] == 0:
                nextstate[ii] = 1
            ii += 1
        self.state = nextstate.reshape(np.array(self.state).shape)


class Organism:
    worldview = [[]]
    state = [[]]
    energy_level = 0
    cells = {}

    def __init__(self, world, cells):
        self.state = np.array(world)
        self.cells = cells
        self.worldview = np.array([[1,2,1],[1,0,1],[1,2,1]])
        self.fractalize = np.array([[1,1,1],[1,0,1],[1,1,1]])

    def antibacterial(self, k_threshold):
        world = ndi.convolve(self.state, self.worldview)
        alt_world = ndi.convolve(self.state, self.fractalize).flatten()
        nextstate = self.state.flatten()
        ii = 0
        for cell in world.flatten():
            alt = alt_world[ii]
            # Sanitize
            if cell%6 == 0 and nextstate[ii]==1:
                nextstate[ii] -= 1
            # But Also accelerate long term
            if alt == 8 and nextstate[ii] ==1:
                nextstate[ii] += 1
            ii += 1
        self.state = nextstate.reshape(np.array(self.state).shape)
        return self.state


def create_seed_image(density, dimensions):
    state = np.zeros(dimensions)
    pts = {}
    for i in range(density):
        pt = utility.spawn_random_point(state)
        state[pt[0],pt[1]] = 1
        pts[i] = pt
    return state, pts


def simulate(density, dims, thresh, t0, kernel, ai):
    test_img, seed_pts = create_seed_image(density, dims)
    evo = Evolve(250, test_img, kernel)
    evo.set_target(False, thresh)
    # Create an organism to inject into this bacterial environment
    eve = Organism(test_img, seed_pts)

    if ai:
        history = evo.evolve(eve, True)
    else:
        history = evo.evolve(eve,False)
    print '\033[33m\033[1m FINISHED SIMULATION \033[0m\033[1m[' + \
          str(time.time() - t0) + 's Elapsed]\033[0m'
    return history


def main():
    t0 = time.time()
    ''' 4 is highly complex  but fast '''
    f0 = [[1,1,1],[1,1,1],[1,1,1]]
    f1 = [[1, 1, 1], [1, 2, 1], [1, 1, 1]]

    if '-bleed' in sys.argv:
        history_5 = simulate(density=10000, dims=[320, 320], thresh=4, t0=t0, kernel=f0, ai=False)
        utility.bw_render(history_5, 100, False, 'decay.mp4')
        exit(0)
    if '-bacterial':
        history_5 = simulate(density=20000, dims=[350, 350], thresh=4, t0=t0, kernel=f1, ai=True)
        utility.color_render(history_5, 65, False , 'organisms.mp4')
        exit(0)



if __name__ == '__main__':
    main()
