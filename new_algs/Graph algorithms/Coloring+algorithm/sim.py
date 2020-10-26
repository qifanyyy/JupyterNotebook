from edge_coloring.algorithms import EdgeColoring, InspectorEngine
from edge_coloring.storage import SQLiteGraphStore

store = SQLiteGraphStore('graphs.db')
graph = store.get_graph(2)


n = 100000

inspector = InspectorEngine(graph)
pentagon = inspector.find_pentagon()
# pentagon must be found to continue
for i in xrange(n):
    inspector.remove_edge(pentagon)
    graph.random_color()
    coloring = EdgeColoring(graph)
    coloring.run()
    if inspector.check_cycles():
        break
    print i
inspector.contract()
