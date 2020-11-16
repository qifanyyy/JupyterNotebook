import argparse
import operator
import sys
import textwrap

from .algorithms import dijkstra_mst, kruskal_mst, prim_mst
from .render import GraphRenderer
from .io_utils import loadtxt


ALGORITHMS = {'dijkstra': dijkstra_mst, 
              'kruskal': kruskal_mst, 
              'prim': prim_mst}
RENDER_OPTIONS = ('static', 'dynamic')
DEFAULT_GRAPH = './graphs/graph1.txt'

RESULT_DELIM = '='*50

def tuple_type(s):
    try:
        x, y = s.split(',')
        return int(x), int(y)
    except:
        raise argparse.ArgumentTypeError('size must be pair of integers')


class Runner:

    def __init__(self, argv=None):
        if argv is None:
            argv = sys.argv
        self._argv = argv
        self._parser = self._get_parser()

    def _get_parser(self):
        parser = argparse.ArgumentParser()

        parser.add_argument('-g', '--graph', 
                            default=DEFAULT_GRAPH,
                            help='the graph which mst will be drawn')
        parser.add_argument('-a', '--algorithm', 
                            choices=sorted(ALGORITHMS.keys()), default='kruskal',
                            help='algorithm used to find the minimum spanning tree')
        parser.add_argument('-v', '--verbose', 
                            default=0, type=int,
                            help='verbosity level (integer >= 0)')
        parser.add_argument('-s', '--show',
                            choices=RENDER_OPTIONS,
                            help='static or dynamic plotting of the mst')
        parser.add_argument('--gifpath', 
                            help='path of the gif file (use this option only when creating dynamic plots)')
        parser.add_argument('--size', dest='size', metavar='X,Y',
                            type=tuple_type, 
                            help='figure size')

        return parser

    def run(self):
        args = self._parser.parse_args(self._argv[1:])
        mst_algorithm = ALGORITHMS[args.algorithm]
        g = loadtxt(args.graph)
        verbose = args.verbose
        mst = mst_algorithm(g, verbose)
        
        trace = sorted(mst._trace, key=operator.itemgetter(1))
        trace = [(sorted(edge), w) for edge, w in trace]
        first, rest = trace[0], trace[1:]

        if verbose > 0:
            print(RESULT_DELIM)
        print(textwrap.indent(f'Result: {first[0][0]}, {first[0][1]}  {first[1]:<10.4f}', prefix=' '*4))
        print(textwrap.indent('\n'.join(f'{u}, {v}  {w:<10.4f}' for (u, v), w in rest), prefix=' '*12))
        
        show = args.show
        if show:
            renderer = GraphRenderer(figsize=args.size)
            if show == 'static':
                renderer.render_mst(g, mst)
            else:
                renderer.render_mst(g, mst, animated=True, trace=mst._trace, gifpath=args.gifpath)


def main():
    Runner().run()
