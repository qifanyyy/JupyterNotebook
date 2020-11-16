"""Python adjacency list implementation."""


def adl(file_name, is_weight=False, default_weight=0, bonus_key=""):
    """The function returns adjacency list representation of a graph.
    bonus_key if set, will be added to all nested dictionaries.
    Input data format:
    With weights:
        1 2,4 3,111
        2 4,55 5,7
    Output:
        {1: {2: 4, 3: 111}, 2: {4: 55, 5: 7}}

    Without weights:
        1 2 3
        2 4 5
    Output:
        {1: {2: None, 3: None}, 2: {4: None, 5: None}}

    It can handle files where edges are in separate lines each:
        1 2
        1 3
        2 4
        2 5
    """
    adj_list = {}
    with open(file_name, 'r') as f:
        for line in f.readlines():
            if not line.strip():
                continue

            line = line.strip().split()
            u = line[0]
            if u not in adj_list:
                adj_list[u] = {bonus_key: default_weight} if bonus_key else {}

            for k in line[1:]:
                if is_weight:
                    x, y = k.split(',')
                else:
                    x = k.split(',')[0]
                    y = default_weight
                adj_list[u][x] = int(y)

    return adj_list
