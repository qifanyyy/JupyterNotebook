from __future__ import division
import networkx as nx
import util
from scipy import spatial
import math
import cv2
import numpy as np
import time

DISPLAY_IMG = False
SCALE_FACTOR = 300
PRUNING_RADIUS = math.sqrt(2)
MIN_NODES_DETECTED = 300
MIN_NODES_ACTUAL = 100

""" Creates a Dense Cluster Graph from the set of moving points, using a
    KD Tree to speed up the process """
def create_cluster_graph(f, point_map, moving_points, shape):
    G = nx.Graph()
    G.add_nodes_from(moving_points)

    start_time = time.time()
    # Add edges
    for pixel in moving_points:
        neighbours = util.get_neighbours(point_map, pixel, shape)
        for n in neighbours:
            dist = math.sqrt((n.x - pixel.x) ** 2 + (n.y - pixel.y) ** 2)
            if dist < pixel.lsw:
                G.add_edge(pixel, n, weight=dist)
    end_time = time.time()

    print("NUMBER OF NODES: %d" % G.number_of_nodes())
    print("NUMBER OF EDGES: %d" % G.number_of_edges())
    f.write("\nNumber of Nodes: %d\n" % G.number_of_nodes())
    f.write("Number of Edges: %d\n" % G.number_of_edges())
    f.write("Time to make cluster graph (s): %s\n\n" % (end_time - start_time))
    return G


""" MAIN CODE """

