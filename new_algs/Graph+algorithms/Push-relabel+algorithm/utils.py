# 1kkk
import argparse
import time


class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print("Elapsed time: {:.3f} sec".format(time.time() - self._startTime))


class edge:
    def __init__(self, flow=0, cup=0):
        self.flow = flow
        self.cup = cup


def printMatrix(M):
    n = len(M)
    for i in range(n):
        for j in range(n):
            print(M[i][j], end=' ')
        print()


def matrix_to_str(M):
    result = ''
    for i in range(len(M)):
        for j in range(len(M)):
            result += str(M[i][j]) + ' '
        result += '\n'
    return result


def get_matrix_stats(M):
    vertexes = len(M)
    edges = 0
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] != 0:
                edges += 1
    return {'e': edges, 'v': vertexes}


def log_report(*args):
    # print(' '.join(map(str, args)))
    with open('log.log', 'a') as file:
        file.write(' '.join(map(str, args)))


def clear_log():
    with open('log.log', 'w') as file:
        file.write('')
    print("Log is cleared")


def generator_read_file(name):
    file = open(name, 'r')
    n = int(file.readline())
    while file.readline():
        M = []
        for i in range(n):
            line = file.readline()
            M.append(list(map(int, line.split())))
        yield M


def parse_gen_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int)
    parser.add_argument('-m', type=int)
    parser.add_argument('-cup', type=int)
    parser.add_argument('-max_cup', type=int)
    parser.add_argument('-file', type=str)
    return parser.parse_args(args)
