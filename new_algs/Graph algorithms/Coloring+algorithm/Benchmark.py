import time
from GraphGen import genGraph
from Algorithms import WelshPowell
from IOHandling import outputBenchmarkResults, removeTmpFile, dumpTmpData, extractTmpData


"""Functions for testing algorithms complexity"""


def timing(f, *args):
    """
    Measure execution time of a function
    :param f: Function which execution time is measured
    :param args: Function's arguments
    :return: Tuple of two integers:
    number of used colors, measured time
    """
    time1 = time.time()
    _, colorsUsed = f(*args)
    time2 = time.time()
    return colorsUsed, time2 - time1


def testit(f, arguments):
    """
    Collect execution times of function f with different parameters, process it
    and pass it to function outputBenchmarkResults() to print it
    :param f: Function to test
    :param arguments: Values defining function f's arguments in each run

    """

    vertexNumber, density, divisibility, problemCount, step, instanceCount, useTmpfile = arguments

    infoToOutput = (f.__name__, vertexNumber, density, divisibility, problemCount, step, instanceCount)

    if useTmpfile:
        removeTmpFile()
        dumpTmpData((f.__name__, vertexNumber, density, divisibility, problemCount, step, instanceCount))

    data = []
    # data = [[vertexNumber, measuredTime, q(n), colorsUsed], ...]

    # warming up
    WelshPowell(genGraph(1000, 0.75, 5))

    for i in range(problemCount):
        data.append([])
        timeSum = 0.0
        edgeCount = 0
        colorsUsedSum = 0.0

        for _ in range(instanceCount):
            g = genGraph(vertexNumber+step*i, density, divisibility)
            edgeCount = g.getEdgeCount()
            colorsUsed, timeSpent = timing(f, g)
            colorsUsedSum += colorsUsed
            timeSum += timeSpent

        colorsUsedAvg = colorsUsedSum / instanceCount
        timeAvg = timeSum / instanceCount

        data[i].append(vertexNumber+step*i)
        data[i].append(timeAvg)
        data[i].append(edgeCount)
        data[i].append(colorsUsedAvg)

        if useTmpfile:
            dumpTmpData(data[i])

    tmedian, Tmedian = calcMedian(f.__name__, data)

    calcQ(f.__name__, data, tmedian, Tmedian)

    outputBenchmarkResults(infoToOutput, data)


def wComplexity(n):
    """
    Theoretical complexity of WelshPowell algorithm
    :param n: Number of vertices in graph
    :return: Calculated complexity of the algorithm
    """

    return n**2



def blComplexity(n, k, e):
    """
    Theoretical complexity of Brute Force algorithm with heuristics
    :param n: Number of vertices in graph
    :param s: Found minimal number of colors to use
    :param e: Number of edges in graph
    :return: Calculated complexity of the algorithm
    """

    return (k**n)*e + 1.44**n


def calcMedian(algorithm, data):
    """
    Calculate complexity of the algorithm for the median time
    :param algorithm: WelshPowell or Brute force with heuristics
    :param data: Data to calculate complexity
    :return: Tuple of integer and float:
    time of median, complexity of median
    """
    median = len(data) // 2
    tmedian = data[median][1]
    Tmedian = 0.0

    if algorithm == 'WelshPowell':
        Tmedian = wComplexity(data[median][0])
    elif algorithm == 'bruteForceWithHeuristics':
        Tmedian = blComplexity(data[median][0], data[median][3], data[median][2])

    return tmedian, Tmedian


def calcQ(algorithm, data, tmedian, Tmedian):
    """
    Calculate q value, how much measured time in data is off relatively to median time
    :param algorithm: WelshPowell or Brute force with heuristics
    :param data: Data to calculate complexity, the results are stored in it
    :param tmedian: Time of median
    :param Tmedian: Calculated complexity of median

    """
    complexity = 0.0
    for row in data:
        if algorithm == 'WelshPowell':
            complexity = wComplexity(row[0])
        elif algorithm == 'bruteForceWithHeuristics':
            complexity = blComplexity(row[0], row[3], row[2])
        q = row[1] * Tmedian / complexity / tmedian

        # seconds to ms
        row[1] = row[1] * 1000

        row[2] = q


if __name__ == '__main__':
    """
    Use as standalone to process data from temporary file
    """
    data = extractTmpData()
    info = data[0]
    algorithm = info[0]
    data = data[1:]
    tmedian, Tmedian = calcMedian(algorithm, data)
    calcQ(algorithm, data, tmedian, Tmedian)
    outputBenchmarkResults(info, data)