def extract_topology(f, moving_points, point_map, img, corners, artist, img_name):

    # encode some constants
    f.write("SCALE FACTOR: %d\n" % SCALE_FACTOR)
    f.write("PRUNING RADIUS: %.4f\n" % PRUNING_RADIUS)

    G = create_cluster_graph(f, point_map, moving_points, img.shape)

    """ Compute Minimum Spanning Tree """

    start_time = time.time()
    mst = nx.minimum_spanning_tree(G)
    end_time = time.time()
    print("NUMBER OF MST NODES: %d" % mst.number_of_nodes())
    print("NUMBER OF MST EDGES: %d" % mst.number_of_edges())
    f.write("NUMBER OF MST NODES: %d\n" % mst.number_of_nodes())
    f.write("NUMBER OF MST EDGES: %d\n" % mst.number_of_edges())
    f.write("Time to compute mst (s): %s\n\n" % (end_time - start_time))

    newImg = util.mapToImage(mst.nodes(), img.shape)
    util.thicken_line(newImg)
    util.display_img(newImg, "Post MST", DISPLAY_IMG)
    cv2.imwrite("topology/%s/%s/%s_CompleteGraph.jpg" % (artist, img_name, img_name), newImg)

    """ Iterative Pruning """

    f.write("--- ITERATIVE PRUNING ---\n")
    num_spc_pts = len(moving_points)
    prev_spc_pts = num_spc_pts # avoid infinite loops
    streak_len = 0
    counter = 0
    endpoints = []
    junctions = []
    itr_pruning_start = time.time()
    while num_spc_pts >= len(moving_points) // SCALE_FACTOR:

        counter += 1
        leaf_nodes = [x for x in mst.nodes_iter() if mst.degree(x) == 1]

        for leaf in leaf_nodes:
            total_weight = 0
            curr_node = leaf
            while total_weight < max(PRUNING_RADIUS, curr_node.lsw):
                n = mst.neighbors(curr_node)
                if len(n) != 1: break # used to be == 0
                e = mst.get_edge_data(curr_node, n[0])
                if total_weight + e['weight'] < max(PRUNING_RADIUS, curr_node.lsw):
                    total_weight += e['weight']
                    mst.remove_node(curr_node)
                    curr_node = n[0]
                else:
                    break

        print("NUM LEAF NODES: %d" % len(leaf_nodes))
        print("NUMBER OF PRUNED MST NODES: %d" % mst.number_of_nodes())
        print("NUMBER OF PRUNED MST EDGES: %d" % mst.number_of_edges())

        endpoints = [x for x in mst.nodes_iter() if mst.degree(x) == 1]
        junctions = [x for x in mst.nodes_iter() if mst.degree(x) >= 3]

        num_spc_pts = len(endpoints) + len(junctions)
        print("REP %d: %d points, %d special points" % (counter, len(moving_points), num_spc_pts))
        f.write("REP %d: %d points, %d special points\n" % (counter, len(moving_points), num_spc_pts))

        mstImg = util.mapToImage(mst.nodes(), img.shape)
        colorImg = mstImg.copy()
        colorImg = cv2.cvtColor(colorImg, cv2.COLOR_GRAY2BGR)

        for endpoint in endpoints:
            cv2.circle(colorImg, (util.R(endpoint.y), util.R(endpoint.x)), 3, (0, 0, 255), -1)

        for junction in junctions:
            cv2.circle(colorImg, (util.R(junction.y), util.R(junction.x)), 3, (255, 0, 0), -1)

        util.display_img(colorImg, "Post MST Pruning %d" % counter, DISPLAY_IMG)
        cv2.imwrite("topology/%s/%s/%s_Pruned_%d.jpg" % (artist, img_name, img_name, counter), colorImg)

        # AVOID INFINITE LOOPS
        if prev_spc_pts == num_spc_pts:
            if streak_len < 2:
                prev_spc_pts = num_spc_pts
                streak_len += 1
            else:
                break
        else:
            prev_spc_pts = num_spc_pts

    itr_pruning_end = time.time()
    print("\n--- FINAL POINTSET ---")
    print("%d points, %d special points\n" % (len(moving_points), (len(endpoints) + len(junctions))))
    f.write("\n--- FINAL POINTSET ---\n")
    f.write("%d points, %d special points\n" % (len(moving_points), (len(endpoints) + len(junctions))))
    f.write("Pruning time (in s): %s\n\n" % (itr_pruning_end - itr_pruning_start))

    mstImg = util.mapToImage(mst.nodes(), img.shape)
    colorImg = mstImg.copy()
    colorImg = cv2.cvtColor(colorImg, cv2.COLOR_GRAY2BGR)

    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(colorImg, (x, y), 3, (0, 255, 0), -1)

    cv2.imwrite("topology/%s/%s/%s_CORNERS_mst.jpg" % (artist, img_name, img_name), colorImg)

    f.write("NUMBER OF Connected Components: %d\n" % nx.number_connected_components(mst))

    loner_nodes = [x for x in mst.nodes_iter() if mst.degree(x) == 0]
    mst.remove_nodes_from(loner_nodes)
    mst.remove_nodes_from(endpoints)
    mst.remove_nodes_from(junctions)

    junction_endpoints = endpoints + junctions
    all_pairs = np.transpose([np.tile(junction_endpoints, len(junction_endpoints)), np.repeat(junction_endpoints, len(junction_endpoints))])
    print("Number of pairs: %d" % len(all_pairs))
    f.write("Number of endpoint-junction pairs: %d\n" % len(all_pairs))

    print("NUMBER OF CC's: %d" % nx.number_connected_components(mst))
    f.write("NEW NUMBER OF Connected Components: %d\n" % nx.number_connected_components(mst))
    components_subgraphs = nx.connected_component_subgraphs(mst)
    point_pairs = []
    counter = 0
    cc_start_time = time.time()
    for comp in components_subgraphs:
        counter += 1
        endpoints = [x for x in comp.nodes_iter() if comp.degree(x) == 1]
        if len(endpoints) != 2: continue

        min_dist = 1000
        pair = []
        for p0, p1 in all_pairs:
            dist1 = util.pointDist(p0, endpoints[0]) + util.pointDist(p1, endpoints[1])
            dist2 = util.pointDist(p0, endpoints[1]) + util.pointDist(p1, endpoints[0])
            if dist1 < min_dist:
                min_dist = dist1
                pair = (p0, p1)
            if dist2 < min_dist:
                min_dist = dist2
                pair = (p1, p0)
        point_pairs.append(pair)

        testImg = img.copy()
        testImg = cv2.cvtColor(testImg, cv2.COLOR_GRAY2BGR)
        for node in comp.nodes_iter():
            cv2.circle(testImg, (util.R(node.y), util.R(node.x)), 3, (0, 255, 0), -1)
        cv2.circle(testImg, (util.R(pair[0].y), util.R(pair[0].x)), 3, (0, 0, 255), -1)
        cv2.circle(testImg, (util.R(pair[1].y), util.R(pair[1].x)), 3, (0, 0, 255), -1)
        util.display_img(testImg, "Test", False)
        if len(comp.nodes()) > MIN_NODES_DETECTED:
            cv2.imwrite("topology/%s/%s/%s_DetectedCurve_%d.jpg" % (artist, img_name, img_name, counter), testImg)

    cc_end_time = time.time()
    print("NUMBER OF POINT PAIRS: %d\n" % len(point_pairs))
    f.write("NUMBER OF POINT PAIRS: %d\n" % len(point_pairs))
    f.write("Time to Find Point Pairs (in s): %s\n\n" % (cc_end_time - cc_start_time))
    util.save_buddy_points("%s.txt" % img_name, artist, "buddyPoints", point_pairs)

    f.write(" --- Calculating Paths --- \n")

    curves = []
    counter = 0
    curve_start = time.time()
    for pair in point_pairs:
        counter += 1
        path = nx.dijkstra_path(G, pair[0], pair[1])

        curves.append(path)
        print("Length of path: %d" % len(path))
        f.write("Length of path: %d\n" % len(path))

        testImg = img.copy()
        testImg = cv2.cvtColor(testImg, cv2.COLOR_GRAY2BGR)
        for node in path:
            cv2.circle(testImg, (util.R(node.y), util.R(node.x)), 3, (0, 0, 255), -1)
        util.display_img(testImg, "Test", False)
        if len(path) > MIN_NODES_ACTUAL:
            cv2.imwrite("topology/%s/%s/%s_ActualCurve_%d.jpg" % (artist, img_name, img_name, counter), testImg)

    curve_end = time.time()
    util.save_curves("%s.txt" % img_name, artist, "curves", curves)
    f.write("\nTime to Seperate Curves (in s): %s\n\n" % (curve_end - curve_start))


