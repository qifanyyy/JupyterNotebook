import matplotlib.pyplot as plt
import sys, time, numpy as np, utility


class Swarm:
    n_particles = 0
    fuel = 200
    dimensions = []
    state = [[]]
    verbosity = False

    def __init__(self, n, verbose):
        self.n_particles = n
        self.dimensions = self.set_canvas_size()
        self.verbosity = verbose
        self.state = np.zeros(self.dimensions)
        if self.verbosity:
            self.fuel = int(input("How many steps to initialize each particle with?:"))
        self.add_particles(self.verbosity)

    @staticmethod
    def set_canvas_size():
        resolutions = {}
        ii = 0
        for i in range(25, 125, 25):
            x = 8 * (i + 1)
            y = 6 * (i + 1)
            resolutions[ii] = [x, y]
            ii += 1
            print (str(ii) + '] ' + str(resolutions[ii - 1]))
        selection = int(input("Select a Resolution: "))
        if 4 >= selection >= 1:
            print ("Good Choice.")
            return resolutions[selection]
        else:
            exit(0)

    def add_particles(self, show):
        Particles = {}
        history = []
        for pt in range(self.n_particles):
            location = utility.spawn_random_point(self.state)
            self.state[location[0], location[1]] = 1
            history.append(self.state)
            Particles[pt] = Particle(location, self.state, self.fuel)
            for frame in Particles[pt].data:
                history.append(frame)
        if show:
            plt.imshow(self.state, 'gray_r')
            plt.show()

            utility.bw_render(history,10,False,'')


class Particle:
    n_steps = 0
    pos = []
    value = 0
    others = {}
    path = []
    data = []
    state = [[]]

    def __init__(self, location, state, depth):
        self.pos = location
        self.value = state[location[0], location[1]]
        self.n_steps = depth
        self.path, self.state = self.generate_random_path(state)

    def generate_random_path(self, state):
        steps = []
        for step in np.random.randint(1, 10, self.n_steps):
            self.data.append(self.state)
            directions = {1: [self.pos[0]-1, self.pos[1]-1],
                          2: [self.pos[0], self.pos[1]-1],
                          3: [self.pos[0]+1, self.pos[1]-1],
                          4: [self.pos[0]-1, self.pos[1]],
                          5: [self.pos[0], self.pos[1]],
                          6: [self.pos[0]+1, self.pos[1]],
                          7: [self.pos[0]-1,self.pos[1]+1],
                          8: [self.pos[0], self.pos[1]+1],
                          9: [self.pos[0]+1, self.pos[1]+1]}
            try:
                steps.append(self.pos)
                state[self.pos[0], self.pos[1]] = 1
                self.pos = directions[step]
            except IndexError:
                break
        return steps, state


def main():
    N = 100
    if len(sys.argv) > 1:
        try:
            N = int(sys.argv[1])
        except ValueError:
            print (str(sys.argv[1]) + " is not a valid number of particles")
            exit(0)
    print ('\033[1m\033[32mCreating a SWARM \033[31m[' + str(N) + ' Particles]\033[0m')

    t0 = time.time()
    s = Swarm(N, True)
    print ("Swarm Initialized ["+'\033[1m\033[34m'+str(time.time()-t0)+'s\033[0m]')


if __name__ == '__main__':
    main()
