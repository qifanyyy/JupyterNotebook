import random
import pprint


class Node:
    """Put into a numberline of sorts, where each Node instance
    has the coordinates of where it should be on a 2D grid."""

    def __init__(self, pos: int, grid_length: int):
        self.position = pos
        self.grid_length = grid_length
        self.is_wall = True
        self.pneighbors = []
        self.neighbors = []
        # All start as walls:
        self.get_possible_neighbors()
        self.path_to_me = []

    def get_possible_neighbors(self):
        up_neighbor = self.position - self.grid_length
        down_neighbor = self.position + self.grid_length
        right_neighbor = self.position + 1
        left_neighbor = self.position - 1
        pneighbors = []
        if up_neighbor >= 0:
            pneighbors.append(up_neighbor)
        if down_neighbor < self.grid_length ** 2:
            pneighbors.append(down_neighbor)
        if right_neighbor // self.grid_length == self.position // self.grid_length:
            pneighbors.append(right_neighbor)
        if left_neighbor // self.grid_length == self.position // self.grid_length:
            pneighbors.append(left_neighbor)

        self.pneighbors = pneighbors


class WallSmasher:
    """Implementation of Prim's algorithm that deletes the walls
    it encouters during generation."""

    def __init__(self, size, start):
        self.size = size
        self.nodes = [Node(i, size) for i in range(size ** 2)]
        self.grid_length = size
        self.startingNode = self.nodes[start]
        self.endingNode = None
        self.path_to_goal = []

    def create_neighbors(self, node1: Node, node2: Node):
        self.nodes[node1].neighbors.append(node2)
        self.nodes[node2].neighbors.append(node1)

    def check_adjacent(self, neighbor: Node, visited: list, cells: list) -> int:
        """Check for adjacent, unvisited nodes."""
        count = 0
        if neighbor in visited:
            return 0
        for nn in neighbor.pneighbors:
            if nn not in visited and nn not in cells:
                count += 1
        return count

    def smash(self) -> None:
        walls = [item for item in self.startingNode.pneighbors]
        cells = [self.startingNode.position]
        visited = [self.startingNode.position]
        self.create_neighbors(self.startingNode.position, walls[0])
        self.create_neighbors(self.startingNode.position, walls[1])
        while len(walls):
            current_wall = random.choice(walls)
            visited.append(current_wall)

            pneighbors = self.nodes[current_wall].pneighbors

            done = False
            count = 0
            for p in pneighbors:

                if p in cells:
                    count += 1
            if count > 1:
                done = True

            if not done:
                neighbors = []
                for item in pneighbors:
                    if self.check_adjacent(self.nodes[item], visited, cells) > 1:
                        neighbors.append(item)

                neighbors = [n for n in neighbors if n not in visited]

                if len(neighbors):
                    neighbor = random.choice(neighbors)
                    neighbors.remove(neighbor)
                else:
                    neighbor = None

                cells.append(current_wall)
                for neighbor in pneighbors:
                    if neighbor not in visited and neighbor not in cells:
                        if self.nodes[current_wall].path_to_me is not None:
                            path = self.nodes[
                                current_wall].path_to_me.copy()
                            path.append(current_wall)
                            self.nodes[neighbor].path_to_me = path
                        else:
                            self.nodes[neighbor].path_to_me = [
                                current_wall]
                        walls.append(neighbor)

            walls.remove(current_wall)
            for item in cells:
                self.nodes[item].is_wall = False

        for item in cells:
            self.nodes[item].is_wall = False

        self.set_straigth_path()

    def get_array(self) -> list:
        """Converts the list into a grid-like form."""
        # Main conversion of nodes to int's
        array = [[int(self.nodes[row * self.size + col].is_wall)
                  for col in range(self.size)] for row in range(self.size)]
        # Starting point
        array[self.startingNode.position //
              self.size][self.startingNode.position % self.size] = 2
        # Ending point
        array[self.endingNode.position //
              self.size][self.endingNode.position % self.size] = 3
        return array

    def find_longest_path_node(self):
        """Used to set an endpoint for the completed maze."""
        longest_dist = 0
        node = 0
        for item in self.nodes:
            if not item.is_wall:
                if len(item.path_to_me) > longest_dist:
                    longest_dist = len(item.path_to_me)
                    node = item.position
        node = self.nodes[node]
        return node

    def set_straigth_path(self):
        self.endingNode = self.find_longest_path_node()
        self.path_to_goal = self.endingNode.path_to_me

    def printMaze(self):
        size = self.size
        rowTracker = 0
        maze = ''
        for node in self.nodes:
            if rowTracker % size == 0:
                maze += '\n'
            if node == self.startingNode:
                maze += "2"
            elif node == self.endingNode:
                maze += "3"
            elif node.is_wall:
                maze += 'x'
            else:
                maze += '.'
            rowTracker += 1;
        print(maze)

if __name__ == '__main__':
    wallSmasher = WallSmasher(100, 0)
    wallSmasher.smash()
    wallSmasher.printMaze()
    print(wallSmasher.get_array())
    print(wallSmasher.endingNode.position)

