def validate_no_incident_edge_for_color(coloring):
    for color in coloring:
        for edge in coloring[color]:
            for another_edge in coloring[color]:
                if (another_edge[0] == edge[0] and another_edge[1] == edge[1]) or (another_edge[0] == edge[1] and another_edge[1] == edge[0]):
                    continue
                if another_edge[0] == edge[0] and another_edge[1] != edge[1]:
                    print("shit happened with " + str(edge) + " " + str(another_edge) + " color " + str(color))
                    raise


def validate_no_uncolored_edges(graph, coloring):
    holder_incident = []
    coloring_total = []
    for node in graph.incident:
        for node2 in graph.incident[node]:
            holder_incident.append((node, node2))

    for color in coloring:
        coloring_total = coloring[color] + coloring_total

    print("TEST: LEN OF INCIDENT " + str(len(holder_incident)))
    print("TEST: LEN OF COLORING " + str(len(coloring_total)))
    if len(holder_incident) != len(coloring_total):
        print("TEST: MAX DEGREE " + str(graph.max_degree('degree')))
        print("TEST: MAX DEGREE VERTEX " + str(graph.max_degree()))
        print("TEST: INCIDENT " + str(graph.incident))
        print("TEST: COLORING " + str(coloring))
        print("TEST: IN COLORING " + str(coloring_total))
        print("TEST: IN INCIDENT " + str(holder_incident))
        print("TEST: DIFFERENCE: " + str(set(holder_incident) - set(coloring_total)))
        print("TEST: DIFFERENCE: " + str(set(coloring_total) - set(holder_incident)))
        raise