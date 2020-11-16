#! python3

"""ROAD ROUTER
Data and input/output utility functions (called from main.py)."""

import csv
import matplotlib.cm as cm
import matplotlib.collections as coll
import matplotlib.pyplot as plt
import os

# Full size electricty substation and road dataset from QGIS
# SERVER_NODE_INFILE = os.path.join(
#    'Input Data', 'Electricity Substation-nodes.csv')
# ROAD_NODE_INFILE = os.path.join(
#    'Input Data', 'Road Node-nodes.csv')
# ROAD_SEGMENT_POINT_INFILE = os.path.join(
#    'Input Data', 'Road-nodes.csv')

# Reduced size electricty substation and road dataset from QGIS
SERVER_NODE_INFILE = os.path.join(
    'Input Data', 'Electricity Substation-nodes-sample.csv')
ROAD_NODE_INFILE = os.path.join(
    'Input Data', 'Road Node-nodes-sample.csv')
ROAD_SEGMENT_POINT_INFILE = os.path.join(
    'Input Data', 'Road-nodes-sample.csv')

# Output dataset for re-import into QGIS
ROAD_NODE_OUTFILE = os.path.join(
    'Output Data', 'Road Node-nodes-routed.csv')
ROAD_SEGMENT_POINT_OUTFILE = os.path.join(
    'Output Data', 'Road-nodes-routed.csv')

# Map plot features
COLORMAP = 'nipy_spectral'
CM_OFFSET = 0   # for rotating plot colours if needed
NUM_COLORS = 25  # note colours will repeat if more servers than colours
GREY = 25
SERVER_SYM_SIZE = 48
ROAD_NODE_SIZE = 0  # 0 means invisible
ROAD_WIDTH = 1


def load_data():
    """Load all CSV files."""

    server_node = load_nodes(SERVER_NODE_INFILE)
    road_node = load_nodes(ROAD_NODE_INFILE)
    road_segment_point = load_nodes(ROAD_SEGMENT_POINT_INFILE)

    return server_node, road_node, road_segment_point


def load_nodes(filename):
    """Load CSV data from QGIS into list of dictionaries
       Expected data format from:
       QGIS v3.0.3 --> MMQGIS v2018.2.27 (plugin) --> Import / Export
                   --> Geometry Export to CSV file
                   --> Options: Line Terminator:LF."""

    with open(filename) as f:
        reader = csv.DictReader(f)
        return [item for item in reader]


def plot_nodes(snode, rnode, rseg):
    """Plot colour-coded results on map."""

    # Prepare plot
    _, ax = plt.subplots()
    plt.title('Best servers by minimal road distance')

    # Plot road segments
    line = [[(item['x1'], item['y1']), (item['x2'], item['y2'])]
            for item in rseg]
    c = [cm.get_cmap(COLORMAP)(item['color_num'] / (NUM_COLORS - 1))
         for item in rseg]
    lc = coll.LineCollection(line, colors=c, linewidth=ROAD_WIDTH)
    ax.add_collection(lc)

    # Plot road nodes
    x = [item['x'] for item in rnode]
    y = [item['y'] for item in rnode]
    c = [item['color_num'] for item in rnode]
    ax.scatter(x, y, c=c, cmap=COLORMAP, edgecolors='face',
               vmin=0, vmax=(NUM_COLORS - 1), s=ROAD_NODE_SIZE)

    # Plot server nodes
    x = [item['x'] for item in snode]
    y = [item['y'] for item in snode]
    c = [item['color_num'] for item in snode]
    ax.scatter(x, y, c=c, cmap=COLORMAP, edgecolors='face',
               vmin=0, vmax=(NUM_COLORS - 1), s=SERVER_SYM_SIZE)

    # Display plot and save
    plt.savefig(os.path.join('Output Data', 'Best server.pdf'))
    plt.show()


