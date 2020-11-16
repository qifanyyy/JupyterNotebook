import sys
sys.path.append("../pygraph")

if len(sys.argv) < 2:
    print("GRAPHFILE must be given. Check --usage")
    exit(1)

import pygraph.core as core
import pygraph.algorithms.transitivity as transitivity
import pygraph.algorithms.topsort as topsort

dg = core.Digraph.from_file(sys.argv[1])
dg = transitivity.reduce(dg)

order = topsort.topsort(dg)
for node in order:
    print(str(node))
