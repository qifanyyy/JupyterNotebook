import timeit
import functools
import itertools
import utilities


def BF(distances, initial_vertex, vertices):
    unvisited_vertices = list(vertices)
    unvisited_vertices.remove(initial_vertex)

    # enter the starting and ending point of our circuit
    min_circuit = [initial_vertex, initial_vertex]
    # create our initial circuit in order to have a min
    min_circuit[1:1] = unvisited_vertices
    # find its cost
    min_cost = 0
    for source, destination in zip(min_circuit, min_circuit[1:]):
        min_cost = min_cost + distances[source][destination]

    # create all permutations and test them
    permutations_iter = itertools.permutations(unvisited_vertices)
    for permutation in permutations_iter:
        circuit = [initial_vertex, initial_vertex]
        circuit[1:1] = permutation
        cost = 0
        for source, destination in zip(circuit, circuit[1:]):
            cost = cost + distances[source][destination]
        if cost < min_cost:
            min_circuit = circuit
            min_cost = cost
    return min_circuit, min_cost


if __name__ == "__main__":
    # build our moons array(our entry point is also considered a moon)
    moons = utilities.read_input('input.txt')

    # build our 2-D matrix with the distances
    distances = utilities.calc_distances(moons)

    # run the brute force algorithm
    circuit, cost = BF(distances, moons[0], moons)

    # calculate average running speed of BF for our problem
    t = timeit.Timer(functools.partial(BF, distances, moons[0], moons))
    timeit_results = t.autorange()

    # print the results from NN
    utilities.print_alg_results("brute force", distances, circuit, cost, timeit_results)