def prep_export(road_node, road_segment_point,
                snode, rnode, rpoint):
    """Append results fields to master input data for export."""

    # Expand results to all records in original road node data
    rnode_xy = [(jtem['x'], jtem['y']) for jtem in rnode]
    for i in range(len(road_node)):
        road_node_xy = (
            float(road_node[i]['x']), float(road_node[i]['y']))
        if road_node_xy in rnode_xy:
            pos = rnode_xy.index(road_node_xy)
            road_node[i]['best_server'] = rnode[pos]['best_server']
        else:
            road_node[i]['best_server'] = None

    # Append results to orginal road segment data
    for i in range(len(road_segment_point)):
        if rpoint[i]['best_server'] is not None:
            road_segment_point[i]['best_server'] = snode[
                rpoint[i]['best_server']]['shapeid']
        else:
            road_segment_point[i]['best_server'] = None

    return road_node, road_segment_point


def save_data(road_node, road_segment_point):
    """Save all CSV files."""

    save_nodes(road_node, ROAD_NODE_OUTFILE)
    save_nodes(road_segment_point, ROAD_SEGMENT_POINT_OUTFILE)


def save_nodes(node, filename):
    """Save CSV data for re-import into QGIS
       Compatible data format for:
       QGIS v3.0.3 --> MMQGIS v2018.2.27 (plugin) --> Import / Export
                   --> Geometry Import from CSV file
                   --> Options: defaults."""

    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f,
                                fieldnames=node[0].keys(),
                                quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(node)


def setup_nodes(server_node, road_node, road_segment_point):
    """Setup data for router functions."""

    # Create working server node data subset excluding unneeded fields
    snode = [{'id': i,
              'shapeid': item['shapeid'],
              'x': float(item['x']),
              'y': float(item['y']),
              'nearest_pt': None,
              'nearest_pt_sl_dist': float("inf"),
              'color_num': (int(item['shapeid']) + CM_OFFSET) % NUM_COLORS}
             for i, item in enumerate(server_node)]

    # Create working road node data subset excluding unneeded fields
    # (note: road nodes consist of junctions and road ends)
    rnode = []
    prev_coord = []
    for i, item in enumerate(road_node):
        if [item['x'], item['y']] not in prev_coord:  # exclude duplicates
            rnode.append({'id': i,
                          'shapeid': item['shapeid'],
                          'x': float(item['x']),
                          'y': float(item['y']),
                          'best_server': None,
                          'color_num': GREY})
            prev_coord.append([item['x'], item['y']])

    # Create working road point data subset excluding unneeded fields
    rpoint = []
    point = 0
    for i in range(len(road_segment_point)):
        id = road_segment_point[i]['shapeid']
        rpoint.append({'id': i,
                       'shapeid': id,
                       'point': point,
                       'x': float(road_segment_point[i]['x']),
                       'y': float(road_segment_point[i]['y']),
                       'lowest_cost': float("inf"),
                       'best_server': None,
                       'color_num': GREY})
        if i < len(road_segment_point) - 1:
            id_next = road_segment_point[i + 1]['shapeid']
            if id == id_next:
                point += 1
            else:
                point = 0

    # Convert adjacent road segment endpoints to lines (x1, y1) to (x2, y2)
    rseg = []
    line = 0
    seg = 0
    for i in range(len(rpoint[:-1])):
        id = rpoint[i]['shapeid']
        id_next = rpoint[i + 1]['shapeid']
        if id == id_next:
            rseg.append({'id': line,
                         'shapeid': id,
                         'segment': seg,
                         'point1': rpoint[i]['id'],
                         'x1': float(rpoint[i]['x']),
                         'y1': float(rpoint[i]['y']),
                         'point2': rpoint[i + 1]['id'],
                         'x2': float(rpoint[i + 1]['x']),
                         'y2': float(rpoint[i + 1]['y']),
                         'best_server': None,
                         'color_num': GREY})
            line += 1
            seg += 1
        else:
            seg = 0

    return snode, rnode, rpoint, rseg
