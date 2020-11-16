"""Python implementation of clustering based on union find structure."""

from disjoint_set import DisjointSet


def k_clusters(items, k):
    """Groups items in k clusters. An item should be a collection of
    2 points or points with distance between them.

    :param items: sorted collection of (node1, node2, distance) objects.
    :param k: int, number of clusters we want to have returned.
    :return: {cluster1: [node1, node2], cluster2: [node3] ...}
    """
    union_find = DisjointSet()

    # Initial setting of all points, where each node belongs to its own cluster.
    for item in items:
        union_find.make_set(item[0])
        union_find.make_set(item[1])

    # After every union operation the clusters counter is decreased by 1.
    counter = len(union_find)
    for item in items:
        node1, node2 = item[:2]
        if union_find.is_connected(node1, node2):
            continue

        if counter == k:
            return union_find.get_clusters()

        union_find.union(node1, node2)
        counter -= 1


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from itertools import combinations

    np.random.seed(5)

    # Generate some points
    xs = np.random.random_integers(1, 100, 40)
    ys = np.random.random_integers(1, 100, 40)
    points = {idx: coords for idx, coords in enumerate(zip(xs, ys))}

    # Create edges with distances. Input for k_clusters function.
    edges = []
    for edge in combinations(points, 2):
        x1, y1 = points[edge[0]]
        x2, y2 = points[edge[1]]
        dist = (abs(x1 - x2) + abs(y1 - y2)) ** 0.5
        edges.append((edge[0], edge[1], dist))

    edges.sort(key=lambda x: x[2])

    # Clustering
    clusters = k_clusters(edges, 7)

    # Plot points. Clusters distinguished by colors.
    colors = 'rgbcmyk'
    for idx, cluster in enumerate(clusters):
        coords = [points[node] for node in clusters[cluster]]
        x_coords, y_coords = zip(*coords)
        plt.scatter(x_coords, y_coords, c=colors[idx])

    plt.show()
