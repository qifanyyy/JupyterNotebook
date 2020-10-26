import networkx as nx
import uuid
import hashlib

import taskflow.symbolic as sym


def build_graph(symbolic_func, call=None, callDest=None, graph=None):

    if graph is None:
        graph = nx.DiGraph()
        graph.add_node("START")

    if call is None:
        call = "STOP"
        graph.add_node(call)
        callDest = 'end_%s' % str(uuid.uuid1())

    if not isinstance(symbolic_func, sym.Symbolic):
        return graph

    id = symbolic_func.__identifier__()

    if isinstance(symbolic_func, sym.SymbolicForkElement):
        args = {}
        dependencies = {"__fork__": symbolic_func.list_}
    elif isinstance(symbolic_func, sym.SymbolicMergeElement):
        args = {'flatten': symbolic_func.flatten_}
        dependencies = symbolic_func.args_
    else:
        optional = False
        if isinstance(symbolic_func, sym.optional):
            symbolic_func = symbolic_func.get_content()
            optional = True

        args = {
            'env': symbolic_func.env_args_,
            'function': symbolic_func.function_,
            'dependency_vars': list(symbolic_func.task_args_.keys()),
            'version': symbolic_func.version_,
            'attributes': symbolic_func.attr_
        }

        if optional:
            args['optional'] = True

        dependencies = symbolic_func.task_args_

    if not graph.has_node(id):
        graph.add_node(id, **args)

        if len(dependencies) == 0:
            graph.add_edge("START", id)
        else:
            for k, symbolic_dep in dependencies.items():
                build_graph(symbolic_dep, call=id,
                            callDest=k, graph=graph)

    if not graph.has_edge(id, call):
        graph.add_edge(id, call, dest=[])
    graph.edges[id, call]['dest'].append(callDest)

    return graph


def to_dot(graph):
    print("digraph D {")
    index = {}
    counter = 0

    for n in graph:
        index[n] = "N"+str(counter)
        counter += 1

        print(index[n]+"[label=\"%s\"];" % n)

    for n1, n2 in graph.edges():
        print(index[n1]+" -> "+index[n2]+";")

    print("}")
