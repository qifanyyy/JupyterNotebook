import os, time, timeit, argparse

from PIL import ImageDraw

from processMaze import Maze
from binaryHeap import BinaryHeap
from helpers import replace_print

class mazeSolve(object):
    """Takes in a maze, makes a graph, and solves it"""

    def __init__(self, filename, to_crop=False):

        self.maze = Maze(filename, to_crop=to_crop)
        self.nodes = self.maze.node_dict
        self.priority_que = BinaryHeap([list(a) for a in zip(self.nodes.keys(), [float('inf')] * len(self.nodes))])
        # Want to use zip function, but need each item to be mutable. therefore, the `list(a) for a in zip...` notation
        self.visited_nodes = set()
        self.path = []

    def solve(self):
        """Connects the nodes from the starting node to the ending node"""

        # Find the starting node of the maze, add it to self.visited_nodes, and assign the node a distance from the start of 0
        start = self.maze.start_node

        self.add_value(start, 0)
        self.heapify()

        end_node = self.process([start, 0])

        self.make_path(end_node[0])

        self.draw_path()

    def process(self, curr_node):
        """Process the maze by running through the binary heap, until the end node is found"""

        current_node = self.nodes[curr_node[0]]
        current_node_distance = curr_node[1]

        connected_nodes = 0.0
        total_nodes = len(self.nodes)


        while current_node.end == False:

            connected_nodes += 1
            percent = connected_nodes / total_nodes * 100

            replace_print('Investigating {0:18} Number {1} of {2} nodes ({3:3.2f} %)'.format(current_node.prettify, int(connected_nodes), total_nodes, percent))

            # Add min node to visited_nodes and remove it from the priority_que
            self.visited_nodes.add(current_node.name)
            self.priority_que.delete_min()

            # Find the adjacent nodes of curr_node
            adjacent_nodes = current_node.adjacent_nodes

            for direction, node_distance in adjacent_nodes.items():

                if node_distance and not (node_distance[0].name in self.visited_nodes):

                    self.add_value(node_distance[0].name, node_distance[1] + current_node_distance)
                    node_distance[0].set_prev_node(current_node)

            self.heapify()

            current_node = self.nodes[self.priority_que.heap[0][0]]
            current_node_distance = self.priority_que.heap[0][1]

        end_node = self.priority_que.delete_min()
        end_node[0] = self.nodes[end_node[0]]

        # Final increment and print of "Investigating Node..."
        connected_nodes += 1
        percent = connected_nodes / total_nodes * 100
        replace_print('Investigating {0:18} Number {1} of {2} nodes ({3:3.2f} %)'.format(current_node.prettify, int(connected_nodes), total_nodes, percent))

        print('\nEnd node has been found: {}'.format(end_node[0].prettify))
        print '\n'
        print 'The path length from start to end node is {} pixels long'.format(end_node[1])

        return end_node

    def make_path(self, curr_node):
        """Returns the path from the start node to the end node"""

        self.path = [curr_node] + self.path

        while curr_node.prev_node:

            self.path = [curr_node.prev_node] + self.path
            curr_node = curr_node.prev_node

        if len(self.path) < 100:
            self.print_path()

    def print_path(self):
        """Prints the path of the nodes"""

        print '\nHere is the path for the maze:',

        for node in self.path:

            print node.name, '-->',

    def draw_path(self):
        """Creates a new maze image with the solution on it"""

        if not self.path:
            raise IndexError('`self.path` MUST BE POPULATED')

        maze_copy = self.maze.maze.copy()
        draw = ImageDraw.Draw(maze_copy)

        for i in xrange(len(self.path)-1):

            node = self.path[i]
            next_node = self.path[i + 1]
            line_coords = [(node.x_pos, node.y_pos), (next_node.x_pos, next_node.y_pos)]
            draw.line(line_coords, fill=(66, 134, 244))

        filename = self.maze.maze.filename.replace('cropped', 'solution')
        maze_copy.save(filename)

    def add_value(self, node, value):
        """Finds `node` in priority_que and assigns `value` to it's second value. If the node hasn't been discovered yet, assign it's distance `value`. Else add value to it's distance"""
        found = False

        for node_dist in self.priority_que.heap:

            if node == node_dist[0]:
                node_dist[1] = value if node_dist[1] == float('inf') else (node_dist[1] + value)
                found = True
                break

        if not found:
            raise ValueError('Node not in priority que')

    def heapify(self):
        """Shortcut method"""
        self.priority_que.heapify()

def parser():
    parser = argparse.ArgumentParser(description="Maze solving program, employing dijkstra's path finding algorithm.")
    parser.add_argument("-f", "--filename", help='The filename of the maze. If left blank, an example is provided.')
    parser.add_argument("-c", "--to_crop", help='The directory of the maze. If left black, the maze is assumed to be in /mazes', default=True)

    return parser.parse_args()

if __name__ == '__main__':

    args = parser()

    filename = args.filename if args.filename else 'smallmaze.png'
    to_crop = args.to_crop

    os.chdir('..')
    os.chdir(os.getcwd() + '/mazes')

    #-----------------------------------------------#

    print '\n', '*'*10, 'Maze Solver', '*'*10, '\n'

    t1 = time.time()

    dijkstra = mazeSolve(filename, to_crop=to_crop)
    dijkstra.solve()

    t2 = time.time()

    print 'Success! The solved maze has the name `{}`'.format(dijkstra.maze.maze.filename).replace('cropped', 'solution')
    print 'The maze took {:.3f} seconds to process and solve!\n'.format(t2 - t1)
