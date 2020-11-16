"""
Parse and process user input
"""

import argparse
import sys


from Algorithms import WelshPowell, bruteForceWithHeuristics
from IOHandling import parseJsonInput, parseSimpleNotationInput
from GraphGen import genGraph
from Benchmark import testit


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Main.py', description='Program to color a graph')
    parser.add_argument('-g', action='store_true', help='Draw graph before and after coloring')
    subparsers = parser.add_subparsers(dest='scenario', help='sub-command help')

    parser_m1 = subparsers.add_parser('m1', help='Color graph provided via stdin')
    parser_m1.add_argument('-b', action='store_true', help='Use Brute force algorithm with heuristics')
    parser_m1.add_argument('-i', action='store_true', help='For simple graph notation usage')

    parser_m2 = subparsers.add_parser('m2', help='Generate instance of the problem and solve it')
    parser_m2.add_argument('-n', type=int, metavar='', help='Number of vertices')
    parser_m2.add_argument('-d', type=float, metavar='', help='Density of the graph')
    parser_m2.add_argument('-k', type=int, metavar='', help='Make graph k-divisible')
    parser_m2.add_argument('-b', action='store_true', help='Use Brute force algorithm with heuristics')

    parser_m3 = subparsers.add_parser('m3', help='Perform the benchmark')
    parser_m3.add_argument('-w', action='store_true', help='Use Welsh-Powell algorithm')
    parser_m3.add_argument('-b', action='store_true', help='Use Brute force algorithm with heuristics')

    parser_m3.add_argument('-n', type=int, metavar='', help='Number of vertices')
    parser_m3.add_argument('-d', type=float, metavar='', help='Density of the graph')
    parser_m3.add_argument('-k', type=int, metavar='', help='Make graph k-divisible')
    parser_m3.add_argument('-c', type=int, metavar='', help='Problem count')
    parser_m3.add_argument('-s', '-step', type=int, metavar='', help='Generate problems\' sizes with this step')
    parser_m3.add_argument('-r', type=int, metavar='', help='Number of generated instances for each size')
    parser_m3.add_argument('-f', action='store_true', default=False, help='Use temporary file to store results')

    # Parsing arguments
    args = vars(parser.parse_args())

    drawUnit = None
    if args['g']:
        from DrawUtils import DrawUnit
        drawUnit = DrawUnit()

    # Handle m1 scenario
    if args['scenario'] == 'm1':
        graph = parseSimpleNotationInput(sys.stdin) if args['i'] else parseJsonInput(sys.stdin)
        if args['g']:
            drawUnit.drawGraph(graph)
        solution = None
        solution = bruteForceWithHeuristics(graph) if args['b'] else WelshPowell(graph)
        print(solution)
        if args['g']:
            drawUnit.drawGraph(graph, solution)

    # Handle m2 scenario
    elif args['scenario'] == 'm2':
        if args['n'] is None:
            parser_m2.print_help()
            exit()
        vertexNumber = args['n']
        density = args['d']
        divisibility = args['k']
        graph = genGraph(vertexNumber, density, divisibility)
        if args['g']:
            drawUnit.drawGraph(graph)
        solution = None
        solution = bruteForceWithHeuristics(graph) if args['b'] else WelshPowell(graph)
        print(solution)
        if args['g']:
            drawUnit.drawGraph(graph, solution)

    # Handle m3 scenario
    elif args['scenario'] == 'm3':
        fun = None
        if args['w']:
            fun = WelshPowell
        elif args['b']:
            fun = bruteForceWithHeuristics
        else:
            parser_m3.print_help()
            exit()

        vertexNumber = args['n']
        density = args['d']
        divisibility = args['k']
        problemCount = args['c']
        step = args['s']
        instanceCount = args['r']
        useTmpFile = args['f']
        testit(fun, (vertexNumber, density, divisibility, problemCount, step, instanceCount, useTmpFile))

    # Wrong input, print help
    else:
        parser.print_help()



