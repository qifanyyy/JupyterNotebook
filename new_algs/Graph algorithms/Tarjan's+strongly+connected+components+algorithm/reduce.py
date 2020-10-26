import sys
sys.path.append("../pygraph")

if len(sys.argv) < 2:
    print("GRAPHFILE must be given. Check --usage")
    exit(1)

import pygraph.core as core
import pygraph.algorithms.transitivity as transitivity
dg = core.Digraph.from_file(sys.argv[1])
dg = transitivity.reduce(dg)

print(dg.to_dot())