import os

from PIL import Image
from helpers import cropBorder, replace_print

class Maze(object):

    # Start of Node Class #

    class Node(object):

        def __init__(self, x_pos, y_pos, surroundings=None, start=False, end=False):

            self.name = 'node_%s_%s' % (x_pos, y_pos)
            self.x_pos, self.y_pos = (x_pos, y_pos)
            self.surroundings = surroundings
            self.start = start
            self.end = end
            self._adjacent_nodes = {}
            self._prev_node = None

        @property
        def adjacent_nodes(self):
            """Adjacent Node Property"""
            return self._adjacent_nodes

        def set_adjacent_nodes(self, key, value):
            """Sets adjacent node"""
            self._adjacent_nodes[key] = value

        @property
        def prev_node(self):
            """Previous Node Property"""
            return self._prev_node

        def set_prev_node(self, value):
            """Set Previous node"""
            self._prev_node = value

        @property
        def prettify(self):
            return 'Node at ({}, {})'.format(self.x_pos, self.y_pos)

    # End of Node Class #

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    start_node = None
    end_node = None

    def __init__(self, filename, to_crop=False):

        print '---------------'
        print 'Processing Maze'
        print '---------------\n'

        self.maze = cropBorder(Image.open(filename)) if to_crop else Image.open(filename)
        self.height, self.width = self.maze.size
        self.node_dict = self.find_nodes()
        self.make_graph()

        print '---------------'
        print 'Solving Maze'
        print '---------------\n'

    def get_surroundings(self, x_pos, y_pos):
        """Gets the values of up,down,left,right at given coords."""

        # The x,y coordinates of a given pixel's surorundings at x_pos and y_pos
        up = (x_pos, y_pos - 1) if y_pos - 1 >= 0 else False
        down = (x_pos, y_pos + 1) if y_pos + 1 < self.height else False
        left = (x_pos - 1, y_pos) if x_pos - 1 >= 0 else False
        right = (x_pos + 1, y_pos) if x_pos + 1 < self.width else False

        surroundings = {
            'up': up,
            'down': down,
            'left': left,
            'right': right
        }

        for direction in surroundings:

            if surroundings[direction]:
                pix = self.maze.getpixel(surroundings[direction])

                if not self.check_black(pix):
                    surroundings[direction] = True
                else:
                    surroundings[direction] = False

        return surroundings

    def move_horizontally(self, y):
        """Moves horizontally along y until it finds a white square, return the x,y positions"""
        x_y_pairs = []

        for x in xrange(self.width):

            pix = self.maze.getpixel((x,y))

            if self.check_white(pix):

                x_y_pairs.append((x, y))

        return x_y_pairs

    def move_vertically(self, x):
        """Moves vertically along x until it finds a white square, return the x,y positions"""

        x_y_pairs = []

        for y in xrange(self.height - 1):

            pix = self.maze.getpixel((x,y))

            if self.check_white(pix):

                x_y_pairs.append((x, y))

        return x_y_pairs

    def make_start_end_node(self):
        """Takes the x and y coords of the start node and makes it the start node"""

        is_start = True
        is_end = False

        node_dict = {}

        # Get x, y coords of start and end nodes
        x_y_pairs = self.move_horizontally(0)
        x_y_pairs += self.move_horizontally(self.height-1)
        x_y_pairs += self.move_vertically(0)
        x_y_pairs += self.move_vertically(self.width - 1)

        for x_y in x_y_pairs:

            x, y = x_y[0], x_y[1]

            node_name = 'node_%s_%s' % (x,y)

            node_dict[node_name] = self.Node(x, y, surroundings=self.get_surroundings(x, y), start=is_start, end=is_end)

            if is_start:
                self.start_node = node_name
                print 'Found Start Node: {}'.format(node_dict[node_name].prettify)

            if is_end:
                self.end_node = node_name
                print 'Found End Node: {}'.format(node_dict[node_name].prettify), '\n'

            is_start = False
            is_end = True

        return node_dict

    def find_nodes(self):
        """Finds and returns nodes in a maze"""

        print 'Finding nodes...'
        maze_copy = self.maze.copy()
        node_dict = self.make_start_end_node()

        for key, node in node_dict.items():
            maze_copy.putpixel((node.x_pos, node.y_pos), self.RED)

        found_nodes = 2
        number_of_nodes = 2

        # Get the rest of the nodes
        for y in xrange(1, self.height - 1):
            for x in xrange(1, self.width):

                pix = self.maze.getpixel((x,y))

                if self.check_white(pix):

                    isNode = True
                    directions = self.get_surroundings(x,y)

                    up_and_down = directions['up'] and directions['down']
                    up_or_down = directions['up'] or directions['down']

                    left_and_right = directions['left'] and directions['right']
                    left_or_right = directions['left'] or directions['right']

                    # Rules for a node (a node is where you can / must change direction while following a path)
                    if up_and_down and not left_or_right:
                        isNode = False

                    elif left_and_right and not up_or_down:
                        isNode = False

                    # Color maze, assign nodes
                    if isNode:

                        node_dict['node_%s_%s' % (x,y)] = self.Node(x, y, surroundings=self.get_surroundings(x,y))

                        found_nodes += 1
                        replace_print('Number of nodes found: {}'.format(found_nodes))

                        maze_copy.putpixel((x, y), self.RED)

        print '\n'
        filename =  self.maze.filename.replace('cropped', 'nodes')
        maze_copy.save(filename)

        return node_dict

    def make_graph(self):
        """Connect the nodes"""

        connected_nodes = 0.0
        total_nodes = len(self.node_dict.keys())
        direction_sums = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0)
        }

        # Loop through the nodes
        for key, node in self.node_dict.items():

            connected_nodes += 1
            string = '{} nodes connected out of {} ({:.2f} %)'.format(
                                                    connected_nodes,
                                                    total_nodes,
                                                    connected_nodes / total_nodes * 100)

            # Pull a given node from the dictionary, get some of its attributes
            surroundings = node.surroundings
            x_pos = node.x_pos
            y_pos = node.y_pos

            # Loop through its surroundings, find nodes
            for direction in surroundings:

                path = surroundings[direction]

                if path:

                    # Get the adjacent node and its position in tuple form from check_nodes_in_dir, split them up
                    node_and_pos = self.check_nodes_in_dir(x_pos, y_pos, direction_sums[direction])

                    adj_node = node_and_pos[0]
                    distance = abs((x_pos - node_and_pos[1][0]) + (y_pos - node_and_pos[1][1]))

                    # Set adjacent node in that direction with the distance
                    node.set_adjacent_nodes(direction, (adj_node, distance))

                else:

                    node.set_adjacent_nodes(direction, None)

            replace_print('Number of connected nodes: {0:.0f} ({1:.2f} %)'.format(connected_nodes, connected_nodes / total_nodes * 100))

        print '\n'

    def check_nodes_in_dir(self, x_pos, y_pos, direc_sum):
        """
           Checks for nodes in the direction directed by direc_sum.
           Very specified just for the `make_graph()` method.
        """

        # `direc_sum` is `direction_sums` tuple defined above
        x_pos += direc_sum[0]
        y_pos += direc_sum[1]
        node = self.get_node_by_pos(x_pos, y_pos)

        while not node:
            x_pos += direc_sum[0]
            y_pos += direc_sum[1]
            node = self.get_node_by_pos(x_pos, y_pos)

        return node, (x_pos, y_pos)

    def get_pixel(self, x_pos, y_pos):
        """Return pixel RGB Value"""

        return self.maze.getpixel((x_pos, y_pos), 'RGB')

    def get_node_by_pos(self, x_pos, y_pos):
        """Gets node from the x and y position"""

        node_name = 'node_%s_%s' % (x_pos, y_pos)

        return self.node_dict.get(node_name)

    def color_pixel(self, x, y, color, filename=None):

        filename = filename if filename else self.maze.filename

        self.maze.putpixel((x, y), color)
        self.maze.save(filename)

    def check_white(self, rgb_tuple):
        """Checks if rgb_tuple is white"""
        return True if rgb_tuple == (255,255,255) or rgb_tuple == (255,255,255,255) else False

    def check_black(self, rgb_tuple):
        """Checks if rgb_tuple is black"""
        return True if rgb_tuple == (0,0,0) or rgb_tuple == (0,0,0,255) else False
