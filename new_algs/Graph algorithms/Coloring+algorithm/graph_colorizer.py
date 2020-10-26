import random


class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []

    def __str__(self):
        return 'Nodes: {}, Edges: {}.'.format(len(self.vertices),
                                              len(self.edges))


class GraphColorizer:
    def __init__(self, filename, parameters):
        self.graph = self._load_graph(filename)
        self.N = parameters['N']
        self.T = parameters['T']
        self.population_size = parameters['population_size']
        self.mutation_probability = parameters['mutation_probability']
        self.crossover_probability = parameters['crossover_probability']
        self.max_no_improvements = parameters['max_no_improvements']
        self.number_of_vertices = len(self.graph.vertices)
        self.number_of_edges = len(self.graph.edges)
        self.length_of_individual = self._bits_for_vertex(
            self.number_of_vertices)

    def colorize(self):
        """The only public method, used to start execution of the ga."""
        results = []
        for n in range(self.N):
            results.append(self._colorize(n))
        return results

    def run_statistics(self):
        results = []
        for n in range(self.N):
            results.append(self._run_stats(n))
        return results

    def generations_statistics(self):
        return self._generations_stats()

    def _fitness(self, individual):
        """Fitness functions calculating a number of colors used. We want to
        maximize that.
        """
        coloring = self._decode(individual)
        return 100 * self.number_of_vertices / len(set([k for _, k in coloring]))

    def _colorize(self, n):
        """Main function performed by our GA."""
        print('Starting run number {}'.format(n))
        population = self._initialize()
        print('Population initialized...')
        t = 0
        solutions = [(self._best(population))]
        while not self._stop_condition_reached(t, solutions):
            population = self._selection(population)
            population = self._crossover(population)
            population = self._mutation(population)
            solutions.append(self._best(population))
            t += 1
        return self._best_solution(solutions)

    def _run_stats(self, n):
        print('Starting run number {}'.format(n))
        population = self._initialize()
        print('Population initialized...')
        t = 0
        solutions = [(self._best(population))]
        while not self._stop_condition_reached(t, solutions):
            population = self._selection(population)
            population = self._crossover(population)
            population = self._mutation(population)
            solutions.append(self._best(population))
            t += 1
        return self._stats(solutions)

    def _generations_stats(self):
        print('Starting run number {}'.format(0))
        population = self._initialize()
        print('Population initialized...')
        t = 0
        solutions = [self._bwa(population)]
        while not self._stop_condition_reached(t, solutions):
            population = self._selection(population)
            population = self._crossover(population)
            population = self._mutation(population)
            solutions.append(self._bwa(population))
            t += 1
        return solutions

    def _bwa(self, population):
        fitnesses = self._fitnesses(population)
        best = max([f for _, f in fitnesses])
        worst = min([f for _, f in fitnesses])
        average = sum([f for _, f in fitnesses]) / len(fitnesses)

        return best, worst, average

    def _initialize(self):
        """Create the initial population. We randomly choose as many
        individuals as is set in self.population_size. To population in T = 0
        goes only valid graphs.
        """
        v = self.graph.vertices
        random.seed()
        population = []
        while len(population) < self.population_size:
            colors = [i for i in range(len(v))]
            coloring = []
            for i in range(len(v)):
                vertex = i + 1
                chosen_color = random.choice(colors)
                coloring.append((vertex, chosen_color))
            if self._is_valid(coloring):
                individual = self._encode(coloring)
                population.append(individual)
        return population

    def _encode(self, coloring, individual_len=None):
        """Encode the vertices into one long binary sequence. The vertex
        number 1 is most righte number 2 second from right etc.
        """
        if individual_len is None:
            individual_len = self.length_of_individual

        individual = 0
        for w, k in coloring:
            individual |= k << (w * individual_len)
        return individual

    def _decode(self, individual, individual_len=None, num_of_vertices=None):
        """Reverse function to _encode. We first create mask to extract
        chosen color and then bitshift right to obtain an actual number.
        """
        if individual_len is None:
            individual_len = self.length_of_individual
        if num_of_vertices is None:
            num_of_vertices = self.number_of_vertices

        coloring = []
        mask = 0
        for i in range(individual_len):
            mask |= 1 << i

        for i in range(num_of_vertices):
            vertex = i + 1
            current_mask = mask << (vertex * individual_len)
            color = (individual & current_mask) >> (vertex * individual_len)
            coloring.append((vertex, color))

        return coloring

    def _is_valid(self, coloring):
        """Coloring is valid iff every two vertices in evry edge have two
        different colors.
        """
        e = self.graph.edges
        c = coloring
        return all(self._color(w1, c) != self._color(w2, c) for w1, w2 in e)

    def _color(self, vertex, coloring):
        """Returns color in coloring palette given vertex number."""
        for v, c in coloring:
            if v == vertex:
                return c

    def _stop_condition_reached(self, t, solutions):
        """Stop condition of the GA. Possible causes:
        *) Achieved limit of iterations
        *) No improvement in last x iterations
        """
        no_improv_time = self.max_no_improvements
        no_improvement = False
        if t > no_improv_time:
            no_improvement = self._no_improvements(solutions, no_improv_time)
        return t == self.T or no_improvement

    def _no_improvements(self, wyniki, k):
        newest = wyniki[-1]
        k_previous = wyniki[-k:-1]
        k_ago = k_previous[0]
        return newest[1] <= k_ago[1]

    def _solution_exist(self, population):
        """Returns true if in population exist individual with valid solution.
        """
        return any([self._is_valid(self._decode(individual)) for individual in
                    population])

    def _stats(self, solutions):
        best = max([f for _, f in solutions])
        worst = min([f for _, f in solutions])
        avg = sum([f for _, f in solutions]) / len(solutions)

        return best, worst, avg

    def _best_solution(self, solutions):
        """Returns best individual and his fitness from list of solutions."""
        best_individual, best_score = solutions[0]
        for individual, score in solutions:
            if score > best_score:
                best_individual, best_score = individual, score
        return best_individual, best_score

    def _fitnesses(self, population):
        """Returns list of tuples in form of (individual, fitness(individual)).
        """
        return [(individual, self._fitness(individual)) for individual in
                population]

    def _selection(self, population):
        """Selection of individuals to reproduction. The number of selected
        individuals is equal to floor(len(population) / 2). Each individual is
        given chances to be selected based on his fitness function. We then
        draw a number and accept the first individual with chance greater then
        this number.
        """
        fitnesses = self._fitnesses(population)

        fitnesses_acc = 0
        before_selection = []
        for individual, fitness in fitnesses:
            fitnesses_acc += fitness
            before_selection.append((individual, fitnesses_acc))

        after_selection = []
        for i in range(self.population_size):
            selected_individual = self._roulette_selection(before_selection,
                                                           fitnesses_acc)
            after_selection.append(selected_individual)

        return after_selection

    def _roulette_selection(self, before_selection, fitnesses_total):
        draw = random.randint(0, int(fitnesses_total))
        for individual, fitness_margin in before_selection:
            if fitness_margin >= draw:
                return individual

    def _crossover(self, population):
        """Randomly choose two individuals to perform crossover. Repeat until
        number of individual in population is as before selection.
        """
        pairs = []
        for i in range(self.population_size // 2):
            individual1 = random.choice(population)
            individual2 = random.choice(population)
            pairs.append((individual1, individual2))

        after_crossover = []
        for c1, c2 in pairs:
            after_crossover.extend(self._crossover_individuales(c1, c2))

        return after_crossover

    def _crossover_individuales(self, c1, c2):
        """Perform crossover with fixed probability. Then randomly choose
        point where two individuals will crossover.
        """
        if random.uniform(0.0, 1.0) < self.crossover_probability:
            crossover_point = random.randint(0, self.length_of_individual)
            mask = 0
            for i in range(crossover_point):
                mask |= 1 << i
            new_c1 = (c1 & mask) | (c2 & ~mask)
            new_c2 = (c1 & ~mask) | (c2 & mask)
            return new_c1, new_c2
        else:
            return c1, c2

    def _mutation(self, population):
        """Perform mutation on every individual with fixed probability."""
        after_mutation = []
        for individual in population:
            after_mutation.append(self._mutate_individual(individual))

        return after_mutation

    def _mutate_individual(self, individual):
        for position in range(self.length_of_individual):
            if random.uniform(0.0, 1.0) < self.mutation_probability:
                individual = self._change_bit(individual, position)
        return individual

    def _change_bit(self, individual, position):
        if individual & (1 << position):
            return individual & ~(1 << position)
        else:
            return individual | (1 << position)

    def _best(self, population):
        """Choose the best individual from set of acceptable solutions and
        return him with his fitness. In case of no acceptable solution print
        an error message.
        """
        colorings = [self._decode(individual) for individual in population]
        acceptable = [self._encode(coloring) for coloring in colorings
                      if self._is_valid(coloring)]
        try:
            best_individual = acceptable[0]
            best_fitness = self._fitness(acceptable[0])
        except IndexError:
            print('Error! Acceptable solution not found.')
            best_individual, best_fitness = None, None
        return best_individual, best_fitness

    def _load_graph(self, path):
        """Load graph from file."""
        graph = Graph()
        with open(path, mode='r') as f:
            for line in f.readlines():
                if line.split()[0] == 'e':
                    _, w1, w2, _ = line.split()
                    if w1 != w2:
                        graph.edges.append((int(w1), int(w2)))
                elif line.split()[0] == 'n':
                    _, w, _ = line.split()
                    graph.vertices.append(int(w))

        return graph

    def _bits_for_vertex(self, v):
        """Calculates number of bits necessary for decoding every vertex's
        color.
        """
        i = 1
        while 2 ** i <= v:
            i += 1
        return i
