from bruteforce import BF
from nearestneighbour import NN
from utilities import calc_distances, Moon
from string import ascii_lowercase
from decimal import Decimal
import random
import timeit
import functools
import sys


def print_analysis(results):
    # redirect all prints to our file
    sys.stdout = open("analysis_output.txt", "w")

    print("Analysis Results")
    print("-" * len("Analysis Results"))
    print()
    print("n: number of vertices")
    print("NN: average time(seconds) in order to complete the nearest neighbour algorithm")
    print("NN trials: number of times the algorithm was run for n")
    print("BF: average time(seconds) in order to complete the brute force algorithm")
    print("BF trials: number of times the algorithm was run for n")
    print()

    print('{:3s}'.format("n"), end="|", flush=True)
    print('{:>10s}'.format("NN"), end="|", flush=True)
    print('{:>10s}'.format("NN trials"), end="|", flush=True)
    print('{:>10s}'.format("BF"), end="|", flush=True)
    print('{:>10s}'.format("BF trials"), end="|\n", flush=True)

    for result in results:
        print('{:<3d}'.format(result["n"]), end="|", flush=True)
        print('{:10.2E}'.format(Decimal(result["NN"])), end="|", flush=True)
        print('{:10d}'.format(result["NN trials"]), end="|", flush=True)
        print('{:10.2E}'.format(Decimal(result["BF"])), end="|", flush=True)
        print('{:10d}'.format(result["BF trials"]), end="|\n", flush=True)


if __name__ == "__main__":
    random.seed(1)
    results = []

    for N in range(2, 13):
        moons = []
        result = {"n": N}
        for i in range(N):
            moon = Moon(ascii_lowercase[i], random.randint(1,13000))
            moons.append(moon)

        distances = calc_distances(moons)

        NN_timer = timeit.Timer(functools.partial(NN, distances, moons[0], moons))
        NN_results = NN_timer.autorange()
        result["NN"] = NN_results[1]/NN_results[0]
        result["NN trials"] = NN_results[0]

        BF_timer = timeit.Timer(functools.partial(BF, distances, moons[0], moons))
        BF_results = BF_timer.autorange()
        result["BF"] = BF_results[1]/BF_results[0]
        result["BF trials"] = BF_results[0]

        results.append(result)

    print_analysis(results)