""" Run the script independantly """

if __name__ == "__main__":

    artists = ['foster', 'levesque', 'koudelka', 'vidal', 'fiala', 'fiala', 'levesque', 'vidal', 'fiala', 'foster']
    images = ['test1', 'levesque2', 'koudelka5', 'vidal2', 'fiala_001', 'fiala_010', 'levesque1', 'vidal6', 'fiala_014', 'test2']

    for i in xrange(len(images)):
        artist = artists[i]
        img_name = images[i]
        orig_name = img_name

        # Load a color image in grayscale
        img = cv2.imread("samples/%s/%s.jpg" % (artist, img_name), 0)
        util.display_img(img, "Initial Image", DISPLAY_IMG)

        corners = cv2.goodFeaturesToTrack(img, 100, 0.01, 10)
        corners = np.int0(corners)

        tmp = img.copy()
        tmp = cv2.cvtColor(tmp, cv2.COLOR_GRAY2BGR)
        for corner in corners:
            x, y = corner.ravel()
            cv2.circle(tmp, (x, y), 3, (0, 255, 0), -1)

        moving_points, point_map = util.load_point_map("%s.txt" % img_name, artist, "pointSet", img.shape)

        img_name = img_name + "_PR_NBHD"

        cv2.imwrite("topology/%s/%s/%s_CORNERS_orig.jpg" % (artist, img_name, img_name), tmp)

        print("Extracting Topology for %s, %s" % (artist, img_name))
        util.DW("curves/%s" % artist) # I think you only need this in a next step...
        util.DW("topology/%s/%s" % (artist, img_name))
        util.DW("stats/%s" % artist)
        util.DW("buddyPoints/%s" % artist)

        f = open("%s/%s/%s_topology.txt" % ("stats", artist, img_name), 'w')
        extract_topology(f, moving_points, point_map, img.shape, corners)
        f.close()

        cv2.destroyAllWindows()


